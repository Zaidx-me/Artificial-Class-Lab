"""Generate sample resume PDFs and a simulated inbox of .eml files (for demo / viva without credentials)."""
from email.message import EmailMessage
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parent.parent
RES, INBOX = ROOT / "assets" / "resumes", ROOT / "assets" / "inbox"
RES.mkdir(parents=True, exist_ok=True); INBOX.mkdir(parents=True, exist_ok=True)

CANDS = [
 ("Ayesha Khan", "ayesha.khan@example.com", "BSCS, FAST-NUCES (2019)",
  ["Backend Engineer, Systems Ltd (2019-2024): 5 years building REST APIs in Python with Django and FastAPI on PostgreSQL.",
   "Dockerised services and deployed to AWS; set up CI/CD pipelines and pytest suites (90% coverage).",
   "Introduced Redis caching, cutting API latency by 40%."],
  "Python, Django, FastAPI, SQL, PostgreSQL, Docker, AWS, Git, pytest, Redis, CI/CD, Linux"),
 ("Bilal Ahmed", "bilal.ahmed@example.com", "BSIT, University of Lahore (2021)",
  ["Junior Developer, WebWorks (2021-2023): 2 years building Flask APIs and SQL reports.",
   "Used Git daily and wrote unit tests with pytest for core modules."],
  "Python, Flask, SQL, Git, pytest, JavaScript"),
 ("Sara Malik", "sara.malik@example.com", "BS Software Engineering, NUST (2025)",
  ["Final-year project: REST API with FastAPI and PostgreSQL, deployed using Docker.",
   "Summer internship (3 months) at a startup working with Python and Git."],
  "Python, FastAPI, SQL, Docker, Git"),
 ("Usman Tariq", "usman.tariq@example.com", "BSc Graphic Design (2018)",
  ["Frontend Developer, PixelHouse (2018-2024): 6 years building React and JavaScript user interfaces.",
   "Some experience with Node tooling and CSS design systems."],
  "JavaScript, React, CSS, Figma"),
 ("Hina Raza", "hina.raza@example.com", "Bachelor of Computer Science, COMSATS (2020)",
  ["Data Analyst, InsightCo (2020-2023): 3 years of SQL reporting and Python scripts for ETL.",
   "Built a machine learning churn model with PyTorch; REST API wrapper in Flask."],
  "Python, SQL, PostgreSQL, machine learning, PyTorch, Flask, Git, Linux"),
]
st = getSampleStyleSheet()
for i, (name, mail, edu, exp, skills) in enumerate(CANDS, 1):
    path = RES / f"{name.replace(' ', '_')}_CV.pdf"
    story = [Paragraph(name, st["Title"]), Paragraph(f"Email: {mail}", st["Normal"]), Spacer(1, 12),
             Paragraph("Education", st["Heading2"]), Paragraph(edu, st["Normal"]),
             Paragraph("Experience", st["Heading2"])]
    story += [Paragraph("- " + e, st["Normal"]) for e in exp]
    story += [Paragraph("Skills", st["Heading2"]), Paragraph(skills, st["Normal"])]
    SimpleDocTemplate(str(path), pagesize=A4).build(story)
    m = EmailMessage()
    m["From"] = f"{name} <{mail}>"; m["To"] = "hr@company.example"
    m["Subject"] = "Application - Software Engineer"; m["Message-ID"] = f"<sample-{i}@example.com>"
    m.set_content(f"Dear Hiring Team,\n\nPlease find my CV attached for the Software Engineer role.\n\nRegards,\n{name}")
    m.add_attachment(path.read_bytes(), maintype="application", subtype="pdf", filename=path.name)
    (INBOX / f"{i:02d}_{name.split()[0].lower()}.eml").write_bytes(bytes(m))

m = EmailMessage()  # an email with no resume: agent must skip it
m["From"] = "Newsletter <news@spam.example>"; m["To"] = "hr@company.example"
m["Subject"] = "Weekly offers"; m["Message-ID"] = "<sample-spam@example.com>"
m.set_content("Buy now!")
(INBOX / "99_noresume.eml").write_bytes(bytes(m))
print("Generated", len(CANDS), "resumes + 1 no-resume email")
