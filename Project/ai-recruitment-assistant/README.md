# AI Recruitment Assistant

An agentic recruitment assistant built with Python and Streamlit for an Artificial Intelligence semester project. The app reads an inbox, extracts resumes, scores candidates against a hiring rubric, ranks the shortlist, and can draft and send email to candidates after the user confirms.

The assistant is not a fixed pipeline. It is a tool-calling agent driven by a language model. The model decides which tool to call next, reads the result, and repeats until it has an answer. The same chat can screen applications, answer ordinary inbox questions, discuss the leaderboard, and send mail.

## Features

- **Agentic screening.** The model chooses the order of work: fetch mail, retrieve the rubric, parse resumes, evaluate candidates, save results, and rank them.
- **On-demand inbox access.** Gmail is checked only when you ask. There is no background poller and no scheduler.
- **Two email sources.** A real Gmail inbox over IMAP, or a local folder of `.eml` files for demos without credentials.
- **Resume parsing.** PDF, DOCX, TXT, and Markdown resumes through `pypdf` and `python-docx`.
- **Retrieval-augmented scoring.** Hiring documents in `knowledge/*.md` are chunked and searched with TF-IDF cosine similarity. The top passages are injected into every evaluation prompt.
- **Bounded, explainable scores.** The LLM proposes sub-scores for skills (50), experience (35), and education (15). Python clamps each value and computes the total. Every candidate gets strengths, weaknesses, missing skills, a justification, and a recommendation.
- **Persistent memory.** SQLite stores candidates, processed email IDs, chat history, job descriptions, and outbound drafts.
- **Read-only general inbox search.** Ask "what arrived today?" or "find emails from Amazon" without marking anything as read.
- **Draft-first email sending.** The agent writes a draft, shows the exact subject and body, and sends only after an explicit confirmation. A code-level guard enforces this, not just the prompt.
- **Single and batch sending.** Send one message to one person, the same message to many recipients, or a personalized message per recipient.
- **Explainable UI.** Streamlit chat with a live tool trace, a leaderboard with charts and CSV export, and a knowledge-base viewer.
- **Offline demo mode.** `USE_MOCK_LLM=1` runs the whole pipeline without an API key.

## Architecture at a glance

```
Streamlit UI (app.py)
    |
    v
RecruitmentAgent (agent.py)  <-- ReAct tool-calling loop
    |-- llm.py                  RealLLM or MockLLM
    |-- tools/email_tool.py     IMAP / local .eml reading, read-only inbox search
    |-- tools/parser_tool.py    PDF / DOCX / TXT text extraction
    |-- tools/knowledge_tool.py TF-IDF retrieval over knowledge/*.md
    |-- tools/database.py       SQLite persistence
    |-- tools/email_sender.py   SMTP sending and draft storage
    |
    v
SQLite (data/recruitment.db) and the Gmail IMAP/SMTP boundary
```

The full design is documented in [`docs/PROJECT_REPORT.md`](docs/PROJECT_REPORT.md).

## Project structure

```
ai-recruitment-assistant/
├── app.py                     Streamlit UI: chat, tool trace, leaderboard, knowledge viewer
├── agent.py                   RecruitmentAgent: ReAct loop, tool schemas, confirmation guard
├── llm.py                     RealLLM (OpenAI-compatible) and deterministic MockLLM
├── config.py                  Environment loading and filesystem paths
├── requirements.txt           Python dependencies
├── .env.example               Template for all configuration keys
├── assets/
│   ├── sample_jd.txt          Sample backend engineer job description
│   ├── resumes/               Five sample resume PDFs
│   └── inbox/                 Six sample .eml messages, including one non-application
├── knowledge/
│   ├── hiring_rubric.md       Scoring weights, bands, red flags, fairness rules
│   └── interview_guidelines.md Screening and interview guidance
├── tools/
│   ├── email_tool.py          IMAP and local inbox fetch, read-only inbox search
│   ├── email_sender.py        SMTP send, draft creation, batch send
│   ├── parser_tool.py         Resume text extraction
│   ├── knowledge_tool.py      Chunking, TF-IDF indexing, cosine retrieval
│   └── database.py            SQLite tables and CRUD helpers
├── data/
│   ├── recruitment.db         Runtime database (created automatically)
│   ├── downloads/             Attachments saved from email
│   └── uploads/               Resumes uploaded through the UI
├── scripts/
│   └── make_samples.py        Regenerates sample resumes and the demo inbox
├── tests/
│   ├── test_pipeline.py       Agent, RAG, dedup, IMAP filter, inbox search
│   ├── test_ui.py             Streamlit flow tests
│   └── test_email_sender.py   Drafts, SMTP sending, confirmation guard
└── docs/
    ├── PROJECT_REPORT.md      Formal semester-project report
    └── superpowers/           Design spec and implementation plan
```

