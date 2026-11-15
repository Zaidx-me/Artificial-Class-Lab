# Design Spec — Agent Messaging, Code Cleanup & Documentation

- **Date:** 2026-11-13
- **Status:** Approved (pending spec review)
- **Project:** AI Recruitment Assistant
- **Author:** Sisyphus (with project owner)

## 1. Summary

Three related pieces of work on the existing AI Recruitment Assistant:

1. **Agent messaging** — the agent can send email *via chat*, to *any* recipient the
   user names, including *batch* sends. Sending is **draft-first**: the agent drafts,
   shows the exact text, and only sends after the user explicitly confirms.
2. **Code cleanup** — review the codebase, remove dead/duplicated code, tighten
   functions, and make it short and human-readable. **All existing features are kept.**
3. **Documentation** — a docstring on every module/class/function, a rewritten
   `README.md`, and a formal semester-project report.

Today the app is **read-only** with respect to email: it fetches and searches the
inbox but never sends. This spec adds the outbound path and cleans up the code
without changing existing behaviour.

## 2. Goals

- Let the user tell the agent, in chat, to email anyone (candidate or arbitrary
  address) and have the agent actually send it after confirmation.
- Support **batch** sending in two modes: *same message to many*, and
  *personalized per recipient*.
- Enforce **draft-first** in code, not only in the prompt, so the LLM cannot mail
  anyone on its own.
- Preserve every current feature (Gmail read, general-inbox search, RAG rubric,
  leaderboard, charts, uploads, local demo inbox).
- Make every function self-explanatory via docstrings and targeted comments.
- Produce submission-ready documentation (README + report).

## 3. Non-Goals (YAGNI)

- No email *attachments* on outbound mail.
- No HTML email templating / branding.
- No scheduling, reminders, or background sending (project rule: on-demand only).
- No open/click tracking, no bounce handling.
- No reply-threading / `In-Reply-To` headers.
- No change to the existing read/inbox behaviour or the UI theme.

## 4. Current Architecture (baseline)

```
app.py (Streamlit UI)
  └─ RecruitmentAgent (agent.py)  ── ReAct loop: LLM ↔ tools
        ├─ llm.py            (RealLLM / MockLLM, get_llm())
        ├─ tools/email_tool.py    fetch_applicant_emails, search_inbox, check_imap_connection
        ├─ tools/parser_tool.py   extract_text_from_resume (PDF/DOCX/TXT)
        ├─ tools/knowledge_tool.py search_knowledge (TF-IDF RAG)
        ├─ tools/database.py      SQLite: candidates, processed_emails, chat_memory, jobs
        └─ config.py              reads .env
```

- The agent loop is in `RecruitmentAgent.run(goal)`: it calls the LLM with a
  `TOOLS` schema list, executes the chosen tool, feeds the observation back, and
  stops when the LLM answers without a tool call.
- Conversation memory is stored in SQLite and replayed each run.
- The agent instance is rebuilt on every Streamlit rerun → **state that must
  survive a rerun (drafts) has to live in the database, not in memory.**

## 5. Feature — Chat-Driven, Draft-First Email Sending

### 5.1 Behaviour

- The user says, e.g., *"email ayesha@example.com and invite her to an interview"*,
  or *"send all shortlisted candidates a rejection"*.
- The agent **drafts** the message and shows the exact subject + body in chat,
  then asks for confirmation. It does **not** send in the same turn.
- The user confirms in chat (*"send"*, *"yes send it"*, *"go ahead"*, *"send them"*).
- The agent then sends and reports what was sent.

### 5.2 Data model — new `drafts` table

Added to `tools/database.py` (created in `init_db()`):

```sql
CREATE TABLE IF NOT EXISTS drafts(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    to_addr       TEXT,      -- one address, or comma-separated for a bulk draft
    cc_addr       TEXT,
    subject       TEXT,
    body          TEXT,
    candidate_id  INTEGER,   -- optional link to candidates.id
    status        TEXT DEFAULT 'pending',   -- pending | sent | failed
    error         TEXT,
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP,
    sent_at       TEXT
);
```

