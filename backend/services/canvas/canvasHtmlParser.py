import re
from html import unescape
from html.parser import HTMLParser


# max character limits kept from HTML bodies (i.e. assignment descriptions, announcements, etc.)
DESCRIPTION_LIMIT = 800
MESSAGE_LIMIT = 600


# used with canvasJsonParser, this helps convert HTML given in the JSON to normal text
class HtmlTextExtractor(HTMLParser):
    """
    Collects visible text from an HTML string, keeping rough line breaks.
    """

    BLOCK_TAGS = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "table"}
    SKIP_TAGS = {"script", "style"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "li":
            self.parts.append("- ")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip_depth:
            self.parts.append(data)


def html_to_text(html: str | None, limit: int | None = DESCRIPTION_LIMIT) -> str | None:
    """
    Converts Canvas HTML into plain text and truncates it to the given limit.
    """

    if not html:
        return None

    extractor = HtmlTextExtractor()
    try:
        extractor.feed(html)
        extractor.close()
        text = "".join(extractor.parts)
    except Exception:
        # fall back to a crude tag strip if the HTML is malformed
        text = unescape(re.sub(r"<[^>]+>", " ", html))

    # collapse whitespace while keeping single line breaks
    text = re.sub(r"[ \t\r\f\v\xa0]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text).strip()

    if not text:
        return None

    if limit and len(text) > limit:
        text = text[:limit].rstrip() + "... (truncated, see html_url for full text)"

    return text