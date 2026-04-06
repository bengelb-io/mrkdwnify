import pytest
from pathlib import Path
from mrkdwnify import mrkdwnify

FIXTURES_DIR = Path(__file__).parent / "fixtures"
DELIMITER = "===="


def _load_fixture(name: str):
    text = (FIXTURES_DIR / name).read_text()
    html, expected = text.split(DELIMITER, 1)
    return html.strip(), expected.strip()


FIXTURE_NAMES = [p.name for p in sorted(FIXTURES_DIR.iterdir()) if p.is_file()]


@pytest.mark.parametrize("fixture_name", FIXTURE_NAMES)
def test_fixture(fixture_name: str):
    html, expected = _load_fixture(fixture_name)
    assert mrkdwnify(html).strip() == expected


# --- OL numbering ---

def test_ol_numbering_with_pretty_printed_html():
    """OL items in pretty-printed HTML must number correctly from 1."""
    html = "<ol>\n  <li>item 1</li>\n  <li>item 2</li>\n</ol>"
    result = mrkdwnify(html)
    assert "1. item 1" in result
    assert "2. item 2" in result
    assert "2. item 1" not in result  # old bug: whitespace nodes offset index

def test_ol_with_start_attribute():
    html = "<ol start='3'><li>item</li><li>item</li></ol>"
    result = mrkdwnify(html)
    assert "3. item" in result
    assert "4. item" in result


# --- Paragraph separation ---

def test_two_paragraphs_are_separated():
    """Two <p> tags must produce a blank line between them."""
    html = "<p>first</p><p>second</p>"
    result = mrkdwnify(html).strip()
    assert result == "first\n\nsecond"


# --- Angle bracket escaping ---

def test_angle_brackets_in_text_are_html_encoded():
    """Literal < and > in text must be output as &lt; and &gt; for Slack safety."""
    result = mrkdwnify("<p>&lt;hello&gt;</p>").strip()
    assert result == "&lt;hello&gt;"

def test_angle_brackets_not_double_encoded_in_links():
    """The <url|text> link format must not have its angle brackets escaped."""
    result = mrkdwnify('<a href="https://example.com">text</a>').strip()
    assert result == "<https://example.com|text>"


# --- Checkbox handling ---

def test_unchecked_checkbox():
    html = '<ul><li><input type="checkbox"> item</li></ul>'
    assert "☐ item" in mrkdwnify(html)

def test_checked_checkbox_boolean_attribute():
    """Real HTML boolean checked attribute (no value) must be recognized."""
    html = '<ul><li><input type="checkbox" checked> item</li></ul>'
    assert "☑︎ item" in mrkdwnify(html)

def test_checked_checkbox_string_attribute():
    """checked="true" (legacy format) must also be recognized."""
    html = '<ul><li><input type="checkbox" checked="true"> item</li></ul>'
    assert "☑︎ item" in mrkdwnify(html)

def test_special_bullet_with_whitespace_leading_child():
    """Checkbox detection must work when <li> has a leading whitespace text node."""
    html = '<ul>\n  <li>\n    <input type="checkbox" checked> item\n  </li>\n</ul>'
    assert "☑︎" in mrkdwnify(html)


# --- Nested list indentation ---

def test_nested_unordered_list_is_indented():
    html = "<ul><li>outer<ul><li>inner</li></ul></li></ul>"
    result = mrkdwnify(html)
    lines = [l for l in result.splitlines() if l.strip()]
    outer_line = next(l for l in lines if "outer" in l)
    inner_line = next(l for l in lines if "inner" in l)
    assert inner_line.startswith(" ")
    assert outer_line.index("•") < inner_line.index("•")


# --- Table behavior ---

def test_table_produces_no_output():
    """Tables must be silently dropped."""
    html = "<table><tr><td>cell</td></tr></table>"
    assert mrkdwnify(html).strip() == ""


# --- Options refactor ---

def test_no_private_api_import():
    """_todict must not be imported from markdownify."""
    import mrkdwnify as pkg
    assert not hasattr(pkg, "_todict")

def test_mrkdwnify_accepts_override_options():
    """Caller should be able to override options via kwargs."""
    result = mrkdwnify("<p>hello_world</p>", escape_underscores=False).strip()
    assert result == "hello_world"


# --- Combined escaping (exercises heading + paragraph + angle brackets) ---

def test_escaping_fixture_combined():
    html = (
        "<h2>1. First things first</h2>"
        "<p>[Effort: M, Impact: L]</p>"
        "<p>&lt;hello&gt;</p>"
    )
    result = mrkdwnify(html).strip()
    assert result == "*1. First things first*\n\n[Effort: M, Impact: L]\n\n&lt;hello&gt;"
