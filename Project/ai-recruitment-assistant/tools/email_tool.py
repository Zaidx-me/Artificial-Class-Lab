"""Tool 1: email fetcher.

Two sources, same output:
  * Gmail/IMAP (real inbox) when credentials are supplied by the UI or .env
  * a local folder of .eml files (assets/inbox) - handy for demos & viva without credentials
Already-processed messages (by Message-ID) are skipped -> memory against duplicates.

Processing is always on-demand: this module never starts a background poller.
"""
import email
import hashlib
import imaplib
import re
from datetime import date, datetime, timedelta
from email import policy
from pathlib import Path

import config
from tools import database as db

ALLOWED = (".pdf", ".docx", ".txt")

APPLICATION_KEYWORDS = (
    "application", "apply", "applying", "resume", "cv", "curriculum vitae",
    "candidate", "job", "position", "role", "internship", "hiring",
)


def _connect(user: str, password: str, server: str) -> imaplib.IMAP4_SSL:
    """Open an authenticated, read-only IMAP connection to the inbox."""
    mail = imaplib.IMAP4_SSL(server, timeout=30)
    mail.login(user, password)
    mail.select("inbox", readonly=True)
    return mail


def _save_attachments(msg, source_id: str) -> list[str]:
    """Save supported attachments from a message and return their paths."""
    config.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for part in msg.walk():
        fn = part.get_filename()
        if fn and fn.lower().endswith(ALLOWED):
            safe = re.sub(r"[^\w.\-]", "_", fn)
            tag = hashlib.md5(source_id.encode()).hexdigest()[:6]
            path = config.DOWNLOAD_DIR / f"{tag}_{safe}"
            path.write_bytes(part.get_payload(decode=True) or b"")
            paths.append(str(path))
    return paths


def _body(msg) -> str:
    """Return the plain-text body of a message, or an empty string on failure."""
    try:
        part = msg.get_body(preferencelist=("plain",))
        return part.get_content() if part else ""
    except Exception:
        return ""


def _attachment_names(msg) -> list[str]:
    """List the filenames of all attachments on a message."""
    return [name for part in msg.walk() if (name := part.get_filename())]


def _looks_like_application(msg, body: str | None = None) -> bool:
    """Heuristically decide whether a message is a job application."""
    if any(name.lower().endswith(ALLOWED) for name in _attachment_names(msg)):
        return True
    text = f"{msg.get('Subject', '')}\n{_body(msg) if body is None else body}".lower()
    return any(keyword in text for keyword in APPLICATION_KEYWORDS)


def _handle(msg, fallback_id: str, only_applications: bool = False) -> dict | None:
    """Turn one message into an email record, skipping processed or irrelevant mail."""
    source_id = (msg.get("Message-ID") or fallback_id).strip()
    if db.is_processed(source_id):
        return None
    body = _body(msg)
    if only_applications and not _looks_like_application(msg, body):
        return None
    return {"source_id": source_id, "sender": str(msg.get("From", "")),
            "subject": str(msg.get("Subject", "")), "body": body[:1500],
            "attachments": _save_attachments(msg, source_id)}


def check_imap_connection(user: str, password: str, server: str = "imap.gmail.com") -> dict:
    """Verify Gmail/IMAP credentials without fetching any messages."""
    user = (user or "").strip()
    password = (password or "").replace(" ", "").strip()
    server = (server or config.IMAP_SERVER).strip()
    if not user or not password:
        return {"ok": False, "error": "Gmail address and app password are required."}
    mail = None
    try:
        mail = imaplib.IMAP4_SSL(server, timeout=15)
        mail.login(user, password)
        mail.select("inbox", readonly=True)
        return {"ok": True, "message": f"Connected to {user} via {server}."}
    except imaplib.IMAP4.error as exc:
        return {"ok": False, "error": f"IMAP login failed: {exc}"}
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    finally:
        if mail is not None:
            try:
                mail.logout()
            except Exception:
                pass


