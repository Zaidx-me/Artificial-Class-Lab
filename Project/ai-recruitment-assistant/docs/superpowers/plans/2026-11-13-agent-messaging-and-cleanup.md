# Agent Messaging & Code Cleanup — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add chat-driven, draft-first outbound email (single + batch) to the AI Recruitment Assistant, then clean up and document the whole codebase without changing existing behaviour.

**Architecture:** A new `tools/email_sender.py` owns all SMTP and persists drafts in SQLite (`drafts` table) so they survive Streamlit reruns. The agent gets three new tools (`draft_email`, `send_draft`, `send_batch`) plus a code-enforced confirmation guard so the LLM cannot send until the user's own message is an explicit confirmation. Existing read/inbox behaviour is untouched.

**Tech Stack:** Python 3, Streamlit, stdlib `smtplib`/`email.message`, SQLite, pytest.

**Spec:** `docs/superpowers/specs/2026-11-13-agent-messaging-and-refactor-design.md`

## Global Constraints

- Keep **every** existing feature; the refactor must not change behaviour.
- All existing 13 tests (`tests/test_pipeline.py`, `tests/test_ui.py`) must stay green.
- Tests must **never send real mail** — SMTP is mocked/patched.
- Credentials come only from `.env` (`config`); no secrets in the UI.
- Sending is **draft-first** and **chat-driven**; no new Send button.
- Run commands with the Anaconda interpreter: `~/anaconda3/bin/python -m pytest ...`.
- No type-error suppression (`as any` equivalents); no bare `except` that hides errors.
- Use stdlib only (no new dependencies).

---

## File Structure

- `tools/email_sender.py` — **new**, single responsibility: SMTP send + draft lifecycle. No IMAP.
- `tools/database.py` — **modify**: add `drafts` table + CRUD helpers.
- `config.py` — **modify**: add `SMTP_SERVER`, `SMTP_PORT`.
- `agent.py` — **modify**: 3 tools, confirmation guard, prompt section, cleanup + docstrings.
- `app.py` — **modify**: optional pending-drafts view, docstrings.
- `tools/email_tool.py` — **modify**: dedupe IMAP logic, docstrings.
- `tests/test_email_sender.py` — **new**.
- `README.md`, `docs/PROJECT_REPORT.md`, `.env.example` — **new/rewrite**.

---

### Task 1: Config — SMTP settings

**Files:**
- Modify: `config.py`
- Modify: `.env.example`

**Interfaces:**
- Produces: `config.SMTP_SERVER: str` (default `"smtp.gmail.com"`), `config.SMTP_PORT: int` (default `465`).

- [ ] **Step 1: Add settings to `config.py`** (after the IMAP block)

```python
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
```

- [ ] **Step 2: Document in `.env.example`** (append)

```
# --- Outbound email (sending) ---
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
```

- [ ] **Step 3: Verify import**

Run: `~/anaconda3/bin/python -c "import config; print(config.SMTP_SERVER, config.SMTP_PORT)"`
Expected: `smtp.gmail.com 465`

- [ ] **Step 4: Commit**

```bash
git add config.py .env.example
git commit -m "feat(config): add SMTP_SERVER/SMTP_PORT settings"
```

---

### Task 2: Database — `drafts` table + CRUD

**Files:**
- Modify: `tools/database.py`
- Test: `tests/test_email_sender.py` (created here, extended later)

**Interfaces:**
- Produces:
  - `db.save_draft(to, subject, body, cc="", candidate_id=None) -> {"draft_id", "to", "subject", "body", "status"}`
  - `db.get_draft(draft_id) -> dict | None`
  - `db.list_drafts(status=None) -> list[dict]`
  - `db.mark_draft_sent(draft_id) -> None`
  - `db.mark_draft_failed(draft_id, error="") -> None`

- [ ] **Step 1: Add the table** inside `init_db()`'s `executescript`

```sql
        CREATE TABLE IF NOT EXISTS drafts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            to_addr TEXT, cc_addr TEXT, subject TEXT, body TEXT,
            candidate_id INTEGER, status TEXT DEFAULT 'pending',
            error TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, sent_at TEXT);
```

