from markdownify import (
    MarkdownConverter,
    abstract_inline_conversion,
    chomp,
    re_line_with_content,
    ASTERISK,
    ATX,
    ATX_CLOSED,
    UNDERLINED,
)
from bs4 import Tag
from typing import Optional

__version__ = "1.0.0"


class MrkdwnConverter(MarkdownConverter):
    class Options(MarkdownConverter.Options):
        convert = [
            "a", "blockquote", "pre", "code", "p",
            *[f"h{i}" for i in range(1, 7)],
            "del", "em", "img", "i", "ol", "ul", "li",
            "s", "strike", "b", "strong", "br", "table",
        ]
        bullets = "•"
        heading_style = ASTERISK

    # --- Inline formatting ---

    convert_b = abstract_inline_conversion(lambda self: "*")
    convert_strong = convert_b
    convert_em = abstract_inline_conversion(lambda self: "_")
    convert_i = convert_em
    convert_s = abstract_inline_conversion(lambda self: "~")
    convert_strike = convert_s
    convert_del = convert_s

    # --- Escaping ---

    def escape(self, text, parent_tags):
        text = super().escape(text, parent_tags)
        text = text.replace("<", "&lt;").replace(">", "&gt;")
        return text

    # --- Headings ---

    def convert_hN(self, n, el, text, parent_tags):
        if "_inline" in parent_tags:
            return text
        style = self.options["heading_style"].lower()
        text = text.strip()
        if style == UNDERLINED and n <= 2:
            line = "=" if n == 1 else "-"
            return self.underline(text, line)
        hashes = "#" * n
        if style == ATX_CLOSED:
            return "\n\n%s %s %s\n\n" % (hashes, text, hashes)
        if style == ASTERISK:
            return "\n\n%s\n\n" % self.convert_b(el, text, parent_tags)
        return "\n\n%s %s\n\n" % (hashes, text)

    # --- List items ---

    def _checkbox_bullet(self, el):
        """Return ☑︎ or ☐ if el is a task-list item, else None."""
        inp = el.find("input", recursive=False)
        if not isinstance(inp, Tag):
            return None
        if inp.get("type") != "checkbox":
            return None
        return "☑︎" if inp.has_attr("checked") else "☐"

    def convert_li(self, el, text, parent_tags):
        text = (text or "").strip()
        if not text:
            return "\n"

        parent = el.parent
        if parent is not None and parent.name == "ol":
            if parent.get("start") and str(parent.get("start")).isnumeric():
                start = int(parent.get("start"))
            else:
                start = 1
            bullet = "%s." % (start + len(el.find_previous_siblings("li")))
        else:
            checkbox = self._checkbox_bullet(el)
            if checkbox:
                bullet = checkbox
            else:
                depth = -1
                node = el
                while node:
                    if node.name == "ul":
                        depth += 1
                    node = node.parent
                bullets = self.options["bullets"]
                bullet = bullets[depth % len(bullets)]

        bullet = bullet + " "
        bullet_width = len(bullet)
        bullet_indent = " " * bullet_width

        def _indent_for_li(match):
            line_content = match.group(1)
            return bullet_indent + line_content if line_content else ""

        text = re_line_with_content.sub(_indent_for_li, text)
        text = bullet + text[bullet_width:]
        return "%s\n" % text

    # --- Links ---

    def _img_with_href(self, el, href):
        """Render an <img> wrapped in an <a> as a Slack link."""
        alt = el.attrs.get("alt") or ""
        src = el.attrs.get("src") or ""
        title = el.attrs.get("title") or ""
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ""
        label = alt if alt else src
        return "<%s|%s%s>" % (href, label, title_part)

    def convert_a(self, el, text, parent_tags):
        prefix, suffix, text = chomp(text)
        if not text:
            return ""
        href = el.get("href")
        title = el.get("title")

        child = el.find(True, recursive=False)
        if isinstance(child, Tag) and child.name == "img":
            return self._img_with_href(child, href)

        if (
            self.options["autolinks"]
            and text.replace(r"\_", "_") == href
            and not title
            and not self.options["default_title"]
        ):
            return "<%s>" % href
        if self.options["default_title"] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ""
        return "%s<%s|%s%s>%s" % (prefix, href, text, title_part, suffix) if href else text

    # --- Images ---

    def convert_img(self, el, text, parent_tags):
        alt = el.attrs.get("alt") or ""
        src = el.attrs.get("src") or ""
        title = el.attrs.get("title") or ""
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ""
        if not alt and not src:
            return ""
        if "_inline" in parent_tags and el.parent.name not in self.options["keep_inline_images_in"]:
            return alt
        if alt:
            return "<%s|%s%s>" % (src, alt, title_part)
        return src

    # --- Tables ---

    def convert_table(self, el, text, parent_tags):
        return ""


def mrkdwnify(html: str, **options) -> str:
    return MrkdwnConverter(**options).convert(html)
