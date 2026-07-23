#!/usr/bin/env python3
"""Fail closed when the public static artifact violates its small trust boundary."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
EXPECTED = {
    "404.html",
    "assets/site.css",
    "index.html",
}
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".svg", ".txt"}
FORBIDDEN_SUFFIXES = {
    ".3ds",
    ".avi",
    ".bin",
    ".dds",
    ".elf",
    ".iso",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".ogg",
    ".png",
    ".psarc",
    ".self",
    ".sprx",
    ".wav",
}
FORBIDDEN_TEXT = (
    "/var/home/",
    "/home/",
    "infamous-decomp",
    "proof_scope",
    "BEGIN PRIVATE KEY",
    "CF_API_TOKEN",
    "GITHUB_TOKEN",
)
SECRET_PATTERNS = (
    re.compile(r"gh[opsu]_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
)


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.h1 = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "h1":
            self.h1 += 1
        if tag in {"a", "link", "script"}:
            attr = "href" if tag in {"a", "link"} else "src"
            if values.get(attr):
                self.links.append((tag, values[attr] or ""))


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    if not SITE.is_dir() or SITE.is_symlink():
        fail("site must be a real directory")
    if (SITE / "CNAME").exists():
        fail("custom domain cutover is intentionally held; CNAME is forbidden")

    files = sorted(path for path in SITE.rglob("*") if path.is_file())
    relative = {path.relative_to(SITE).as_posix() for path in files}
    missing = EXPECTED - relative
    if missing:
        fail(f"missing required site files: {sorted(missing)}")

    for path in SITE.rglob("*"):
        if path.is_symlink():
            fail(f"symlink forbidden in public artifact: {path.relative_to(SITE)}")
    for path in files:
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"game/media-like file forbidden: {path.relative_to(SITE)}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            fail(f"unexpected public file type: {path.relative_to(SITE)}")

    parsers: dict[Path, Links] = {}
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        for needle in FORBIDDEN_TEXT:
            if needle in text:
                fail(f"forbidden disclosure marker {needle!r} in {path.relative_to(ROOT)}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"secret-like token in {path.relative_to(ROOT)}")
        if path.suffix == ".html":
            parser = Links()
            parser.feed(text)
            parsers[path] = parser
            if parser.h1 != 1:
                fail(f"{path.relative_to(SITE)} must contain exactly one h1")
            if "#main" not in [link for tag, link in parser.links if tag == "a"]:
                fail(f"{path.relative_to(SITE)} is missing a skip link")

    for source, parser in parsers.items():
        for tag, link in parser.links:
            if link.startswith(("mailto:", "tel:")):
                continue
            parsed = urlsplit(link)
            if parsed.scheme:
                if parsed.scheme != "https":
                    fail(f"non-HTTPS external link in {source.relative_to(SITE)}: {link}")
                continue
            if link.startswith("//"):
                fail(f"scheme-relative link forbidden: {link}")
            target_text = parsed.path
            target = SITE / target_text.lstrip("/") if target_text.startswith("/") else source.parent / target_text
            if not target_text:
                target = source
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                fail(f"broken local link in {source.relative_to(SITE)}: {link}")
            if parsed.fragment and target.suffix == ".html":
                target_parser = parsers.get(target.resolve())
                if target_parser is None:
                    target_parser = Links()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                if parsed.fragment not in target_parser.ids:
                    fail(f"missing fragment target in {source.relative_to(SITE)}: {link}")

    workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    uses = re.findall(r"uses:\s*([^\s#]+)", workflow)
    if not uses or any(not re.search(r"@[0-9a-f]{40}$", item) for item in uses):
        fail("every workflow action must be pinned to a full commit SHA")
    if "github.event_name != 'pull_request'" not in workflow:
        fail("pull requests must validate without deploying")

    print(f"public-site checks passed: {len(files)} files, {len(parsers)} HTML documents")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, UnicodeError) as error:
        print(f"public-site check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