- [ ] **Step 2: Write the failing test** (`tests/test_email_sender.py`)

```python
import config
from tools import database as db


def test_save_and_get_draft(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DB_PATH", str(tmp_path / "t.db"))
    db.init_db()
    saved = db.save_draft("a@x.com", "Hi", "Body")
    assert saved["status"] == "pending"
    got = db.get_draft(saved["draft_id"])
    assert got["to_addr"] == "a@x.com"
    db.mark_draft_sent(saved["draft_id"])
    assert db.get_draft(saved["draft_id"])["status"] == "sent"
```

- [ ] **Step 3: Run test — expect FAIL**

Run: `~/anaconda3/bin/python -m pytest tests/test_email_sender.py -q`
Expected: FAIL (`no such table: drafts` / `save_draft` missing)

- [ ] **Step 4: Implement the CRUD helpers**

```python
# ---------- drafts (outbound email) ----------
def save_draft(to: str, subject: str, body: str, cc: str = "", candidate_id=None) -> dict:
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO drafts(to_addr,cc_addr,subject,body,candidate_id) VALUES (?,?,?,?,?)",
            (to, cc, subject, body, candidate_id))
        did = cur.lastrowid
    return {"draft_id": did, "to": to, "subject": subject, "body": body, "status": "pending"}


def get_draft(draft_id) -> dict | None:
    with _conn() as c:
        r = c.execute("SELECT * FROM drafts WHERE id=?", (int(draft_id),)).fetchone()
        return dict(r) if r else None


def list_drafts(status: str | None = None) -> list[dict]:
    q, args = "SELECT * FROM drafts", []
    if status:
        q += " WHERE status=?"
        args.append(status)
    q += " ORDER BY id DESC"
    with _conn() as c:
        return [dict(r) for r in c.execute(q, args).fetchall()]


def mark_draft_sent(draft_id):
    with _conn() as c:
        c.execute("UPDATE drafts SET status='sent', sent_at=CURRENT_TIMESTAMP WHERE id=?", (int(draft_id),))


def mark_draft_failed(draft_id, error: str = ""):
    with _conn() as c:
        c.execute("UPDATE drafts SET status='failed', error=? WHERE id=?", (error, int(draft_id)))
```

- [ ] **Step 5: Run test — expect PASS**

Run: `~/anaconda3/bin/python -m pytest tests/test_email_sender.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add tools/database.py tests/test_email_sender.py
git commit -m "feat(db): add drafts table and CRUD helpers"
```

---

### Task 3: `tools/email_sender.py`

**Files:**
- Create: `tools/email_sender.py`
- Test: `tests/test_email_sender.py` (extend)

**Interfaces:**
- Consumes: `config.EMAIL_USER`, `config.EMAIL_PASS`, `config.SMTP_SERVER`, `config.SMTP_PORT`; `db.save_draft/get_draft/mark_draft_sent/mark_draft_failed`.
- Produces:
  - `send_email(to, subject, body, cc=None, *, user=None, password=None, server=None, port=None) -> {"sent": bool, ...}`
  - `draft_email(to, subject, body, cc="", candidate_id=None) -> {"draft_id", ...} | {"error"}`
  - `send_draft(draft_id, *, user=None, password=None) -> {"sent": bool, ...}`
  - `send_batch(draft_ids, *, user=None, password=None) -> {"sent", "failed", "results"}`

- [ ] **Step 1: Write failing tests** (append to `tests/test_email_sender.py`)

```python
import smtplib
from tools import email_sender


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
```

- [ ] **Step 2: Run — expect FAIL** (`ModuleNotFoundError: tools.email_sender`)

Run: `~/anaconda3/bin/python -m pytest tests/test_email_sender.py -q`

- [ ] **Step 3: Implement `tools/email_sender.py`**