CRUD helpers in `database.py`:

| Function | Purpose |
|---|---|
| `save_draft(to, subject, body, cc="", candidate_id=None) -> dict` | Insert a `pending` draft, return `{"id", "to", "subject", "body"}`. |
| `get_draft(draft_id) -> dict \| None` | Load one draft. |
| `list_drafts(status=None) -> list[dict]` | List drafts, optionally filtered. |
| `mark_draft_sent(draft_id)` | Set `status='sent'`, `sent_at=CURRENT_TIMESTAMP`. |
| `mark_draft_failed(draft_id, error)` | Set `status='failed'`, store the error. |

### 5.3 New module — `tools/email_sender.py`

Thin, single-purpose module. SMTP only; it never touches IMAP.

| Function | Signature | Returns |
|---|---|---|
| `send_email` | `(to, subject, body, cc=None, *, user=None, password=None, server=None, port=None)` | `{"sent": True, "recipients": [...], "subject": ...}` or `{"sent": False, "error": "..."}` |
| `draft_email` | `(to, subject, body, cc="", candidate_id=None)` | `{"draft_id", "to", "subject", "body"}` or `{"error": ...}` |
| `send_draft` | `(draft_id, *, user=None, password=None)` | `{"sent": True, "to": ..., "draft_id": ...}` or `{"sent": False, "error": ...}` |
| `send_batch` | `(draft_ids, *, user=None, password=None)` | `{"sent": n, "failed": m, "results": [...]}` |

Details:

- **Recipients:** `to` accepts a single address or a comma/semicolon-separated
  string (bulk). Each address is validated with a simple regex; an invalid
  address is rejected at *draft* time with a clear error.
- **SMTP:** `smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)` (defaults
  `smtp.gmail.com:465`), `login(EMAIL_USER, EMAIL_PASS)`, `send_message` with an
  `email.message.EmailMessage`. Credentials come from `config` unless overridden.
- **Guards (in code):**
  - Missing credentials → `{"sent": False, "error": "Gmail isn't configured..."}`.
  - Draft not found, or `status != 'pending'` (already sent) → refuse.
  - Empty subject/body or invalid recipient → refuse at draft time.
- `send_batch` loops over drafts, calling `send_draft` for each, collecting
  per-draft results; one failure does not stop the rest.

### 5.4 Config additions (`config.py`)

```python
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT   = int(os.getenv("SMTP_PORT", "465"))
```

`EMAIL_USER` / `EMAIL_PASS` are already read from `.env`. `.env.example` documents
the new `SMTP_SERVER` / `SMTP_PORT` keys.

### 5.5 Agent integration (`agent.py`)

- **Three new tools** added to `TOOLS` and implemented as `_tool_*` methods:
  - `draft_email(to, subject, body, cc="")` → calls `email_sender.draft_email`.
  - `send_draft(draft_id)` → calls `email_sender.send_draft`.
  - `send_batch(draft_ids)` → calls `email_sender.send_batch`.
- **Confirmation guard (code-enforced):**
  - `run(goal)` computes `confirmed = bool(CONFIRM_RE.search(goal))` and stores it
    on the instance (`self._send_confirmed`).
  - `CONFIRM_RE` matches explicit confirmations: `send`, `send it`, `send them`,
    `yes send`, `go ahead`, `do it`, `send now`.
  - `_tool_send_draft` / `_tool_send_batch` return
    `{"error": "Not confirmed. Show the draft and ask the user to confirm before sending."}`
    unless `self._send_confirmed` is true.
  - Result: even if the LLM calls a send tool early, **nothing is sent** until the
    user's own message is a confirmation. This is the human-in-the-loop gate.
- **Prompt additions** (`SYSTEM_PROMPT`): an "Emailing" section instructing the
  agent to (a) always draft first, (b) never send in the same turn, (c) show the
  exact text and ask to confirm, (d) only send after explicit confirmation,
  (e) email any address the user names, (f) for bulk use a comma-separated list,
  (g) for personalized batches call `draft_email` once per person then `send_batch`.

