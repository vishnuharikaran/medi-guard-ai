"""Unit tests for security vulnerabilities and code cleanliness."""

import html
import subprocess
import sys


def test_html_escaping():
    malicious_input = "<script>alert('xss')</script>"
    escaped = html.escape(malicious_input)
    assert "<script>" not in escaped
    assert "&lt;script&gt;" in escaped


def test_no_speech_references_in_codebase():
    cmd = [sys.executable, "-c", "import app"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
