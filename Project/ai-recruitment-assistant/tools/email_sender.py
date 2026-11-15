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