def fetch_applicant_emails(
    limit: int = 20,
    *,
    user: str | None = None,
    password: str | None = None,
    server: str | None = None,
    only_applications: bool = False,
    mode: str = "auto",
) -> dict:
    """Fetch NEW (not yet processed) application emails. Returns {'source', 'emails': [...]}."""
    if mode not in {"auto", "local", "imap"}:
        raise ValueError(f"Unknown email mode: {mode}")
    emails = []
    scanned = 0
    user = (user if user is not None else config.EMAIL_USER).strip()
    password = (password if password is not None else config.EMAIL_PASS).replace(" ", "").strip()
    server = (server or config.IMAP_SERVER).strip()
    use_imap = mode == "imap" or (mode == "auto" and bool(user and password))
    if use_imap and not (user and password):
        raise ValueError("Gmail address and app password are required for Gmail mode.")

    if use_imap:
        source = f"Gmail IMAP ({user}) - unread only"
        mail = _connect(user, password, server)
        try:
            _, data = mail.search(None, "(UNSEEN)")
            numbers = data[0].split() if data and data[0] else []
            for num in numbers:
                if len(emails) >= limit:
                    break
                scanned += 1
                _, fetched = mail.fetch(num, "(RFC822)")
                if not fetched or not fetched[0] or not isinstance(fetched[0], tuple):
                    continue
                msg = email.message_from_bytes(fetched[0][1], policy=policy.default)
                item = _handle(msg, f"imap-{num.decode()}", only_applications)
                if item:
                    emails.append(item)
        finally:
            try:
                mail.logout()
            except Exception:
                pass
    else:
        source = f"local folder {config.INBOX_DIR}"
        for f in sorted(Path(config.INBOX_DIR).glob("*.eml")):
            if len(emails) >= limit:
                break
            scanned += 1
            msg = email.message_from_bytes(f.read_bytes(), policy=policy.default)
            item = _handle(msg, f"file-{f.name}", only_applications)
            if item:
                emails.append(item)

    config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for f in sorted(config.UPLOAD_DIR.iterdir()):
        if f.suffix.lower() in ALLOWED:
            sid = "upload-" + hashlib.md5(f.read_bytes()).hexdigest()
            if not db.is_processed(sid):
                emails.append({"source_id": sid, "sender": "uploaded via dashboard", "subject": f.name,
                               "body": "", "attachments": [str(f)]})
    return {"source": source + " + uploads", "count": len(emails), "scanned": scanned, "emails": emails}


def search_inbox(
    limit: int = 5,
    *,
    query: str = "",
    user: str | None = None,
    password: str | None = None,
    server: str | None = None,
    unread_only: bool = False,
    since_days: int = 0,
    mode: str = "auto",
) -> dict:
    """Read-only search across the inbox for general, non-application questions."""
    if mode not in {"auto", "local", "imap"}:
        raise ValueError(f"Unknown email mode: {mode}")
    user = (user if user is not None else config.EMAIL_USER).strip()
    password = (password if password is not None else config.EMAIL_PASS).replace(" ", "").strip()
    server = (server or config.IMAP_SERVER).strip()
    use_imap = mode == "imap" or (mode == "auto" and bool(user and password))
    if use_imap and not (user and password):
        raise ValueError("Gmail address and app password are required for Gmail mode.")

    limit = max(1, min(int(limit), 20))
    query = (query or "").strip()[:200]
    results: list[dict] = []

    if use_imap:
        source = f"Gmail IMAP ({user}) - read-only search"
        criteria = []
        if unread_only:
            criteria.append("UNSEEN")
        if since_days > 0:
            fmt = (date.today() - timedelta(days=since_days)).strftime("%d-%b-%Y")
            criteria.append(f"SINCE {fmt}")
        if query:
            safe = re.sub(r'[\\"]', " ", query)
            criteria.append(f'TEXT "{safe}"')
        search_arg = "(" + " ".join(criteria) + ")" if criteria else "ALL"
        mail = _connect(user, password, server)
        try:
            _, data = mail.search(None, search_arg)
            numbers = data[0].split() if data and data[0] else []
            for num in reversed(numbers[-limit:]):
                _, fetched = mail.fetch(num, "(RFC822)")
                if not fetched or not fetched[0] or not isinstance(fetched[0], tuple):
                    continue
                msg = email.message_from_bytes(fetched[0][1], policy=policy.default)
                results.append({
                    "source_id": f"imap-{num.decode()}",
                    "sender": str(msg.get("From", "")),
                    "subject": str(msg.get("Subject", "")),
                    "date": str(msg.get("Date", "")),
                    "body": _body(msg)[:1500],
                    "attachments": _attachment_names(msg),
                })
        finally:
            try:
                mail.logout()
            except Exception:
                pass
    else:
        source = f"local folder {config.INBOX_DIR} - read-only search"
        cutoff = datetime.now() - timedelta(days=since_days) if since_days > 0 else None
        files = sorted(Path(config.INBOX_DIR).glob("*.eml"),
                       key=lambda p: p.stat().st_mtime, reverse=True)
        for f in files:
            if len(results) >= limit:
                break
            mtime = f.stat().st_mtime
            if cutoff is not None and datetime.fromtimestamp(mtime) < cutoff:
                continue
            msg = email.message_from_bytes(f.read_bytes(), policy=policy.default)
            body = _body(msg)
            text = f"{msg.get('From', '')}\n{msg.get('Subject', '')}\n{body}".lower()
            if query and query.lower() not in text:
                continue
            results.append({
                "source_id": f"file-{f.name}",
                "sender": str(msg.get("From", "")),
                "subject": str(msg.get("Subject", "")),
                "date": str(msg.get("Date", "") or datetime.fromtimestamp(mtime).isoformat(timespec="seconds")),
                "body": body[:1500],
                "attachments": _attachment_names(msg),
            })

    return {"source": source, "count": len(results), "query": query, "emails": results}
