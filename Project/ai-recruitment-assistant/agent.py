"""Core agent: LLM-driven tool-calling loop (ReAct style).

The agent receives a *goal* in natural language, then repeatedly
  1. asks the LLM what to do next (reasoning),
  2. executes the tool(s) the LLM chose (acting),
  3. feeds the observation back,
until the LLM answers without calling a tool. No fixed script decides the order of steps.
Conversation memory is persisted in SQLite and replayed on each run.
"""
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import config
from llm import get_llm
from tools import database as db
from tools import email_sender
from tools.email_tool import fetch_applicant_emails, search_inbox
from tools.knowledge_tool import search_knowledge
from tools.parser_tool import extract_text_from_resume

SYSTEM_PROMPT = """You are a friendly, experienced technical recruiter talking with a hiring manager. You are also a capable general assistant with a recruiting specialty. Talk like a real person, not like a chatbot or a dashboard.

Voice:
- Use first person, contractions, and plain language.
- Keep replies short: usually 2-5 sentences. Use bullets only when comparing candidates or listing next steps.
- Acknowledge what the person just said before moving on. Greet them back when they greet you.
- Be warm, direct, and a little informal. "I checked the inbox" sounds better than "The fetch tool returned 5 records."
- Never say "As an AI", "I am an autonomous agent", "tool call", or dump raw JSON/tool names. Don't narrate every internal step.
- If the request is ambiguous, ask one short clarifying question. Otherwise, make a sensible call and move on.
- If asked directly whether you are an AI, be honest, but keep the same natural tone.

Your job:
You are a capable general assistant with a recruiting specialty. You can answer ordinary questions, explain things, draft messages, and inspect the user's inbox. Don't force every request into recruitment.

Route the request:
- General knowledge, explanations, and chit-chat: answer directly, no tools.
- Non-application email questions ("what emails did I get today?", "find emails from Amazon", "summarize the latest email", "what's in my inbox?"): use search_inbox (read-only; it never marks mail read or saves attachments).
- Application screening ("process new applications", "check", "yes" after an offer): use the fetch_new_applications workflow below.
- Candidate questions ("who are the top 3?", "why was X rejected?"): use get_leaderboard / get_candidate_details.

Typical workflow for "process new applications":
  1. process_new_applications          -> fetch, read every attached resume, score all candidates, save them, and rank the shortlist in one call
     (the leaderboard is already included in its result, so there is no separate get_leaderboard step)

Granular tools (the fallback for one-off work, e.g. re-scoring a single uploaded resume):
  - fetch_new_applications             -> list of new emails (+ attachment paths)
  - search_knowledge                   -> retrieve the company hiring rubric (once before scoring)
  - for EACH email with a resume: parse_resume -> evaluate_candidate -> save_candidate
    (use skip_email for emails with no usable resume)
  - get_leaderboard                    -> rank everyone and report the result

Rules:
- Never invent candidates or scores; only report what tools returned.
- If a tool returns an error, say so plainly, adapt (skip that file, report it) and continue with the rest.
- When asked to process applications, just do it; don't ask for permission first. If the user says "check", "check now", or "yes" after you offered to check, treat it as "process new applications now".
- Never repeat the same tool call with the same arguments. Use the earlier result and move on. If you catch yourself looping, stop and give a short summary.
- Process every new application before answering. Finish with a short, human summary: what you found, who stands out, and what you'd do next.

Emailing:
- To email anyone, first call draft_email, then show the exact subject and body and ask the user to confirm. Never send in the same turn as drafting.
- Only call send_draft / send_batch after the user explicitly confirms ("send", "send it", "go ahead").
- You may email any address the user names. For the same message to many people, pass a comma-separated list to draft_email. For a personalized batch, call draft_email once per person, then send_batch.
- Never invent recipients; use the addresses the user gave or that a tool returned."""

