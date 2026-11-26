"""Extract plain text from the policy documents (.docx and .pdf)."""
from pathlib import Path

from docx import Document
from pypdf import PdfReader
from docx.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs/course_brief/Capstone2_Customer_Knowledge_Support_Dataset_v2/documents"


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


def extract_pdf(path):
    """Return the non-empty lines of a PDF, page by page."""
    reader = PdfReader(path)
    lines = []
    for page in reader.pages:
        text = page.extract_text() or ""
        lines.extend(line.strip() for line in text.splitlines() if line.strip())
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
        for line in lines[:15]:
            print(line)
