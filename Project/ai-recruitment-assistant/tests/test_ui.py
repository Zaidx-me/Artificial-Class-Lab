import os, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["USE_MOCK_LLM"] = "1"
os.environ["DB_PATH"] = str(Path(tempfile.mkdtemp()) / "ui.db")
os.environ["EMAIL_USER"] = ""
os.environ["EMAIL_PASS"] = ""
os.environ["LLM_API_KEY"] = ""
os.environ["LLM_BASE_URL"] = ""
from streamlit.testing.v1 import AppTest


def test_ui_flow():
    at = AppTest.from_file(str(Path(__file__).resolve().parent.parent / "app.py"), default_timeout=30).run()
    assert not at.exception
    next(b for b in at.button if "Process new" in b.label).click().run()
    assert not at.exception
    assert any("Ayesha Khan" in m.value for m in at.markdown)
    at.chat_input[0].set_value("Who are the top 3 candidates?").run()
    assert not at.exception
    assert len(at.tabs) == 3


def test_gmail_source_requires_credentials():
    at = AppTest.from_file(str(Path(__file__).resolve().parent.parent / "app.py"), default_timeout=30).run()
    source_radio = next(r for r in at.radio if "Gmail inbox" in r.options)
    gmail_label = next(o for o in source_radio.options if "Gmail" in o)
    source_radio.set_value(gmail_label).run()
    assert not at.exception
    assert any("EMAIL_USER" in w.value for w in at.warning)
    next(b for b in at.button if "Process new" in b.label).click().run()
    assert not at.exception
    assert any("EMAIL_USER" in w.value for w in at.warning)