TOOLS = [
    {"type": "function", "function": {"name": "process_new_applications",
     "description": "Preferred way to process applications: fetches new emails, reads every attached resume, scores each candidate against the job description and hiring rubric IN PARALLEL, saves them, and returns the ranked leaderboard — all in one step. Use this for 'process new applications', 'screen the inbox', or 'check'.",
     "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "fetch_new_applications",
     "description": "Fetch new, not-yet-processed application emails (IMAP inbox or local folder) and uploaded resumes. Saves attachments and returns source_id, sender, subject and attachment paths.",
     "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "search_inbox",
     "description": "Read-only search across the inbox (Gmail or local demo) for general, non-application email questions. Use for 'what arrived today', 'find emails from X', 'summarize the latest email'. Does not mark messages read or save attachments.",
     "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer"},
                    "unread_only": {"type": "boolean"}, "since_days": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "parse_resume",
     "description": "Extract text from a resume file (PDF/DOCX/TXT). Returns a preview and length; the full text is cached for evaluate_candidate.",
     "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "search_knowledge",
     "description": "RAG: search the company knowledge base (hiring rubric, interview guidelines) and return the most relevant passages.",
     "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "k": {"type": "integer"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "evaluate_candidate",
     "description": "Score a parsed resume against the job description and the retrieved hiring rubric using the LLM. Returns sub-scores, total score (0-100), strengths, weaknesses, missing skills and justification. Does not save.",
     "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "source_id": {"type": "string"},
                    "sender": {"type": "string"}}, "required": ["path", "source_id"]}}},
    {"type": "function", "function": {"name": "save_candidate",
     "description": "Persist an evaluated candidate to the database and mark the email as processed (prevents duplicates).",
     "parameters": {"type": "object", "properties": {"source_id": {"type": "string"}}, "required": ["source_id"]}}},
    {"type": "function", "function": {"name": "skip_email",
     "description": "Mark an email without a usable resume as processed so it is not fetched again.",
     "parameters": {"type": "object", "properties": {"source_id": {"type": "string"}, "reason": {"type": "string"}}, "required": ["source_id"]}}},
    {"type": "function", "function": {"name": "get_leaderboard",
     "description": "Return candidates ranked by score (highest first), optionally limited to top N.",
     "parameters": {"type": "object", "properties": {"limit": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "get_candidate_details",
     "description": "Get the full evaluation of one candidate by name (partial ok) or id.",
     "parameters": {"type": "object", "properties": {"name_or_id": {"type": "string"}}, "required": ["name_or_id"]}}},
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
]

WEIGHTS = {"skills_score": 50, "experience_score": 35, "education_score": 15}

ACTION_RE = re.compile(r"\b(process|screen|fetch|review|scan|check)\b|\blook at\b|\bgo through\b", re.I)

# An explicit confirmation from the user, required before anything is sent.
CONFIRM_RE = re.compile(
    r"^\s*(yes|yeah|yep|ok|okay|sure|go ahead|do it|send|send it|send them|"
    r"send now|please send|confirm|go for it)\b", re.I)


def tool_observation(result, limit=12000):
    """Serialize a tool result for the LLM, shrinking oversized payloads gracefully.

    Two shrinking passes keep the payload compact while preserving structure (keys such as
    ``source_id``, ``path`` and ``attachments`` always survive). The output is always valid JSON.
    """
    def shrink(value, max_str, max_items):
        """Recursively truncate strings and collections to keep observations compact."""
        if isinstance(value, str):
            return value[:max_str] + "…" if len(value) > max_str else value
        if isinstance(value, list):
            return [shrink(item, max_str, max_items) for item in value[:max_items]]
        if isinstance(value, dict):
            return {key: shrink(item, max_str, max_items) for key, item in value.items()}
        return value

    raw = json.dumps(result, default=str)
    if len(raw) <= limit:
        return raw
    raw = json.dumps(shrink(result, 600, 15), default=str)
    if len(raw) <= limit:
        return raw
    raw = json.dumps(shrink(result, 250, 10), default=str)
    if len(raw) <= limit:
        return raw
    return json.dumps({"truncated": True, "result": shrink(result, 250, 10)}, default=str)


class RecruitmentAgent:
    """Stateful agent that maps LLM tool calls onto recruitment tools and SQLite."""

    def __init__(
        self,
        job_title: str = "Software Engineer",
        job_description: str = "",
        llm=None,
        *,
        email_user: str | None = None,
        email_password: str | None = None,
        imap_server: str | None = None,
        email_filter_applications: bool = False,
        email_mode: str = "auto",
        email_limit: int = 20,
    ):
        """Configure the agent, its LLM client, email settings, and per-run caches."""
        db.init_db()
        self.llm = llm or get_llm()
        self.job_title = job_title
        self.job_description = job_description or self._default_jd()
        self.email_user = email_user
        self.email_password = email_password
        self.imap_server = imap_server
        self.email_filter_applications = email_filter_applications
        self.email_mode = email_mode
        self.email_limit = email_limit
        self.resume_cache: dict[str, str] = {}
        self.pending: dict[str, dict] = {}
        self._send_confirmed = False
        self._on_token = None
        self._on_step = None

    def _default_jd(self) -> str:
        """Return the stored job description, falling back to the sample or job title."""
        job = db.get_job(self.job_title)
        if job:
            return job["description"]
        sample = config.BASE_DIR / "assets" / "sample_jd.txt"
        return sample.read_text() if sample.exists() else self.job_title

    # ------------------------------------------------------------------ tools
    def _tool_fetch_new_applications(self, **_):
        """Fetch new application emails and uploaded resumes from the configured source."""
        return fetch_applicant_emails(
            user=self.email_user,
            password=self.email_password,
            server=self.imap_server,
            only_applications=self.email_filter_applications,
            mode=self.email_mode,
            limit=self.email_limit,
        )

    def _tool_process_new_applications(self, **_):
        """Fetch new applications, score every attached resume in parallel, save, and rank them."""
        fetched = self._tool_fetch_new_applications()
        emails = fetched.get("emails", [])
        if not emails:
            return {"source": fetched.get("source"), "fetched": 0, "scored": 0, "skipped": 0,
                    "leaderboard": self._tool_get_leaderboard()}
        rubric = self._rubric()
        ready, skipped = [], []
        for e in emails:
            if e.get("attachments"):
                ready.append((e, e["attachments"][0]))
            else:
                skipped.append(e)
        for e in skipped:
            self._tool_skip_email(e["source_id"], "no resume attached")
            self._emit_step("skip_email", {"source_id": e["source_id"]},
                            {"skipped": True, "reason": "no resume attached"})
        processed = []
        if ready:
            workers = max(1, min(config.LLM_EVAL_WORKERS, len(ready)))
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = {
                    pool.submit(self._score_resume, path, e["source_id"], e.get("sender", ""),
                                rubric, stream=False): (e, path)
                    for e, path in ready
                }
                # on_step drives Streamlit and must run on the main thread only; parallel
                # evaluations also must not stream tokens into the single UI placeholder.
                for fut in as_completed(futures):
                    e, path = futures[fut]
                    source_id = e["source_id"]
                    try:
                        ev = fut.result()
                    except Exception as exc:
                        err = {"error": f"{type(exc).__name__}: {exc}", "source_id": source_id}
                        self._emit_step("evaluate_candidate",
                                        {"source_id": source_id, "path": path}, err)
                        continue
                    self.pending[source_id] = ev
                    saved = self._tool_save_candidate(source_id)
                    self._emit_step("evaluate_candidate", {"source_id": source_id, "path": path},
                                    {k: ev[k] for k in ("name", "score", "recommendation")})
                    processed.append({**ev, **saved})
        return {"source": fetched.get("source"), "fetched": len(emails), "scored": len(processed),
                "skipped": len(skipped), "leaderboard": self._tool_get_leaderboard()}

    def _tool_search_inbox(self, query="", limit=5, unread_only=False, since_days=0, **_):
        """Search the inbox read-only for general, non-application email questions."""
        return search_inbox(
            query=query, limit=limit, unread_only=unread_only, since_days=since_days,
            user=self.email_user, password=self.email_password,
            server=self.imap_server, mode=self.email_mode,
        )

    def _tool_parse_resume(self, path, **_):
        """Extract resume text, cache it, and return a short preview for the LLM."""
        text = extract_text_from_resume(path)
        self.resume_cache[path] = text
        return {"path": path, "characters": len(text), "preview": text[:300]}

    def _tool_search_knowledge(self, query, k=3, **_):
        """Retrieve the most relevant knowledge-base passages for a query."""
        return search_knowledge(query, k)

    def _rubric(self) -> str:
        """Retrieve and join the hiring-rubric passages relevant to this job."""
        results = search_knowledge(
            f"{self.job_title} scoring weights skills experience education fairness", 3)["results"]
        return "\n\n".join(r["text"] for r in results)

    def _score_resume(self, path, source_id, sender, rubric, *, stream) -> dict:
        """Parse and score one resume against the job description and rubric; return the full eval."""
        text = self.resume_cache.get(path) or extract_text_from_resume(path)
        self.resume_cache[path] = text
        prompt = f"""Evaluate the candidate against the job description using the company rubric.

HIRING RUBRIC (retrieved from knowledge base):
{rubric}

JOB DESCRIPTION ({self.job_title}):
{self.job_description}

RESUME:
{text[:5000]}

Return ONLY JSON with keys: name (string), email (string), skills_score (0-50), experience_score (0-35),
education_score (0-15), strengths (list of strings), weaknesses (list of strings),
missing_skills (list of strings), justification (2-3 sentences citing resume evidence)."""
        msgs = [{"role": "system", "content": "You are a fair, evidence-based technical recruiter. Output valid JSON only."},
                {"role": "user", "content": prompt}]
        ev = None
        for _ in range(2):  # one retry on malformed JSON
            raw = self.llm.chat(msgs, json_mode=True, max_tokens=900,
                                on_token=self._on_token if stream else None)["content"]
            try:
                ev = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
                break
            except Exception:
                msgs.append({"role": "user", "content": "That was not valid JSON. Return only the JSON object."})
        if ev is None:
            raise ValueError("LLM did not return valid JSON")
        for k, mx in WEIGHTS.items():  # clamp: LLM judges components, code computes the total
            ev[k] = max(0.0, min(float(ev.get(k, 0) or 0), mx))
        ev["score"] = round(sum(ev[k] for k in WEIGHTS), 1)
        ev["recommendation"] = ("Strong hire - technical interview" if ev["score"] >= 80 else
                                "Potential - phone screen" if ev["score"] >= 60 else
                                "Weak - keep on file" if ev["score"] >= 40 else "Reject")
        if not ev.get("email"):
            m = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", sender)
            ev["email"] = m.group(0) if m else ""
        ev.update(job_title=self.job_title, resume_path=path, source_id=source_id)
        return ev

    def _tool_evaluate_candidate(self, path, source_id, sender="", **_):
        """Score a cached resume against the job description and hiring rubric via the LLM."""
        ev = self._score_resume(path, source_id, sender, self._rubric(), stream=True)
        self.pending[source_id] = ev
        return {k: ev[k] for k in ("name", "score", "skills_score", "experience_score", "education_score",
                                   "recommendation", "strengths", "weaknesses", "missing_skills", "justification")}

    def _tool_save_candidate(self, source_id, **_):
        """Persist a pending evaluation and mark the source email as processed."""
        if source_id not in self.pending:
            return {"error": "No evaluation pending for this source_id. Call evaluate_candidate first."}
        ev = self.pending.pop(source_id)
        res = db.save_candidate(ev)
        db.mark_processed(source_id, ev.get("email", ""), ev.get("job_title", ""))
        return {**res, "name": ev["name"], "score": ev["score"]}

    def _tool_skip_email(self, source_id, reason="", **_):
        """Mark an email without a usable resume as processed."""
        db.mark_processed(source_id, "", f"skipped: {reason}")
        return {"skipped": True, "reason": reason}

    def _tool_get_leaderboard(self, limit=None, **_):
        """Return candidates for this job ranked by score."""
        rows = db.get_ranked_candidates(self.job_title, limit)
        return {"count": len(rows), "candidates": [
            {"rank": i, "id": r["id"], "name": r["name"], "email": r["email"], "score": r["score"],
             "recommendation": r["recommendation"]} for i, r in enumerate(rows, 1)]}

    def _tool_get_candidate_details(self, name_or_id, **_):
        """Look up one candidate by id or partial name."""
        r = db.get_candidate(name_or_id)
        return r or {"error": f"No candidate matching '{name_or_id}'"}

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

    # ------------------------------------------------------------------ loop
    def _emit_step(self, tool, args, result):
        """Send an extra timeline event (not a trace entry) to the UI callback."""
        if self._on_step:
            self._on_step({"step": 0, "tool": tool, "args": args, "result": result})

    def _execute(self, name, args):
        """Dispatch a tool call by name, converting exceptions into observations."""
        fn = getattr(self, f"_tool_{name}", None)
        if not fn:
            return {"error": f"Unknown tool {name}"}
        try:
            return fn(**args)
        except Exception as e:  # observation, not a crash: the agent can adapt
            return {"error": f"{type(e).__name__}: {e}"}

    def run(self, goal: str, on_step=None, on_token=None) -> dict:
        """Run the agent on a natural-language goal. Returns {'answer', 'trace'}."""
        self._on_token = on_token
        self._on_step = on_step
        memory = db.get_memory(10)
        action_request = bool(ACTION_RE.search(goal))
        self._send_confirmed = bool(CONFIRM_RE.search(goal))
        messages = [{"role": "system", "content": SYSTEM_PROMPT + f"\n\nActive job: {self.job_title}"}]
        if action_request:
            messages.append({"role": "system", "content": "This is an action request. Use tools now; do not ask for permission or just describe a plan. Start with the most relevant tool."})
        messages += memory + [{"role": "user", "content": goal}]
        trace = []
        answer = ""
        nudged = False
        seen: dict[tuple[str, str], int] = {}
        duplicate_errors = 0
        for step in range(config.MAX_AGENT_STEPS):
            msg = self.llm.chat(messages, tools=TOOLS, max_tokens=700, on_token=on_token)
            messages.append(msg)
            calls = msg.get("tool_calls")
            if not calls:
                if action_request and not trace and not nudged:
                    nudged = True
                    messages.append({"role": "system", "content": "You replied without calling a tool. This is an action request: call the right tool now instead of chatting about it."})
                    continue
                answer = msg["content"]
                break
            for tc in calls:
                name = tc["function"]["name"]
                try:
                    args = json.loads(tc["function"]["arguments"] or "{}")
                except json.JSONDecodeError:
                    args = {}
                signature = (name, json.dumps(args, sort_keys=True))
                if seen.get(signature, 0) >= 2:
                    result = {"error": "This exact tool call already ran. Use the earlier result and move on."}
                    duplicate_errors += 1
                else:
                    result = self._execute(name, args)
                    seen[signature] = seen.get(signature, 0) + 1
                entry = {"step": len(trace) + 1, "tool": name, "args": args, "result": result}
                trace.append(entry)
                if on_step:
                    on_step(entry)
                messages.append({"role": "tool", "tool_call_id": tc["id"],
                                 "content": tool_observation(result)})
            if duplicate_errors >= 3:
                messages.append({"role": "system", "content": "You are repeating the same tool calls. Stop using tools and give the user a short summary of what you already found."})
                final = self.llm.chat(messages, tools=None, max_tokens=700, on_token=on_token)
                if not final.get("tool_calls"):
                    answer = final.get("content") or "I stopped because I was repeating the same step. Want me to continue?"
                else:
                    answer = "I stopped because I was repeating the same step. Want me to continue from here?"
                break
        else:
            answer = "I got partway through and hit my step limit. Want me to continue with the rest?"
        db.add_memory("user", goal)
        db.add_memory("assistant", answer)
        return {"answer": answer, "trace": trace}