## Setup

### 1. Python environment

Python 3.10 or newer is required because the code uses modern type syntax such as `str | None`.

With Anaconda:

```bash
conda create -n ai-recruitment python=3.11 -y
conda activate ai-recruitment
```

Or with the standard library `venv`:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

Install the dependencies from the project root:

```bash
pip install -r requirements.txt
```

The dependencies are `streamlit`, `openai`, `pypdf`, `python-docx`, `python-dotenv`, `pandas`, `reportlab`, and `pytest`.

### 2. Configure `.env`

Copy the template and edit it:

```bash
cp .env.example .env
```

All keys are optional in the sense that the app still starts without them. Without an LLM key it falls back to the offline mock model. Without email credentials it falls back to the local demo inbox.

| Key | Purpose | Default / example |
| --- | --- | --- |
| `LLM_API_KEY` | API key for the OpenAI-compatible provider | empty |
| `LLM_BASE_URL` | Provider base URL; must match the key | empty (OpenAI), `https://integrate.api.nvidia.com/v1` for NVIDIA |
| `LLM_MODEL` | Model name sent to the provider | `gpt-4o-mini` |
| `USE_MOCK_LLM` | Set to `1` to force the offline mock model | `0` |
| `IMAP_SERVER` | Incoming mail server for reading | `imap.gmail.com` |
| `EMAIL_USER` | Full email address used for IMAP and SMTP | empty |
| `EMAIL_PASS` | Gmail app password (spaces are ignored) | empty |
| `SMTP_SERVER` | Outgoing mail server for sending | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP SSL port | `465` |
| `DB_PATH` | SQLite database file | `data/recruitment.db` |

Example `.env` for a Gmail account:

```env
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL=nvidia/nemotron-3.5-lightning-30b-a3b
USE_MOCK_LLM=0

IMAP_SERVER=imap.gmail.com
EMAIL_USER=you@gmail.com
EMAIL_PASS=your-app-password

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

DB_PATH=data/recruitment.db
```

Credentials are read from `.env` only. The UI never asks for secrets.

### 3. Run the app

```bash
streamlit run app.py
```

Streamlit opens the app in your browser, usually at `http://localhost:8501`. The database and required folders are created on first run.

The sample resumes and demo inbox are already included. To regenerate them:

```bash
python scripts/make_samples.py
```

## Usage

### Screen new applications

1. Choose an email source in the sidebar: **Local demo inbox** or **Gmail inbox**.
2. For Gmail, keep **Only process application-looking emails** enabled and set **Max emails to process per check** (default 5 in the UI).
3. Press **Process new applications**, or type `check` or `check inbox` in chat.

The agent fetches unread mail, saves resume attachments, retrieves the hiring rubric, parses each resume, evaluates it, saves the candidate, and returns a ranked shortlist. The raw tool calls are available in expandable steps under each reply.

Application checks read unread messages only. Processed messages are remembered by `Message-ID` or file hash, so a second run does not score the same person twice.

### Ask general inbox questions

The same chat handles ordinary mail questions without running the screening workflow:

- `What emails came in today?`
- `Find emails from Amazon`
- `Summarize the latest email`
- `What's in my inbox?`

These use the read-only `search_inbox` tool. It does not mark messages as read, does not save attachments, and does not run the application pipeline.

### Email a candidate

Ask in plain language:

```text
Email ayesha.khan@example.com and invite her to a technical interview.
```

The agent calls `draft_email`, shows the exact subject and body, and asks you to confirm. Nothing is sent at this point. Reply with an explicit confirmation such as:

```text
send it
```

The agent then calls `send_draft` and reports the result. If the last user message is not a confirmation, the send tool refuses with an error even if the model tries to call it. This is the human-in-the-loop safety gate.

Sending needs `EMAIL_USER`, `EMAIL_PASS`, `SMTP_SERVER`, and `SMTP_PORT` in `.env`. Messages are plain text. Outbound attachments are not supported.

### Batch email

Both batch modes are supported.

**Same message to many recipients.** Give the agent a comma-separated list:

```text
Draft an interview invitation to ayesha.khan@example.com, bilal.ahmed@example.com, and sara.malik@example.com.
```

The agent creates one pending draft with multiple recipients, shows it, and sends it after confirmation.

**Personalized message per recipient.** Name each person and what should differ:

