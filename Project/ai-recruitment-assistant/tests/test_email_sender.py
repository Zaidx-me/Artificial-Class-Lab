"""Tests for the outbound email path: drafts, SMTP sender, and the agent guard.

SMTP is always mocked — no real mail is ever sent during the suite.
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["USE_MOCK_LLM"] = "1"
os.environ["DB_PATH"] = str(Path(tempfile.mkdtemp()) / "email.db")
os.environ["EMAIL_USER"] = ""
os.environ["EMAIL_PASS"] = ""
os.environ["LLM_API_KEY"] = ""
os.environ["LLM_BASE_URL"] = ""

import smtplib

import config
from agent import RecruitmentAgent
from llm import MockLLM
from tools import database as db
from tools import email_sender


def test_save_and_get_draft(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DB_PATH", str(tmp_path / "t.db"))
    db.init_db()
    saved = db.save_draft("a@x.com", "Hi", "Body")
    assert saved["status"] == "pending"
    got = db.get_draft(saved["draft_id"])
    assert got["to_addr"] == "a@x.com"
    db.mark_draft_sent(saved["draft_id"])
    assert db.get_draft(saved["draft_id"])["status"] == "sent"


class _FakeSMTP:
    sent = []
    def __init__(self, *a, **k): pass
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def login(self, *a): pass
    def send_message(self, msg): _FakeSMTP.sent.append(msg)


def _setup(tmp_path, monkeypatch, user="me@x.com", pw="app"):
    monkeypatch.setattr(config, "DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.setattr(config, "EMAIL_USER", user)
    monkeypatch.setattr(config, "EMAIL_PASS", pw)
    db.init_db()
    _FakeSMTP.sent = []
    monkeypatch.setattr(smtplib, "SMTP_SSL", _FakeSMTP)


def test_draft_email_rejects_bad_address(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert "error" in email_sender.draft_email("not-an-email", "s", "b")


def test_send_draft_refuses_without_credentials(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch, user="", pw="")
    d = email_sender.draft_email("a@x.com", "s", "b")
    res = email_sender.send_draft(d["draft_id"])
    assert res["sent"] is False and "error" in res


def test_send_draft_sends_and_marks_sent(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    d = email_sender.draft_email("a@x.com", "Hello", "Body")
    assert email_sender.send_draft(d["draft_id"])["sent"] is True
    assert db.get_draft(d["draft_id"])["status"] == "sent"
    assert len(_FakeSMTP.sent) == 1


def test_send_draft_refuses_double_send(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    d = email_sender.draft_email("a@x.com", "s", "b")
    email_sender.send_draft(d["draft_id"])
    assert email_sender.send_draft(d["draft_id"])["sent"] is False


def test_send_batch_reports_counts(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    ids = [email_sender.draft_email(f"u{i}@x.com", "s", "b")["draft_id"] for i in range(3)]
    res = email_sender.send_batch(ids)
    assert res["sent"] == 3 and res["failed"] == 0


def test_send_tool_blocked_without_confirmation(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    agent = RecruitmentAgent(llm=MockLLM())
    d = agent._tool_draft_email(to="a@x.com", subject="s", body="b")
    agent._send_confirmed = False
    assert "error" in agent._tool_send_draft(draft_id=d["draft_id"])
    agent._send_confirmed = True
    assert agent._tool_send_draft(draft_id=d["draft_id"])["sent"] is True


def test_streamed_response_is_assembled_offline():
    """A fake OpenAI-style chunk stream assembles content + tool-call deltas (no network)."""
    from types import SimpleNamespace as NS

    from llm import _assemble_stream

    def chunk(content=None, tool_calls=None):
        return NS(choices=[NS(delta=NS(content=content, tool_calls=tool_calls))])

    chunks = [
        chunk(content="Hel"),
        chunk(content="lo"),
        chunk(tool_calls=[NS(index=0, id="call_1",
                             function=NS(name="get_leaderboard", arguments='{"li'))]),
        chunk(tool_calls=[NS(index=0, id=None,
                             function=NS(name=None, arguments='mit": 3}'))]),
        NS(choices=[]),
    ]
    seen = []
    msg = _assemble_stream(chunks, seen.append)
    assert seen == ["Hel", "lo"]
    assert msg == {
        "role": "assistant",
        "content": "Hello",
        "tool_calls": [{"id": "call_1", "type": "function",
                        "function": {"name": "get_leaderboard", "arguments": '{"limit": 3}'}}],
    }
