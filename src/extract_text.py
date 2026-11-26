"""Extract plain text from the policy documents (.docx and .pdf), including tables."""
import re
from pathlib import Path

import pdfplumber
from docx import Document
from docx.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs/course_brief/Capstone2_Customer_Knowledge_Support_Dataset_v2/documents"

# A section heading starts with a number like "2." or "2.3"
HEADING = re.compile(r"^\d+(\.\d+)*\.?\s")

# PDF bullet symbols come out as special unprintable characters
BULLET = re.compile(r"^[\ue000-\uf8ff•]\s*")

def table_to_lines(rows):
    """Turn table rows into one line per row: 'Header: value | Header: value'."""
    header, *body = rows
    return [" | ".join(f"{h}: {v}" for h, v in zip(header, row) if v) for row in body]


def extract_docx(path):
    """Return the paragraphs and table rows of a Word document, in order."""
    doc = Document(path)
    lines = []
    for item in doc.iter_inner_content():
        if isinstance(item, Table):
            rows = [[cell.text.strip() for cell in row.cells] for row in item.rows]
            lines.extend(table_to_lines(rows))
        elif item.text.strip():
            lines.append(item.text.strip())
    return lines


def is_continuation(prev, cur):
    """True when a PDF line just carries on the sentence from the line before it."""
    if cur["text"].startswith("- "):
        return False
    if prev["table"] or cur["table"]:
        return False
    if HEADING.match(prev["text"]) or HEADING.match(cur["text"]):
        return False
    return not prev["text"].endswith((".", ":", "?", "!"))


def extract_pdf(path):
    """Return the text lines and table rows of a PDF, in reading order."""
    items = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            boxes = [t.bbox for t in tables]

            def outside_tables(obj):
                x = (obj["x0"] + obj["x1"]) / 2
                y = (obj["top"] + obj["bottom"]) / 2
                return not any(x0 <= x <= x1 and top <= y <= bottom for x0, top, x1, bottom in boxes)

            page_items = []
            for line in page.filter(outside_tables).extract_text_lines():
                text = line["text"].strip()
                if BULLET.match(text):
                    text = "- " + BULLET.sub("", text)
                page_items.append({"top": line["top"], "text": text, "table": False})
            for table in tables:
                rows = [[(cell or "").replace("-\n", "-").replace("\n", " ").strip() for cell in row] for row in table.extract()]
                for row_line in table_to_lines(rows):
                    page_items.append({"top": table.bbox[1], "text": row_line, "table": True})

            items.extend(sorted(page_items, key=lambda item: item["top"]))

    lines = []
    for i, item in enumerate(items):
        if not item["text"]:
            continue
        if lines and is_continuation(items[i - 1], item):
            separator = "" if lines[-1].endswith("-") else " "
            lines[-1] += separator + item["text"]
        else:
            lines.append(item["text"])
    return lines


def extract_text(path):
    """Pick the right reader based on the file extension."""
    if path.suffix.lower() == ".docx":
        return extract_docx(path)
    if path.suffix.lower() == ".pdf":
        return extract_pdf(path)
    raise ValueError(f"Unsupported file type: {path.name}")


if __name__ == "__main__":
    for path in sorted(DOCS_DIR.iterdir()):
        lines = extract_text(path)
        print(f"\n===== {path.name} ({len(lines)} lines) =====")
        for line in lines:
            print(line)
