"""Tool 3 + long-term memory: SQLite persistence (stdlib only).

Tables
  candidates        - evaluated applicants (score, justification, ...)
  processed_emails  - Message-IDs / file hashes already handled (de-duplication memory)
  chat_memory       - conversation history so the agent remembers earlier turns
  jobs              - job descriptions the recruiter has configured
  drafts            - outbound emails persisted before sending (draft-first flow)
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import config


@contextmanager
def _conn():
    """Open a SQLite connection, commit on success, and always close it."""
    Path(config.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(config.DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db():
    """Create all tables if they do not already exist."""
    with _conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS candidates(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT, name TEXT, email TEXT, score REAL,
            skills_score REAL, experience_score REAL, education_score REAL,
            strengths TEXT, weaknesses TEXT, missing_skills TEXT,
            justification TEXT, recommendation TEXT,
            resume_path TEXT, source_id TEXT UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS processed_emails(
            source_id TEXT PRIMARY KEY, sender TEXT, subject TEXT,
            processed_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS chat_memory(
            id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS jobs(
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS drafts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            to_addr TEXT, cc_addr TEXT, subject TEXT, body TEXT,
            candidate_id INTEGER, status TEXT DEFAULT 'pending',
            error TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, sent_at TEXT);
        """)


# ---------- candidates ----------
def save_candidate(data: dict) -> dict:
    """Insert/replace an evaluated candidate. Returns {'saved': True, 'id': ...}."""
    def lst(v):
        """Format a list value as newline-prefixed bullets."""
        return "\n".join(f"- {x}" for x in v) if isinstance(v, list) else (v or "")
    with _conn() as c:
        c.execute("""INSERT OR REPLACE INTO candidates
            (job_title,name,email,score,skills_score,experience_score,education_score,
             strengths,weaknesses,missing_skills,justification,recommendation,resume_path,source_id)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (data.get("job_title", ""), data.get("name", "Unknown"), data.get("email", ""),
             float(data.get("score", 0) or 0),
             float(data.get("skills_score", 0) or 0),
             float(data.get("experience_score", 0) or 0),
             float(data.get("education_score", 0) or 0),
             lst(data.get("strengths")), lst(data.get("weaknesses")),
             lst(data.get("missing_skills")), data.get("justification", ""),
             data.get("recommendation", ""), data.get("resume_path", ""),
             data.get("source_id") or data.get("resume_path", "")))
        cid = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    return {"saved": True, "id": cid}


def get_ranked_candidates(job_title: str | None = None, limit: int | None = None) -> list[dict]:
    """Return candidates ordered by score, optionally filtered by job title and limited."""
    q, args = "SELECT * FROM candidates", []
    if job_title:
        q += " WHERE job_title = ?"
        args.append(job_title)
    q += " ORDER BY score DESC, id ASC"
    if limit:
        q += " LIMIT ?"
        args.append(int(limit))
    with _conn() as c:
        return [dict(r) for r in c.execute(q, args).fetchall()]


def get_candidate(name_or_id) -> dict | None:
    """Fetch one candidate by numeric id or partial (case-insensitive) name."""
    with _conn() as c:
        if str(name_or_id).isdigit():
            r = c.execute("SELECT * FROM candidates WHERE id=?", (int(name_or_id),)).fetchone()
        else:
            r = c.execute("SELECT * FROM candidates WHERE lower(name) LIKE ? ORDER BY score DESC",
                          (f"%{str(name_or_id).lower()}%",)).fetchone()
        return dict(r) if r else None


def clear_candidates():
    """Delete all candidates and processed-email markers."""
    with _conn() as c:
        c.execute("DELETE FROM candidates")
        c.execute("DELETE FROM processed_emails")


# ---------- de-duplication memory ----------
def is_processed(source_id: str) -> bool:
    """Return whether a source id has already been handled."""
    with _conn() as c:
        return c.execute("SELECT 1 FROM processed_emails WHERE source_id=?", (source_id,)).fetchone() is not None


def mark_processed(source_id: str, sender: str = "", subject: str = ""):
    """Record a source id as handled so it is not fetched again."""
    with _conn() as c:
        c.execute("INSERT OR IGNORE INTO processed_emails(source_id,sender,subject) VALUES (?,?,?)",
                  (source_id, sender, subject))


# ---------- conversation memory ----------
def add_memory(role: str, content: str):
    """Append a message to the conversation history."""
    with _conn() as c:
        c.execute("INSERT INTO chat_memory(role,content) VALUES (?,?)", (role, content))


def get_memory(limit: int = 12) -> list[dict]:
    """Return the most recent messages in chronological order."""
    with _conn() as c:
        rows = c.execute("SELECT role,content FROM chat_memory ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in reversed(rows)]


def clear_memory():
    """Delete the stored conversation history."""
    with _conn() as c:
        c.execute("DELETE FROM chat_memory")


# ---------- jobs ----------
def save_job(title: str, description: str):
    """Insert or update a job description by title."""
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO jobs(title,description) VALUES (?,?)", (title, description))


def get_jobs() -> list[dict]:
    """Return all configured jobs, newest first."""
    with _conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM jobs ORDER BY id DESC").fetchall()]


def get_job(title: str) -> dict | None:
    """Return one job by exact title, or None."""
    with _conn() as c:
        r = c.execute("SELECT * FROM jobs WHERE title=?", (title,)).fetchone()
        return dict(r) if r else None


# ---------- drafts (outbound email) ----------
def save_draft(to: str, subject: str, body: str, cc: str = "", candidate_id=None) -> dict:
    """Persist a pending outbound email draft and return its id."""
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO drafts(to_addr,cc_addr,subject,body,candidate_id) VALUES (?,?,?,?,?)",
            (to, cc, subject, body, candidate_id))
        did = cur.lastrowid
    return {"draft_id": did, "to": to, "subject": subject, "body": body, "status": "pending"}


def get_draft(draft_id) -> dict | None:
    """Return one draft by id, or None."""
    with _conn() as c:
        r = c.execute("SELECT * FROM drafts WHERE id=?", (int(draft_id),)).fetchone()
        return dict(r) if r else None


def list_drafts(status: str | None = None) -> list[dict]:
    """Return drafts, optionally filtered by status, newest first."""
    q, args = "SELECT * FROM drafts", []
    if status:
        q += " WHERE status=?"
        args.append(status)
    q += " ORDER BY id DESC"
    with _conn() as c:
        return [dict(r) for r in c.execute(q, args).fetchall()]


def mark_draft_sent(draft_id):
    """Mark a draft as sent and record the send time."""
    with _conn() as c:
        c.execute("UPDATE drafts SET status='sent', sent_at=CURRENT_TIMESTAMP WHERE id=?", (int(draft_id),))


def mark_draft_failed(draft_id, error: str = ""):
    """Mark a draft as failed and store the error text."""
    with _conn() as c:
        c.execute("UPDATE drafts SET status='failed', error=? WHERE id=?", (error, int(draft_id)))
