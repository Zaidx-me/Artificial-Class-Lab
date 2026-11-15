"""Tool 2: resume parser (PDF, DOCX, TXT)."""
from pathlib import Path


def extract_text_from_resume(path: str) -> str:
    """Return the plain text of a resume file. Raises ValueError on unsupported/empty files."""
    p = Path(path)
    if not p.exists():
        raise ValueError(f"File not found: {path}")
    ext = p.suffix.lower()
    if ext == ".pdf":
        from pypdf import PdfReader
        text = "\n".join((pg.extract_text() or "") for pg in PdfReader(str(p)).pages)
    elif ext == ".docx":
        import docx
        d = docx.Document(str(p))
        text = "\n".join(par.text for par in d.paragraphs)
        for t in d.tables:
            for row in t.rows:
                text += "\n" + " | ".join(c.text for c in row.cells)
    elif ext in (".txt", ".md"):
        text = p.read_text(errors="ignore")
    else:
        raise ValueError(f"Unsupported resume format: {ext}")
    text = text.strip()
    if not text:
        raise ValueError("No extractable text (scanned image PDF?)")
    return text