```text
Draft a personalized rejection to usman.tariq@example.com and hina.raza@example.com. Mention their strongest skill, but keep it kind.
```

The agent calls `draft_email` once per person, shows the drafts, then uses `send_batch` with the draft IDs after you confirm.

Pending drafts are also listed in a **Pending drafts** expander in the Agent tab. Draft status (`pending`, `sent`, `failed`) is stored in the `drafts` table in SQLite.

### Review the shortlist

Use the **Leaderboard** tab or ask:

- `Who are the top 3 candidates?`
- `Why did Usman rank below Ayesha?`

The leaderboard shows total and component scores, a stacked bar chart, per-candidate justifications, and a CSV export.

## Running the tests

```bash
python -m pytest -q tests
```

The suite contains 20 tests and is designed to run fully offline. It forces `USE_MOCK_LLM=1`, uses temporary SQLite databases, and mocks SMTP, so no real mail is sent and no API key is needed. Install the dependencies from `requirements.txt` first.

Coverage includes:

- RAG retrieval from the hiring rubric.
- The end-to-end screening run, ranking, conversation memory, and duplicate suppression.
- Application filtering for resume and newsletter emails.
- IMAP credential checks and scanning past non-application messages.
- Short replies such as `check` and `yes` triggering the fetch tool.
- Large tool observations remaining valid JSON.
- Read-only inbox search in local mode.
- The Streamlit flow, including the Gmail warning when credentials are missing.
- Draft persistence, invalid recipient rejection, credential guards, double-send protection, batch counts, and the agent confirmation guard.

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401`, `404`, or `model not found` from the LLM | `LLM_BASE_URL` does not match the provider that issued `LLM_API_KEY`, or the model name is wrong | Use one provider consistently. For NVIDIA set `LLM_BASE_URL=https://integrate.api.nvidia.com/v1` and a model the key can access. For Groq use `https://api.groq.com/openai/v1`. For local Ollama use `http://localhost:11434/v1` with `LLM_API_KEY=ollama`. |
| "I couldn't reach the language model" in chat | Network error, bad base URL, or missing key while mock mode is off | Check the three LLM keys in `.env`, then restart Streamlit. As a quick check, set `USE_MOCK_LLM=1`. |
| Gmail login fails with an authentication error | A normal account password was used, or 2-Step Verification is off | Enable 2-Step Verification, open **Google Account → Security → App passwords**, create a **Mail** app password, and put the 16 characters in `EMAIL_PASS`. Spaces are ignored. Use **Test Gmail connection** in the sidebar. |
| "Gmail isn't configured" warning | `EMAIL_USER` or `EMAIL_PASS` is empty, or the Gmail source is selected without credentials | Fill both keys in `.env` and restart, or switch to **Local demo inbox**. |
| Sending is refused with "Not confirmed" | The last message was not an explicit confirmation | Reply with `send`, `send it`, `send them`, `go ahead`, or `confirm`. The guard is intentional. |
| Sending fails with an SMTP error | Wrong SMTP server or port, or the account blocks SMTP | Keep `SMTP_SERVER=smtp.gmail.com` and `SMTP_PORT=465` for Gmail. Recheck the app password. |
| No candidates appear | No unread mail, no supported attachments, or messages were already processed | Use the local demo inbox for a known-good run. Reset with **Reset candidates & memory** in the sidebar. |
| A scanned PDF yields "No extractable text" | Image-only PDF with no text layer | Use a text-based PDF or DOCX. OCR is not implemented. |
| Want a fully offline demo | No provider or no network | Set `USE_MOCK_LLM=1`. The mock model uses deterministic keyword scoring and scripted tool choices. |

## Design notes

- **The LLM judges, Python computes.** Sub-scores are clamped to their rubric maxima and summed in code, so a model cannot return 140 out of 100.
- **Fairness by prompt and rubric.** The rubric forbids using name, gender, nationality, age, photo, or university prestige as scoring factors.
- **Deduplication.** Processed emails are tracked by `Message-ID` or file hash. Identical tool calls are also detected inside a run and stopped after repeats.
- **Drafts live in SQLite.** Streamlit rebuilds the app on every interaction, so drafts must persist outside memory.
- **On-demand by design.** There is no polling, no scheduling, no background worker, and no outbound attachment handling.
- **Graceful failure.** Tools return error dictionaries instead of raising, so the agent can report a problem and continue with the rest of the batch.

## Course context

This project was built for a 5th-semester Artificial Intelligence course. It demonstrates intelligent agents, the ReAct pattern, LLM tool calling, retrieval-augmented generation, persistent memory, human-in-the-loop safety, and a practical Streamlit interface in one system.