```python
"""Outbound email: SMTP sending + draft-first persistence.

This is the ONLY module that talks SMTP; it never touches IMAP. Drafts are
stored in SQLite so they survive Streamlit reruns. Every send is guarded:
credentials must exist, the draft must exist and still be 'pending'.
"""
import re
import smtplib
from email.message import EmailMessage

import config
from tools import database as db

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _split_addresses(to) -> list[str]:
    """Turn a string/list of recipients into a clean list of addresses."""
    raw = to if isinstance(to, (list, tuple)) else re.split(r"[,;\s]+", str(to or ""))
    return [a.strip() for a in raw if a.strip()]


def _invalid(addresses: list[str]) -> list[str]:
    """Return the subset of addresses that are not valid email addresses."""
    return [a for a in addresses if not _EMAIL_RE.match(a)]


def send_email(to, subject, body, cc=None, *, user=None, password=None, server=None, port=None) -> dict:
    """Send one plain-text email via SMTP. Returns {'sent': bool, ...}; never raises."""
    recipients = _split_addresses(to)
    bad = _invalid(recipients)
    if bad:
        return {"sent": False, "error": f"Invalid recipient(s): {', '.join(bad)}"}
    if not recipients:
        return {"sent": False, "error": "No recipient given."}
    if not (subject or "").strip() or not (body or "").strip():
        return {"sent": False, "error": "Subject and body cannot be empty."}
    user = (user if user is not None else config.EMAIL_USER).strip()
    password = (password if password is not None else config.EMAIL_PASS).replace(" ", "").strip()
    server = (server or config.SMTP_SERVER).strip()
    port = int(port or config.SMTP_PORT)
    if not (user and password):
        return {"sent": False, "error": "Gmail isn't configured. Set EMAIL_USER and EMAIL_PASS in .env."}
    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = ", ".join(recipients)
    if cc:
        msg["Cc"] = ", ".join(_split_addresses(cc))
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL(server, port, timeout=30) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
    except Exception as exc:  # surfaced to the agent, not a crash
        return {"sent": False, "error": f"{type(exc).__name__}: {exc}"}
    return {"sent": True, "recipients": recipients, "subject": subject}


def draft_email(to, subject, body, cc="", candidate_id=None) -> dict:
    """Validate recipients and persist a 'pending' draft. Never sends."""
    recipients = _split_addresses(to)
    bad = _invalid(recipients)
    if bad:
        return {"error": f"Invalid recipient(s): {', '.join(bad)}"}
    if not recipients:
        return {"error": "No recipient given."}
    return db.save_draft(", ".join(recipients), subject, body, cc, candidate_id)


def send_draft(draft_id, *, user=None, password=None) -> dict:
    """Send a stored pending draft; refuses if missing, already sent, or unconfigured."""
    draft = db.get_draft(draft_id)
    if not draft:
        return {"sent": False, "error": f"No draft with id {draft_id}."}
    if draft["status"] != "pending":
        return {"sent": False, "error": f"Draft {draft_id} is already {draft['status']}."}
    result = send_email(draft["to_addr"], draft["subject"], draft["body"],
                        draft["cc_addr"], user=user, password=password)
    if result.get("sent"):
        db.mark_draft_sent(draft_id)
        return {"sent": True, "draft_id": draft_id, "to": draft["to_addr"]}
    db.mark_draft_failed(draft_id, result.get("error", ""))
    return {"sent": False, "draft_id": draft_id, "error": result.get("error", "")}


def send_batch(draft_ids, *, user=None, password=None) -> dict:
    """Send several drafts in one call; one failure does not stop the rest."""
    results = [send_draft(did, user=user, password=password) for did in draft_ids]
    sent = sum(1 for r in results if r.get("sent"))
    return {"sent": sent, "failed": len(results) - sent, "results": results}
```

- [ ] **Step 4: Run — expect PASS**

Run: `~/anaconda3/bin/python -m pytest tests/test_email_sender.py -q`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add tools/email_sender.py tests/test_email_sender.py
git commit -m "feat(email): add SMTP sender with draft-first lifecycle"
```

---

### Task 4: Agent tools + confirmation guard

**Files:**
- Modify: `agent.py`
- Test: `tests/test_email_sender.py` (extend)

**Interfaces:**
- Consumes: `email_sender.draft_email/send_draft/send_batch`.
- Produces: agent tools `draft_email`, `send_draft`, `send_batch`; instance flag `self._send_confirmed: bool`.

- [ ] **Step 1: Write failing test** (append)

```python
from agent import RecruitmentAgent
from llm import MockLLM