### 5.6 Batch modes

| Mode | How the agent does it | Send |
|---|---|---|
| Same message to many | one `draft_email` with comma-separated `to` | one `send_draft` |
| Personalized | `draft_email` once per recipient (tailored body) | `send_batch([ids])` |

### 5.7 UI (`app.py`)

- Chat-driven: no new Send button (the user asked for sending "via chat").
- The agent's chat reply already contains the draft text and the confirmation ask.
- Optionally show a small "Pending drafts" expander listing `list_drafts('pending')`
  for visibility. Marked optional so it can be dropped if it clutters the chat.

### 5.8 Error handling

- All send functions return `{"sent": False, "error": ...}` instead of raising, so
  the agent adapts and reports plainly (consistent with existing tool style).
- Network/SMTP errors are caught and surfaced as a short human message.

## 6. Feature — Code Cleanup (keep all features)

- **Docstrings:** every module, class, and function gets a clear docstring
  (purpose, args, returns). Inline comments only where logic is non-obvious.
- **Deduplicate:** the two IMAP blocks in `email_tool.py`
  (`fetch_applicant_emails`, `search_inbox`) share one connection/select helper.
- **Tighten:** extract small helpers in `agent.py` where the loop is dense;
  clearer names; remove the small amount of genuinely dead code found during the
  pass. `config.py` has no dead code after the earlier env-only refactor.
- **Behaviour is unchanged** — the existing 13 tests must still pass.

## 7. Feature — Documentation

1. **`README.md`** — rewritten: what it is, features, architecture, setup
   (`.env`, install), running, usage examples, testing, project structure.
2. **`docs/PROJECT_REPORT.md`** — formal semester report with sections:
   Abstract; Introduction; Objectives; Background & Concepts (agents, ReAct,
   tool-calling, RAG/TF-IDF, IMAP/SMTP); System Design; Architecture (diagram);
   Component-by-component explanation; Methodology; Tools & Technologies;
   Testing; Results; Limitations; Future Work; Conclusion; References.
3. **This spec** under `docs/superpowers/specs/`.

## 8. Testing Plan

New `tests/test_email_sender.py` (SMTP mocked — **no real mail is ever sent**):

- `draft_email` persists a `pending` draft and returns its id.
- `draft_email` rejects an invalid recipient.
- `send_draft` refuses when credentials are missing.
- `send_draft` refuses to send a draft twice.
- `send_batch` sends N drafts and reports failures independently.
- Agent confirmation guard: `send_draft` is refused when the user message is not a
  confirmation, and allowed when it is.

Existing `tests/test_pipeline.py` + `tests/test_ui.py` (13 tests) must stay green.

## 9. Files Touched

**New**
- `tools/email_sender.py`
- `tests/test_email_sender.py`
- `docs/PROJECT_REPORT.md`
- `docs/superpowers/specs/2026-11-13-agent-messaging-and-refactor-design.md` (this file)

**Modified**
- `agent.py` — new tools, confirmation guard, prompt section, cleanup + docstrings
- `app.py` — optional pending-drafts view, docstrings
- `config.py` — `SMTP_SERVER`, `SMTP_PORT`
- `tools/email_tool.py` — dedupe IMAP logic, docstrings
- `tools/database.py` — `drafts` table + CRUD helpers
- `README.md`, `.env.example`, tests

## 10. Decisions & Rationale

- **Drafts in SQLite, not memory** — the agent is rebuilt each Streamlit rerun.
- **Confirmation enforced in code** — prompt-only safety is not reliable.
- **No Send button** — the user asked to send "via chat".
- **Keep all features** — the user chose clean + document over trimming features.
- **Mock SMTP in tests** — never send real mail during automated runs.

## 11. Open Questions

None blocking. Confirmed with the user:
- Sending = email candidates/anyone, **draft-first**.
- Refactor = **clean + document, keep all features**.
- Docs = **docstrings + README + formal report**.
- Batch = **both** bulk-identical and personalized.
- Sending = **chat-driven** (no UI button).
