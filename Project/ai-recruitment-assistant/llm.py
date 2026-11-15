"""LLM access layer.

`get_llm()` returns an object with  chat(messages, tools=None, json_mode=False) -> assistant message dict.
 * RealLLM : any OpenAI-compatible endpoint (OpenAI, Groq, Ollama, Together, ...)
 * MockLLM : deterministic offline stand-in so the whole pipeline can be demoed/tested without an API key.
"""
import json
import re
import uuid

import config


def _assemble_stream(chunks, on_token=None):
    """Assemble OpenAI-style streamed chunks into one normalized assistant message.

    Content deltas are concatenated (and forwarded to ``on_token`` as they arrive).
    Tool-call deltas are merged by ``index`` into complete ``{id, type, function}`` entries.
    """
    content_parts = []
    tool_calls = {}
    for chunk in chunks:
        choices = getattr(chunk, "choices", None)
        if not choices:
            continue
        delta = getattr(choices[0], "delta", None)
        if delta is None:
            continue
        piece = getattr(delta, "content", None)
        if piece:
            content_parts.append(piece)
            if on_token is not None:
                on_token(piece)
        for tc_delta in getattr(delta, "tool_calls", None) or []:
            idx = getattr(tc_delta, "index", 0)
            idx = 0 if idx is None else idx
            slot = tool_calls.setdefault(
                idx, {"id": "", "type": "function", "function": {"name": "", "arguments": ""}}
            )
            if getattr(tc_delta, "id", None):
                slot["id"] = tc_delta.id
            fn = getattr(tc_delta, "function", None)
            if fn is not None:
                if getattr(fn, "name", None):
                    slot["function"]["name"] += fn.name
                if getattr(fn, "arguments", None):
                    slot["function"]["arguments"] += fn.arguments
    out = {"role": "assistant", "content": "".join(content_parts)}
    if tool_calls:
        out["tool_calls"] = [tool_calls[i] for i in sorted(tool_calls)]
    return out


class RealLLM:
    """OpenAI-compatible chat client backed by the `openai` package."""

    name = "real"

    def __init__(self):
        """Create the SDK client from the configured API key, base URL, and model."""
        from openai import OpenAI
        self.client = OpenAI(api_key=config.LLM_API_KEY or "none", base_url=config.LLM_BASE_URL)
        self.model = config.LLM_MODEL

    def chat(self, messages, tools=None, json_mode=False, max_tokens=None, on_token=None):
        """Send a chat completion request and normalize the assistant message."""
        kw = {"model": self.model, "messages": messages, "temperature": 0.1 if json_mode else 0.35}
        if config.LLM_DISABLE_THINKING:
            # vLLM/NIM flag: skip the model's chain-of-thought (much faster, non-empty content).
            kw["extra_body"] = {"chat_template_kwargs": {"enable_thinking": False,
                                                         "force_nonempty_content": True}}
        if tools:
            kw["tools"] = tools
            kw["tool_choice"] = "auto"
        if json_mode:
            kw["response_format"] = {"type": "json_object"}
        if max_tokens is not None:
            kw["max_tokens"] = max_tokens
        if on_token is not None:
            kw["stream"] = True
            return _assemble_stream(self.client.chat.completions.create(**kw), on_token)
        m = self.client.chat.completions.create(**kw).choices[0].message
        out = {"role": "assistant", "content": m.content or ""}
        if m.tool_calls:
            out["tool_calls"] = [{"id": t.id, "type": "function",
                                  "function": {"name": t.function.name, "arguments": t.function.arguments}}
                                 for t in m.tool_calls]
        return out


# --------------------------------------------------------------------------- mock
SKILLS = ["python", "django", "flask", "fastapi", "sql", "postgresql", "docker", "kubernetes", "aws",
          "git", "rest", "api", "machine learning", "pytorch", "testing", "pytest", "javascript",
          "react", "linux", "ci/cd", "redis", "microservices"]


