"""End-to-end test of the agent loop using the offline mock LLM (no API key needed)."""
import json, os, sys, tempfile
from email import message_from_string, policy
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["USE_MOCK_LLM"] = "1"
os.environ["DB_PATH"] = str(Path(tempfile.mkdtemp()) / "test.db")
os.environ["EMAIL_USER"] = ""
os.environ["EMAIL_PASS"] = ""
os.environ["LLM_API_KEY"] = ""
os.environ["LLM_BASE_URL"] = ""

from agent import RecruitmentAgent
from tools import database as db
from tools.email_tool import _looks_like_application, check_imap_connection, search_inbox
from tools.knowledge_tool import search_knowledge


def test_rag():
    r = search_knowledge("how many points for experience", 2)["results"]
    assert r and "Relevant experience" in r[0]["text"]


def test_full_run_ranking_memory_dedup():
    a = RecruitmentAgent("Software Engineer")
    out = a.run("Process all new applicant emails for the Software Engineer role.")
    tools = [t["tool"] for t in out["trace"]]
    assert tools[0] == "fetch_new_applications" and tools.count("save_candidate") == 5
    assert "skip_email" in tools and tools[-1] == "get_leaderboard"
    ranked = db.get_ranked_candidates("Software Engineer")
    assert [c["name"] for c in ranked][0] == "Ayesha Khan"
    assert ranked[-1]["name"] == "Usman Tariq"
    assert all(0 <= c["score"] <= 100 for c in ranked)
    # second run: dedup memory -> nothing new gets scored again
    out2 = a.run("Process new applications again.")
    assert [t["tool"] for t in out2["trace"]].count("save_candidate") == 0
    assert len(db.get_ranked_candidates()) == 5
    # conversational memory + Q&A
    out3 = a.run("Who are the top 3 candidates?")
    assert out3["trace"][0]["tool"] == "get_leaderboard" and "Ayesha" in out3["answer"]
    assert len(db.get_memory(20)) == 6


def test_application_filter_accepts_resume_email():
    msg = message_from_string(
        "From: applicant@example.com\nSubject: Application - Software Engineer\n\nPlease find my CV.",
        policy=policy.default,
    )
    assert _looks_like_application(msg)


def test_application_filter_rejects_newsletter():
    msg = message_from_string(
        "From: news@example.com\nSubject: Weekly offers\n\nThis week only.",
        policy=policy.default,
    )
    assert not _looks_like_application(msg)


def test_imap_connection_requires_credentials():
    assert check_imap_connection("", "")["ok"] is False


def test_imap_filter_scans_past_non_applications(monkeypatch, tmp_path):
    import tools.email_tool as email_tool
    from email.message import EmailMessage

    def raw(subject, mid):
        m = EmailMessage()
        m["From"] = "x@example.com"
        m["Subject"] = subject
        m["Message-ID"] = mid
        m.set_content("This week only." if "Weekly" in subject else "Please find my CV.")
        return m.as_bytes()

    messages = [raw("Weekly offers", f"<scan-{i}@example.com>") for i in range(5)]
    messages.append(raw("Application - Software Engineer", "<scan-app@example.com>"))

    class FakeMail:
        def login(self, user, password):
            return "OK", [b"logged in"]

        def select(self, mailbox, readonly=False):
            assert readonly is True
            return "OK", [b"1"]

        def search(self, charset, criteria):
            assert criteria == "(UNSEEN)"
            return "OK", [b"1 2 3 4 5 6"]

        def fetch(self, num, spec):
            return "OK", [(b"1 (RFC822)", messages[int(num) - 1])]

        def logout(self):
            pass

    monkeypatch.setattr(email_tool.imaplib, "IMAP4_SSL", lambda host, timeout=30: FakeMail())
    monkeypatch.setattr(email_tool.config, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(email_tool.config, "DOWNLOAD_DIR", tmp_path / "downloads")
    db.init_db()

    out = email_tool.fetch_applicant_emails(
        limit=1, user="u@example.com", password="pw",
        only_applications=True, mode="imap",
    )
    assert out["count"] == 1
    assert out["emails"][0]["subject"] == "Application - Software Engineer"
    assert out["scanned"] == 6


def test_check_and_yes_trigger_fetch_tool():
    from agent import TOOLS
    from llm import MockLLM

    for text in ("check", "yes", "check the inbox"):
        out = MockLLM().chat([{"role": "user", "content": text}], tools=TOOLS)
        assert out["tool_calls"][0]["function"]["name"] == "fetch_new_applications"


def test_large_tool_observation_stays_valid_json():
    from agent import tool_observation

    payload = {"count": 20, "emails": [{"body": "x" * 1500, "attachments": ["/tmp/cv.pdf"]} for _ in range(20)]}
    parsed = json.loads(tool_observation(payload))
    assert parsed["emails"]


def test_search_inbox_local_filters_by_query():
    assert search_inbox(query="Ayesha", mode="local")["count"] >= 1
    assert search_inbox(query="zzz-no-such-thing", mode="local")["count"] == 0


def test_search_inbox_requires_gmail_credentials():
    with pytest.raises(ValueError):
        search_inbox(mode="imap")


def test_mock_agent_routes_general_email_question():
    agent = RecruitmentAgent(job_title="Software Engineer")
    out = agent.run("what emails are in my inbox?")
    assert any(t["tool"] == "search_inbox" for t in out["trace"])
    assert out["answer"]


def test_process_new_applications_batch(monkeypatch, tmp_path):
    import config
    from llm import MockLLM

    monkeypatch.setattr(config, "DB_PATH", str(tmp_path / "batch.db"))
    monkeypatch.setattr(config, "DOWNLOAD_DIR", tmp_path / "downloads")
    agent = RecruitmentAgent("Software Engineer", llm=MockLLM())
    events = []
    agent._on_step = events.append

    result = agent._tool_process_new_applications()

    assert result["scored"] >= 1
    assert len(result["leaderboard"]["candidates"]) >= 1
    assert db.get_ranked_candidates(agent.job_title)
    scored_ids = [e["args"]["source_id"] for e in events if e["tool"] == "evaluate_candidate"]
    assert scored_ids
    assert all(db.is_processed(sid) for sid in scored_ids)
