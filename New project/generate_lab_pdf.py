from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "lex_yacc_lab_programs.pdf"


PROGRAMS = [
    ("01_infix_to_postfix", "Program 1: Infix to Postfix Conversion"),
    ("02_boolean_evaluator", "Program 2: Boolean Expression Evaluator"),
    ("03_calculator_with_variables", "Program 3: Calculator with Variables"),
    ("04_for_loop_validator", "Program 4: For Loop Syntax Validator"),
    ("05_balanced_parentheses", "Program 5: Balanced Parentheses Checker"),
    ("06_variable_declaration_validator", "Program 6: Variable Declaration Validator"),
    ("07_if_else_validator", "Program 7: If-Else Syntax Validator"),
    ("08_simple_type_checker", "Program 8: Simple Type Checker"),
    ("09_relational_expression_validator", "Program 9: Relational Expression Validator"),
    ("10_arithmetic_evaluator", "Program 10: Arithmetic Evaluator"),
]


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class SimplePDF:
    def __init__(self):
        self.pages = []
        self.page_width = 595
        self.page_height = 842
        self.margin = 40
        self.current = []
        self.y = self.page_height - self.margin
        self.page_no = 0
        self.new_page()

    def new_page(self):
        if self.current:
            self.pages.append("\n".join(self.current))
        self.current = []
        self.page_no += 1
        self.y = self.page_height - self.margin

    def ensure_space(self, needed):
        if self.y - needed < self.margin:
            self.new_page()

    def text(self, x, y, text, font="F1", size=11):
        safe = pdf_escape(text)
        self.current.append(f"BT /{font} {size} Tf 1 0 0 1 {x} {y} Tm ({safe}) Tj ET")

    def line(self, x1, y1, x2, y2):
        self.current.append(f"{x1} {y1} m {x2} {y2} l S")

    def rect(self, x, y, w, h):
        self.current.append(f"{x} {y} {w} {h} re S")

    def add_wrapped_text(self, text, font="F1", size=11, indent=0, leading=14):
        for raw_line in text.splitlines():
            parts = wrap_line(raw_line, 88 if font == "F2" else 95)
            if not parts:
                self.ensure_space(leading)
                self.text(self.margin + indent, self.y, "", font=font, size=size)
                self.y -= leading
                continue
            for part in parts:
                self.ensure_space(leading)
                self.text(self.margin + indent, self.y, part, font=font, size=size)
                self.y -= leading

    def heading(self, text, size=16):
        self.ensure_space(24)
        self.text(self.margin, self.y, text, font="F1", size=size)
        self.y -= 24

    def subheading(self, text, size=13):
        self.ensure_space(18)
        self.text(self.margin, self.y, text, font="F1", size=size)
        self.y -= 18

    def paragraph(self, text):
        self.add_wrapped_text(text, font="F1", size=11, indent=0, leading=14)
        self.y -= 4

    def code_block(self, code):
        lines = code.splitlines()
        if not lines:
            lines = [""]
        for line in lines:
            parts = wrap_line(line, 82)
            if not parts:
                parts = [""]
            for part in parts:
                self.ensure_space(12)
                self.text(self.margin + 10, self.y, part, font="F2", size=9)
                self.y -= 12
        self.y -= 4

    def output_placeholder(self, title="Output Screenshot Placeholder"):
        box_h = 140
        self.ensure_space(box_h + 30)
        self.text(self.margin, self.y, title, font="F1", size=11)
        self.y -= 18
        self.rect(self.margin, self.y - box_h, self.page_width - (2 * self.margin), box_h)
        self.text(self.margin + 18, self.y - 30, "Paste or attach your program output image here.", font="F1", size=11)
        self.text(self.margin + 18, self.y - 48, "You can also use this area as a manual output record box.", font="F1", size=11)
        self.y -= box_h + 16

    def page_footer(self):
        for index, page in enumerate(self.pages, start=1):
            footer = f"BT /F1 9 Tf 1 0 0 1 {self.page_width - 90} 20 Tm (Page {index}) Tj ET"
            self.pages[index - 1] = page + "\n" + footer

    def save(self, path: Path):
        if self.current:
            self.pages.append("\n".join(self.current))
            self.current = []

        self.page_footer()

        objects = []

        def add_object(data: bytes):
            objects.append(data)
            return len(objects)

        font1 = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        font2 = add_object(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

        page_ids = []
        content_ids = []

        for content in self.pages:
            content_bytes = content.encode("latin-1", "replace")
            content_obj = add_object(
                f"<< /Length {len(content_bytes)} >>\nstream\n".encode("latin-1") +
                content_bytes +
                b"\nendstream"
            )
            content_ids.append(content_obj)
            page_obj = add_object(
                f"<< /Type /Page /Parent 0 0 R /MediaBox [0 0 {self.page_width} {self.page_height}] "
                f"/Resources << /Font << /F1 {font1} 0 R /F2 {font2} 0 R >> >> "
                f"/Contents {content_obj} 0 R >>".encode("latin-1")
            )
            page_ids.append(page_obj)

        kids = " ".join(f"{pid} 0 R" for pid in page_ids)
        pages_obj = add_object(
            f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("latin-1")
        )

        for pid in page_ids:
            objects[pid - 1] = objects[pid - 1].replace(b"/Parent 0 0 R", f"/Parent {pages_obj} 0 R".encode("latin-1"))

        catalog_obj = add_object(f"<< /Type /Catalog /Pages {pages_obj} 0 R >>".encode("latin-1"))

        pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for idx, obj in enumerate(objects, start=1):
            offsets.append(len(pdf))
            pdf.extend(f"{idx} 0 obj\n".encode("latin-1"))
            pdf.extend(obj)
            pdf.extend(b"\nendobj\n")

        xref_offset = len(pdf)
        pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
        pdf.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
        pdf.extend(
            f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_obj} 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("latin-1")
        )
        path.write_bytes(pdf)


def wrap_line(text: str, width: int):
    if len(text) <= width:
        return [text]
    parts = []
    current = text
    while len(current) > width:
        split_at = current.rfind(" ", 0, width)
        if split_at <= 0:
            split_at = width
        parts.append(current[:split_at])
        current = current[split_at:].lstrip()
    parts.append(current)
    return parts


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_pdf():
    pdf = SimplePDF()
    pdf.heading("Lex and Yacc Lab Programs", size=20)
    pdf.paragraph("This document contains all 10 Lex and Yacc programs prepared in the project workspace.")
    pdf.paragraph("Each section includes the lexer, parser, and a blank placeholder box where you can place an output screenshot later.")

    for folder_name, title in PROGRAMS:
        folder = ROOT / folder_name
        lexer = folder / "lexer.l"
        parser = folder / "parser.y"

        pdf.heading(title, size=16)
        pdf.paragraph(f"Folder: {folder_name}")

        pdf.subheading("Lexer (lexer.l)")
        pdf.code_block(read_text(lexer))

        pdf.subheading("Parser (parser.y)")
        pdf.code_block(read_text(parser))

        pdf.output_placeholder()

    pdf.save(OUTPUT)


if __name__ == "__main__":
    build_pdf()
    print(f"Generated: {OUTPUT}")
