"""Tool 4 (RAG): retrieve hiring guidelines from the local knowledge base.

Documents in knowledge/*.md are split into chunks (by heading) and indexed with a
small TF-IDF vector model (pure Python, no external service). `search_knowledge`
returns the top-k chunks by cosine similarity, which the agent injects into the
evaluation prompt so scoring stays consistent with company policy.
"""
import math
import re
from collections import Counter
from functools import lru_cache

import config

STOP = set("the a an and or of to in for with on at by is are be as from that this it your our we you".split())


def _tok(text: str) -> list[str]:
    """Lowercase, split, and drop stopwords/single characters to form tokens."""
    return [w for w in re.findall(r"[a-z0-9\+#\.]+", text.lower()) if w not in STOP and len(w) > 1]


@lru_cache(maxsize=1)
def _index():
    """Build and cache the TF-IDF index of knowledge-base chunks."""
    chunks = []
    for f in sorted(config.KNOWLEDGE_DIR.glob("*.md")):
        for block in re.split(r"\n(?=#{1,3} )", f.read_text()):
            if block.strip():
                chunks.append({"source": f.name, "text": block.strip()})
    df = Counter()
    for c in chunks:
        c["tf"] = Counter(_tok(c["text"]))
        df.update(c["tf"].keys())
    n = max(len(chunks), 1)
    idf = {t: math.log((1 + n) / (1 + d)) + 1 for t, d in df.items()}
    for c in chunks:
        c["vec"] = {t: f * idf[t] for t, f in c["tf"].items()}
        c["norm"] = math.sqrt(sum(v * v for v in c["vec"].values())) or 1.0
    return chunks, idf


def reload_index():
    """Invalidate the cached index so the next search re-reads the knowledge files."""
    _index.cache_clear()


def search_knowledge(query: str, k: int = 3) -> dict:
    """Return the top-k knowledge chunks by cosine similarity to the query."""
    chunks, idf = _index()
    q = Counter(_tok(query))
    qv = {t: f * idf.get(t, 1.0) for t, f in q.items()}
    qn = math.sqrt(sum(v * v for v in qv.values())) or 1.0
    scored = []
    for c in chunks:
        dot = sum(w * c["vec"].get(t, 0.0) for t, w in qv.items())
        scored.append((dot / (qn * c["norm"]), c))
    scored.sort(key=lambda x: -x[0])
    return {"results": [{"source": c["source"], "relevance": round(s, 3), "text": c["text"]}
                        for s, c in scored[:k] if s > 0]}