def test_send_tool_blocked_without_confirmation(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    agent = RecruitmentAgent(llm=MockLLM())
    d = agent._tool_draft_email(to="a@x.com", subject="s", body="b")
    agent._send_confirmed = False
    assert "error" in agent._tool_send_draft(draft_id=d["draft_id"])
    agent._send_confirmed = True
    assert agent._tool_send_draft(draft_id=d["draft_id"])["sent"] is True
```

- [ ] **Step 2: Run — expect FAIL** (`_tool_draft_email` missing)

Run: `~/anaconda3/bin/python -m pytest tests/test_email_sender.py::test_send_tool_blocked_without_confirmation -q`

- [ ] **Step 3: Implement**

Add near the imports:
```python
from tools import email_sender
```
Add after `ACTION_RE`:
```python
# An explicit confirmation from the user, required before anything is sent.
CONFIRM_RE = re.compile(
    r"^\s*(yes|yeah|yep|ok|okay|sure|go ahead|do it|send|send it|send them|"
    r"send now|please send|confirm|go for it)\b", re.I)
```
In `__init__` add: `self._send_confirmed = False`.
Add the three tool methods after `_tool_get_candidate_details`:
```python
    def _tool_draft_email(self, to, subject, body, cc="", **_):
        """Create a pending draft (does not send)."""
        return email_sender.draft_email(to, subject, body, cc)

    def _tool_send_draft(self, draft_id, **_):
        """Send one pending draft — only when the user's last message confirmed it."""
        if not self._send_confirmed:
            return {"error": "Not confirmed. Show the draft and ask the user to confirm before sending."}
        return email_sender.send_draft(draft_id)

    def _tool_send_batch(self, draft_ids, **_):
        """Send several pending drafts — only when the user's last message confirmed it."""
        if not self._send_confirmed:
            return {"error": "Not confirmed. Show the drafts and ask the user to confirm before sending."}
        return email_sender.send_batch(draft_ids)
```
Append these to `TOOLS`:
```python
    {"type": "function", "function": {"name": "draft_email",
     "description": "Create a draft email to any recipient(s). Does NOT send. Show the draft to the user and ask them to confirm. 'to' may be a single address or a comma-separated list for a bulk message.",
     "parameters": {"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"},
                     "body": {"type": "string"}, "cc": {"type": "string"}}, "required": ["to", "subject", "body"]}}},
    {"type": "function", "function": {"name": "send_draft",
     "description": "Send ONE previously created pending draft by its draft_id. Only call after the user explicitly confirms.",
     "parameters": {"type": "object", "properties": {"draft_id": {"type": "integer"}}, "required": ["draft_id"]}}},
    {"type": "function", "function": {"name": "send_batch",
     "description": "Send SEVERAL pending drafts by id. Only call after the user explicitly confirms.",
     "parameters": {"type": "object", "properties": {"draft_ids": {"type": "array", "items": {"type": "integer"}}}, "required": ["draft_ids"]}}},
```
In `run()`, right after `action_request = ...`:
```python
        self._send_confirmed = bool(CONFIRM_RE.search(goal))
```
Add an "Emailing" section to `SYSTEM_PROMPT`:
```
Emailing:
- To email anyone, first call draft_email, then show the exact subject and body and ask the user to confirm. Never send in the same turn as drafting.
- Only call send_draft / send_batch after the user explicitly confirms ("send", "send it", "go ahead").
- You may email any address the user names. For the same message to many people, pass a comma-separated list to draft_email. For a personalized batch, call draft_email once per person, then send_batch.
- Never invent recipients; use the addresses the user gave or that a tool returned.
```

- [ ] **Step 4: Run — expect PASS**

Run: `~/anaconda3/bin/python -m pytest tests/test_email_sender.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add agent.py tests/test_email_sender.py
git commit -m "feat(agent): add draft-first email tools with confirmation guard"
```

---

### Task 5: App wiring (chat-driven) + docstrings

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: `db.list_drafts`, existing `agent.run`.

- [ ] **Step 1:** Add a small **Pending drafts** expander in the Agent tab (below the chat history) so the user can see unsent drafts:

```python
    pending = db.list_drafts("pending")
    if pending:
        with st.expander(f"📬 Pending drafts ({len(pending)})"):
            for d in pending:
                st.markdown(f"**#{d['id']} → {d['to_addr']}** — {d['subject']}")
                st.caption(d["body"][:300])
