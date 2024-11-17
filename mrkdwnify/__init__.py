from markdownify import MarkdownConverter, abstract_inline_conversion, chomp, UNDERLINED, ATX_CLOSED, ATX, ASTERISK, _todict
from bs4 import Tag
from typing import Optional
from string import digits

__version__ = "0.1.1"


class MrkdwnOptions:
    convert = [
        "a", "blockquote", "pre", "code", *[f"h{i}" for i in range(1, 7)],
        "del", "em", "img", "i", "ol", "ul", "li", "s", "strike", "b",
        "strong", "br", "table"
    ]
    bullets = '•'  # An iterable of bullet types.
    strong_em_symbol = ASTERISK
    heading_style = ASTERISK
    render_tables = False


class MrkdwnConverter(MarkdownConverter):
    convert_b = abstract_inline_conversion(lambda self: "*")
    convert_strong = convert_b
    convert_em = abstract_inline_conversion(lambda self: "_")
    convert_i = convert_em
    convert_s = abstract_inline_conversion(lambda self: "~")
    convert_strike = convert_s
    convert_del = convert_s

    def special_bullet(self, el):
        child = next(iter(el.children))
        if type(child) == Tag:
            if child.get("type") == "checkbox":
                if bool(child.get("checked")) == True:
                    return "☑︎"
                return "☐"
        return None

    def convert_li(self, el, text, convert_as_inline):
        parent = el.parent
        special_bullet = self.special_bullet(el)
        if parent is not None and parent.name == 'ol':
            if parent.get("start") and str(parent.get("start")).isnumeric():
                start = int(parent.get("start"))
            else:
                start = 1
            bullet = '%s.' % (start + parent.index(el))
        else:
            depth = -1
            while el:
                if el.name == 'ul':
                    depth += 1
                el = el.parent
            bullets = self.options['bullets']
            bullet = special_bullet or bullets[depth % len(bullets)]
        return '%s %s\n' % (bullet, (text or '').strip())

    def tabulate_newlines(self, el: Tag):
        if el.next_sibling:
            if type(el.next_sibling) == Tag:
                if el.next_sibling.name.rstrip(digits) == el.name.rstrip(
                        digits):
                    return "\n"
        return "\n\n"

    def convert_hn(self, n, el, text, convert_as_inline):
        if convert_as_inline:
            return text
        style = self.options['heading_style'].lower()
        text = text.strip()
        if style == UNDERLINED and n <= 2:
            line = '=' if n == 1 else '-'
            return self.underline(text, line)
        hashes = '#' * n
        if style == ATX_CLOSED:
            return '%s %s %s\n\n' % (hashes, text, hashes)
        if style == ASTERISK:
            return '%s%s' % (self.convert_b(
                el, text, convert_as_inline), self.tabulate_newlines(el))
        return '%s %s\n\n' % (hashes, text)

    def convert_table(self, el, text, convert_as_inline):
        if self.options["render_tables"]:
            return super().convert_table(el, text, convert_as_inline)
        return ""

    def convert_img(self,
                    el,
                    text,
                    convert_as_inline,
                    href: Optional[str] = None):
        alt = el.attrs.get('alt', None) or ''
        src = el.attrs.get('src', None) or ''
        title = el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        if not alt and not href:
            return src
        if (convert_as_inline and el.parent.name
                not in self.options['keep_inline_images_in']):
            return alt
        if href:
            return '<%s|%s%s>' % (href, alt if alt else src, title_part)
        return '<%s|%s%s>' % (src, alt, title_part)

    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        href = el.get('href')
        title = el.get('title')

        child = next(iter(el.children))
        if type(child) == Tag:
            if child.name == "img":
                return self.convert_img(child, child.text, convert_as_inline, href)

        # For the replacement see #29: text nodes underscores are escaped
        if (self.options['autolinks'] and text.replace(r'\_', '_') == href
                and not title and not self.options['default_title']):
            # Shortcut syntax
            return '<%s>' % href
        if self.options['default_title'] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        return '%s<%s|%s%s>%s' % (prefix, href, text, title_part,
                                  suffix) if href else text


def mrkdwnify(html: str, **options):
    return MrkdwnConverter(**_todict(MrkdwnOptions), **options).convert(html)