class MockLLM:
    """Deterministic offline stand-in for RealLLM used in demos and tests."""

    name = "mock"

    def chat(self, messages, tools=None, json_mode=False, max_tokens=None, on_token=None):
        """Answer with scripted tool calls or an evaluation JSON depending on the mode.

        ``max_tokens`` and ``on_token`` are accepted for interface compatibility and ignored,
        except that ``on_token`` is optionally fired once with the final content.
        """
        msg = ({"role": "assistant", "content": json.dumps(self._evaluate(messages))}
               if json_mode else self._act(messages))
        if on_token is not None and msg.get("content"):
            on_token(msg["content"])
        return msg

    # --- evaluation by keyword overlap (stand-in for semantic judgement)
    def _evaluate(self, messages):
        """Score a resume by keyword overlap and return evaluation JSON fields."""
        text = messages[-1]["content"]
        jd = text.split("JOB DESCRIPTION", 1)[-1].split("\nRESUME:\n", 1)[0].lower()
        resume = text.split("\nRESUME:\n", 1)[-1]
        rl = resume.lower()
        wanted = [s for s in SKILLS if s in jd] or SKILLS[:8]
        have = [s for s in wanted if s in rl]
        missing = [s for s in wanted if s not in rl]
        yrs = [int(x) for x in re.findall(r"(\d+)\+?\s*years", rl)]
        years = max(yrs) if yrs else 0
        edu = 15 if re.search(r"(bs|bsc|b\.sc|bachelor|master)[^\n]*(computer|software|information tech|bscs|bsit|engineering)|bscs|bsit", rl) else 6
        relevance = min(1.0, 2 * len(have) / max(len(wanted), 1))  # experience only counts if relevant
        name = next((l.strip() for l in resume.splitlines() if l.strip() and len(l.split()) <= 4), "Unknown")
        em = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", resume)
        return {"name": name, "email": em.group(0) if em else "",
                "skills_score": round(50 * len(have) / max(len(wanted), 1), 1),
                "experience_score": round(min(35, years * 7) * relevance, 1),
                "education_score": edu,
                "strengths": [f"Covers required skills: {', '.join(have[:6]) or 'none'}",
                              f"About {years} years of stated experience"],
                "weaknesses": [f"Missing: {', '.join(missing[:5])}"] if missing else ["No major gaps"],
                "missing_skills": missing[:8],
                "justification": f"Matched {len(have)}/{len(wanted)} required skills; {years} yrs experience."}

    # --- scripted planner that reacts to tool results (stand-in for LLM reasoning)
    def _act(self, messages):
        """Choose the next tool call or final reply from the conversation so far."""
        last_user = max(i for i, m in enumerate(messages) if m["role"] == "user")
        goal = messages[last_user]["content"].lower()
        calls, results = [], []
        for m in messages[last_user + 1:]:
            if m["role"] == "assistant":
                for tc in m.get("tool_calls", []):
                    calls.append((tc["function"]["name"], json.loads(tc["function"]["arguments"] or "{}")))
            elif m["role"] == "tool":
                results.append(m["content"])
        done = {(n, json.dumps(a, sort_keys=True)) for n, a in calls}
        names = [n for n, _ in calls]

        def call(name, args):
            """Build an assistant message that requests one tool call."""
            return {"role": "assistant", "content": "", "tool_calls": [{
                "id": "call_" + uuid.uuid4().hex[:8], "type": "function",
                "function": {"name": name, "arguments": json.dumps(args)}}]}

        def say(t):
            """Build a plain assistant text message."""
            return {"role": "assistant", "content": t}

        if not re.search(r"process|screen|fetch|evaluate|application|rank|top", goal):
            if re.search(r"^(hi|hello|hey|salam|assalam|good morning|good afternoon|good evening)\b", goal):
                return say("Hey! Good to see you. Want me to check the new applications, or talk through the current shortlist?")
            if re.search(r"^(thanks|thank you|shukriya)\b", goal):
                return say("Anytime. Want me to keep going with the inbox or look at the rankings?")
            if re.search(r"how are you", goal):
                return say("Doing well, thanks — ready to dig into the shortlist. What do you need?")
            if re.search(r"what can you do|what do you do|how can you help", goal):
                return say("I can check your inbox, read resumes, score people against the hiring rubric, and talk you through the shortlist. Want me to start with the inbox?")
            if re.search(r"who are you|your name", goal):
                return say("I'm your recruiting partner for this role — I help you cut through the inbox and focus on the strongest people. Want me to check what's new?")

        if re.search(r"\bwhy\b", goal) and re.search(r"\b(rank|ranked|below|behind|score|reject)\b", goal):
            named = re.search(r"[Ww]hy (?:is|was) ([A-Z][\w'-]+(?: [A-Z][\w'-]+)?)", messages[last_user]["content"])
            if named:
                name = named.group(1)
                if "get_leaderboard" not in names:
                    return call("get_leaderboard", {})
                if "get_candidate_details" not in names:
                    return call("get_candidate_details", {"name_or_id": name})
                board = json.loads(results[names.index("get_leaderboard")])
                details = json.loads(results[names.index("get_candidate_details")])
                if "error" in details:
                    return say(f"I couldn't find {name} in the shortlist. Want me to pull up the current rankings?")
                others = [c for c in board.get("candidates", []) if c["name"].lower() != details["name"].lower()]
                compare = f"{details['name']} is at {details['score']}/100"
                if others:
                    compare += f"; {others[0]['name']} is at {others[0]['score']}/100"
                return say(f"{compare}. {details.get('justification', '')} Want me to walk through the scoring?")

        check_action = re.search(r"^(check|check now|check it|check inbox|check the inbox|check email|check emails|check new applications|check new emails)(?: please)?[.! ]*$|^(yes|yeah|yep|sure|ok|okay|go ahead|go for it|do it|please do)$", goal)
        general_email = (re.search(r"\b(email|emails|mail|inbox|messages?)\b", goal)
                         and not re.search(r"process|screen|fetch|evaluate|application|resume|cv|candidate|rank|top", goal)
                         and not check_action)
        if general_email:
            if "search_inbox" not in names:
                found = re.search(r"(?:from|about|regarding|mentioning|subject)\s+([^\n?]+)", messages[last_user]["content"], re.I)
                q = found.group(1).strip()[:80] if found else ""
                since_days = 1 if "today" in goal else 2 if "yesterday" in goal else 7 if "this week" in goal else 30 if "this month" in goal else 0
                limit = 1 if re.search(r"latest|last|most recent", goal) else 5
                return call("search_inbox", {"query": q, "limit": limit, "since_days": since_days})
            result = json.loads(results[names.index("search_inbox")])
            if result.get("error"):
                return say(f"I couldn't search your inbox just now: {result['error']}")
            emails = result.get("emails", [])
            if not emails:
                return say("I looked, but I didn't find anything matching that.")
            lines = [f"• {e['subject']} — {e['sender']}" for e in emails]
            return say("Here's what I found:\n" + "\n".join(lines) + "\n\nWant me to open any of them?")

        ranking_question = re.search(r"top|best|rank|who|compare|candidate|shortlist|leaderboard", goal)
        email_action = re.search(r"process|screen|fetch|new (applic|email)|evaluate|\bcheck\b|\binbox\b|^(yes|yeah|yep|sure|ok|okay|go ahead|go for it|do it|please do)\b", goal)
        if email_action and (not ranking_question or re.search(r"process|screen|fetch|evaluate", goal)):
            if "fetch_new_applications" not in names:
                return call("fetch_new_applications", {})
            fetched = next(json.loads(r) for (n, _), r in zip(calls, results) if n == "fetch_new_applications")
            for e in fetched.get("emails", []):
                if not e["attachments"]:
                    a = {"source_id": e["source_id"], "reason": "no resume attached"}
                    if ("skip_email", json.dumps(a, sort_keys=True)) not in done:
                        return call("skip_email", a)
                    continue
                path = e["attachments"][0]
                for n, a in (("search_knowledge", {"query": "scoring rubric skills experience education"}),
                             ("parse_resume", {"path": path}),
                             ("evaluate_candidate", {"path": path, "source_id": e["source_id"], "sender": e["sender"]}),
                             ("save_candidate", {"source_id": e["source_id"]})):
                    if n == "search_knowledge" and "search_knowledge" in names:
                        continue
                    if (n, json.dumps(a, sort_keys=True)) not in done:
                        return call(n, a)
            if "get_leaderboard" not in names:
                return call("get_leaderboard", {"limit": 5})
            board = json.loads(results[names.index("get_leaderboard")])
            lines = [f"{i}. {c['name']} - {c['score']}/100" for i, c in enumerate(board.get("candidates", []), 1)]
            count = fetched.get("count", 0)
            intro = (f"I went through {count} new email{'s' if count != 1 else ''}. "
                     if count else "I checked the inbox — nothing new that needs scoring. ")
            if not lines:
                return say(intro + "I don't have anyone on the shortlist yet.")
            return say(intro + "Here's how they stack up:\n" + "\n".join(lines) + "\n\nWant me to dig into anyone?")
        if re.search(r"top|best|rank|who|compare|candidate", goal):
            if "get_leaderboard" not in names:
                m = re.search(r"top (\d+)", goal)
                return call("get_leaderboard", {"limit": int(m.group(1)) if m else 5})
            board = json.loads(results[names.index("get_leaderboard")])
            lines = [f"{i}. {c['name']} - {c['score']}/100" for i, c in enumerate(board.get("candidates", []), 1)]
            if not lines:
                return say("I don't have anyone scored yet. Want me to check the inbox first?")
            return say("Here's the current shortlist:\n" + "\n".join(lines) + "\n\nWant me to compare a couple of them?")
        return say("I can answer that best when a live model is connected. In this offline demo I can still search your inbox, summarize emails, and screen applications — want me to look something up in your inbox?")


def get_llm():
    """Return the configured real LLM, or the mock when offline or unconfigured."""
    if config.USE_MOCK_LLM or (not config.LLM_API_KEY and not config.LLM_BASE_URL):
        return MockLLM()
    return RealLLM()
