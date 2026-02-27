#!/usr/bin/env python3
"""
Convert .eml to Markdown.
- Ignores ALL headers
- Keeps only the readable body
- Removes embedded media and attachments
- Prefers text/plain over text/html
"""

import argparse
import os
import re
from email import policy
from email.parser import BytesParser
from email.message import Message
from html.parser import HTMLParser


# ---------------------------------------------------------
# Simple HTML → Markdown converter (media stripped)
# ---------------------------------------------------------

class SimpleHTMLToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
        self.drop_depth = 0
        self.in_pre = False
        self.in_code = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag in ("script", "style"):
            self.drop_depth += 1
            return
        if self.drop_depth:
            return

        if tag == "img":
            return  # drop images entirely

        if tag in ("br",):
            self.output.append("\n")
        elif tag in ("p", "div"):
            self.output.append("\n\n")
        elif tag in ("h1","h2","h3","h4","h5","h6"):
            level = int(tag[1])
            self.output.append("\n\n" + "#" * level + " ")
        elif tag == "li":
            self.output.append("\n- ")
        elif tag in ("strong", "b"):
            self.output.append("**")
        elif tag in ("em", "i"):
            self.output.append("*")
        elif tag == "pre":
            self.in_pre = True
            self.output.append("\n\n```text\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = True
            self.output.append("`")

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in ("script", "style"):
            self.drop_depth -= 1
            return
        if self.drop_depth:
            return

        if tag in ("strong", "b"):
            self.output.append("**")
        elif tag in ("em", "i"):
            self.output.append("*")
        elif tag == "pre":
            self.in_pre = False
            self.output.append("\n```\n")
        elif tag == "code" and self.in_code:
            self.in_code = False
            self.output.append("`")

    def handle_data(self, data):
        if self.drop_depth:
            return
        if not self.in_pre:
            data = re.sub(r"\s+", " ", data)
        self.output.append(data)

    def get_markdown(self):
        text = "".join(self.output)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def html_to_markdown(html):
    parser = SimpleHTMLToMarkdown()
    parser.feed(html)
    return parser.get_markdown()


# ---------------------------------------------------------
# Body extraction
# ---------------------------------------------------------

def is_valid_text_part(part: Message):
    if part.get_content_disposition() == "attachment":
        return False
    if part.get_filename():
        return False
    if part.get_content_maintype() != "text":
        return False
    if part.get_content_type() not in ("text/plain", "text/html"):
        return False
    return True


def extract_body(msg: Message):
    text_plain = None
    text_html = None

    for part in msg.walk():
        if part.is_multipart():
            continue
        if not is_valid_text_part(part):
            continue

        try:
            content = part.get_content()
        except Exception:
            raw = part.get_payload(decode=True) or b""
            charset = part.get_content_charset() or "utf-8"
            content = raw.decode(charset, errors="replace")

        if part.get_content_type() == "text/plain" and text_plain is None:
            text_plain = content
        elif part.get_content_type() == "text/html" and text_html is None:
            text_html = content

    if text_plain:
        return clean_plain(text_plain)
    elif text_html:
        return html_to_markdown(text_html)
    else:
        return ""


def clean_plain(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    return text.strip() + "\n"


# ---------------------------------------------------------
# Main conversion
# ---------------------------------------------------------

def eml_to_markdown(path):
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    return extract_body(msg)


def main():
    parser = argparse.ArgumentParser(description="Convert EML to Markdown (no headers).")
    parser.add_argument("eml")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    output_path = args.output or os.path.splitext(args.eml)[0] + ".md"

    markdown = eml_to_markdown(args.eml)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()