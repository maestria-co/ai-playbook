#!/usr/bin/env python3
"""Print a linked source as markdown, from the skill's cache when it is fresh.

Usage: python3 scripts/fetch_link.py <url>

The cache lives in cache/ next to this skill's SKILL.md, one file per page.
A cached page older than MAX_AGE_DAYS is fetched again and rewritten.
"""

import datetime
import hashlib
import pathlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

# These sources change rarely, so two months keeps reads cheap without
# letting a moved or rewritten page go unnoticed for long.
MAX_AGE_DAYS = 60
CACHE_DIR = pathlib.Path(__file__).resolve().parent.parent / "cache"
FETCHED_PREFIX = "Fetched: "
# Some sites refuse requests without a browser-like agent string.
USER_AGENT = "Mozilla/5.0 (compatible; design-principles-skill)"
# Long slugs hit filesystem name limits; a hash suffix keeps them unique.
MAX_SLUG_LENGTH = 100


def page_url(url):
    """Anchors point into the same page, so they share one cache file."""
    return urllib.parse.urldefrag(url)[0]


def cache_path(url):
    parts = urllib.parse.urlsplit(page_url(url))
    slug = re.sub(r"[^a-z0-9.]+", "-", (parts.netloc + parts.path + "-" + parts.query).lower()).strip("-.")
    if len(slug) > MAX_SLUG_LENGTH:
        digest = hashlib.sha1(page_url(url).encode()).hexdigest()[:8]
        slug = slug[:MAX_SLUG_LENGTH] + "-" + digest
    return CACHE_DIR / (slug + ".md")


def fetched_on(path):
    for line in path.read_text(encoding="utf-8").splitlines()[:5]:
        if line.startswith(FETCHED_PREFIX):
            return datetime.date.fromisoformat(line[len(FETCHED_PREFIX):].strip())
    return None


def is_fresh(path):
    if not path.exists():
        return False
    fetched = fetched_on(path)
    return fetched is not None and (datetime.date.today() - fetched).days <= MAX_AGE_DAYS


def download_target(url):
    """A GitHub repository page is mostly site chrome; its README is the content."""
    parts = urllib.parse.urlsplit(url)
    segments = [s for s in parts.path.split("/") if s]
    if parts.netloc == "github.com" and len(segments) == 2:
        return f"https://raw.githubusercontent.com/{segments[0]}/{segments[1]}/HEAD/README.md"
    return url


class MarkdownConverter(HTMLParser):
    """Page chrome (menus, footers, scripts) would bury the text an agent needs."""

    SKIP = {"script", "style", "nav", "header", "footer", "aside", "svg", "noscript", "form", "button", "iframe"}
    BLOCK = {"p", "div", "section", "article", "main", "table", "tr", "blockquote", "figure"}

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.out = []
        self.skip_depth = 0
        self.in_pre = False
        self.href = None
        self.list_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
        if self.skip_depth:
            return
        attrs = dict(attrs)
        if re.fullmatch(r"h[1-6]", tag):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in self.BLOCK:
            self.out.append("\n\n")
        elif tag == "br":
            self.out.append("\n")
        elif tag in ("ul", "ol"):
            self.list_depth += 1
        elif tag == "li":
            self.out.append("\n" + "  " * (self.list_depth - 1) + "- ")
        elif tag == "pre":
            self.in_pre = True
            self.out.append("\n\n```\n")
        elif tag == "code" and not self.in_pre:
            self.out.append("`")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "a" and attrs.get("href") and not attrs["href"].startswith("#"):
            self.href = urllib.parse.urljoin(self.base_url, attrs["href"])
            self.out.append("[")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if re.fullmatch(r"h[1-6]", tag) or tag in self.BLOCK:
            self.out.append("\n\n")
        elif tag in ("ul", "ol"):
            self.list_depth = max(0, self.list_depth - 1)
            self.out.append("\n")
        elif tag == "pre":
            self.in_pre = False
            self.out.append("\n```\n\n")
        elif tag == "code" and not self.in_pre:
            self.out.append("`")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "a" and self.href:
            self.out.append(f"]({self.href})")
            self.href = None

    def handle_data(self, data):
        if self.skip_depth:
            return
        self.out.append(data if self.in_pre else re.sub(r"\s+", " ", data))

    def markdown(self):
        text = "".join(self.out)
        text = re.sub(r"[ \t]+\n", "\n", text)
        return re.sub(r"\n{3,}", "\n\n", text).strip()


def main_content(html):
    """Prefer the page's <main> or <article>, so menus and sidebars stay out."""
    for tag in ("main", "article"):
        match = re.search(rf"<{tag}\b.*?</{tag}>", html, re.S | re.I)
        if match:
            return match.group(0)
    return html


def fetch_markdown(url):
    request = urllib.request.Request(download_target(url), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        content_type = response.headers.get_content_type()
        body = response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    if content_type in ("text/markdown", "text/plain"):
        return body.strip()
    if content_type != "text/html":
        raise ValueError(f"{content_type} pages are not converted; open the link directly")
    converter = MarkdownConverter(url)
    converter.feed(main_content(body))
    return converter.markdown()


def heading_anchor(heading):
    """GitHub-style anchor, so a link like ...#brooks-law finds its heading."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading.lstrip("#").strip()).lower()
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", text))


def section(document, anchor):
    """A link to one section needs that section, not the whole page in context."""
    lines = document.splitlines()
    header = lines[:2]
    for start, line in enumerate(lines):
        if line.startswith("#") and heading_anchor(line) == anchor:
            level = len(line) - len(line.lstrip("#"))
            end = next((i for i in range(start + 1, len(lines))
                        if lines[i].startswith("#") and len(lines[i]) - len(lines[i].lstrip("#")) <= level), len(lines))
            return "\n".join(header + [""] + lines[start:end])
    return document


def show(document, anchor):
    print(section(document, anchor) if anchor else document)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/fetch_link.py <url>")
    url, anchor = urllib.parse.urldefrag(sys.argv[1])
    path = cache_path(url)
    if is_fresh(path):
        show(path.read_text(encoding="utf-8"), anchor)
        return
    try:
        content = fetch_markdown(url)
    except (urllib.error.URLError, ValueError, TimeoutError) as error:
        # A stale copy beats no copy when the site is down; say so plainly.
        if path.exists():
            print(f"Could not refresh {url} ({error}); showing the cached copy.", file=sys.stderr)
            show(path.read_text(encoding="utf-8"), anchor)
            return
        sys.exit(f"Could not fetch {url}: {error}")
    CACHE_DIR.mkdir(exist_ok=True)
    document = f"Source: {url}\n{FETCHED_PREFIX}{datetime.date.today().isoformat()}\n\n{content}\n"
    path.write_text(document, encoding="utf-8")
    show(document, anchor)


if __name__ == "__main__":
    main()