```

- [ ] **Step 2:** Ensure `from tools import database as db` is imported in `app.py` (add if missing).

- [ ] **Step 3: Verify** the app still boots

Run: `~/anaconda3/bin/streamlit run app.py --server.headless true --server.port 8511 &` then `curl -s -o /dev/null -w "%{http_code}" http://localhost:8511` → `200`, then kill it.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "feat(ui): show pending drafts in the agent tab"
```

---

### Task 6: Cleanup — dedupe IMAP + docstrings everywhere

**Files:**
- Modify: `tools/email_tool.py`, `agent.py`, `llm.py`, `app.py`, `config.py`, `tools/*.py`, `scripts/*.py`

- [ ] **Step 1:** In `tools/email_tool.py`, extract the repeated connection/select boilerplate into one helper used by both `fetch_applicant_emails` and `search_inbox`:

```python
def _connect(user: str, password: str, server: str) -> imaplib.IMAP4_SSL:
    """Open an authenticated, read-only IMAP connection to the inbox."""
    mail = imaplib.IMAP4_SSL(server, timeout=30)
    mail.login(user, password)
    mail.select("inbox", readonly=True)
    return mail
```
Replace both inline blocks with `mail = _connect(user, password, server)` inside a `try/finally` that logs out.

- [ ] **Step 2:** Add a docstring to **every** module, class, and function that lacks one (`agent.py`, `app.py`, `llm.py`, `config.py`, `tools/parser_tool.py`, `tools/knowledge_tool.py`, `scripts/make_samples.py`). Each docstring states purpose, args, returns.

- [ ] **Step 3:** Remove any genuinely dead code found (unused imports/vars). Do **not** change behaviour.

- [ ] **Step 4: Run the full suite**

Run: `~/anaconda3/bin/python -m pytest -q tests -p no:cacheprovider`
Expected: all pass (13 existing + new).

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "refactor: dedupe IMAP flow, document all functions"
```

---

### Task 7: README + project report

**Files:**
- Rewrite: `README.md`
- Create: `docs/PROJECT_REPORT.md`

- [ ] **Step 1:** Rewrite `README.md`: overview, features, architecture, setup (`.env` incl. SMTP), running, usage examples (including "email X" / batch), testing, project structure.

- [ ] **Step 2:** Write `docs/PROJECT_REPORT.md` with: Abstract, Introduction, Objectives, Background & Concepts (agents, ReAct, tool-calling, RAG/TF-IDF, IMAP/SMTP), System Design, Architecture (mermaid diagram), Component-by-component explanation, Methodology, Tools & Technologies, Testing, Results, Limitations, Future Work, Conclusion, References.

- [ ] **Step 3: Commit**

```bash
git add README.md docs/PROJECT_REPORT.md
git commit -m "docs: rewrite README and add semester project report"
```

---

### Task 8: Final verification

- [ ] **Step 1:** `~/anaconda3/bin/python -m py_compile app.py agent.py llm.py config.py tools/*.py` → no errors.
- [ ] **Step 2:** `~/anaconda3/bin/python -m pytest -q tests -p no:cacheprovider` → all pass.
- [ ] **Step 3:** Boot Streamlit headless on a scratch port → HTTP 200, no tracebacks.
- [ ] **Step 4:** Confirm `grep -rn "as any\|@ts-ignore" .` is irrelevant (Python) and no secrets were added to tracked files.

---

## Self-Review

- **Spec coverage:** sending (Tasks 1–4), chat-driven UI (Task 5), cleanup (Task 6), docs (Task 7), testing (Tasks 2–4, 8). ✔
- **Placeholder scan:** no TBD/TODO; all code steps contain real code. ✔
- **Type consistency:** `save_draft` returns `draft_id`; `draft_email` returns the same dict; `send_draft(draft_id)` consumes it; `send_batch(draft_ids)` matches the agent tool arg name. ✔
