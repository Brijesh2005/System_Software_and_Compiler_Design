from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "lex_yacc_lab_programs.docx"


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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def xml_run(text: str, bold=False, size=None, font=None):
    props = []
    if bold:
        props.append("<w:b/>")
    if size is not None:
        props.append(f'<w:sz w:val="{size}"/>')
        props.append(f'<w:szCs w:val="{size}"/>')
    if font:
        props.append(
            f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
        )
    prop_xml = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    return f'<w:r>{prop_xml}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def xml_paragraph(text="", bold=False, size=None, style=None, font=None):
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{xml_run(text, bold=bold, size=size, font=font)}</w:p>"


def xml_code_paragraph(text: str):
    text = text.replace("\t", "    ")
    return (
        "<w:p>"
        '<w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
        f'{xml_run(text, size=18, font="Courier New")}'
        "</w:p>"
    )


def xml_page_break():
    return "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>"


def build_document_xml():
    body = []
    body.append(xml_paragraph("Lex and Yacc Lab Programs", style="Title"))
    body.append(xml_paragraph("All 10 programs with output image placeholders.", style="Subtitle"))
    body.append(xml_paragraph(""))

    for index, (folder_name, title) in enumerate(PROGRAMS):
        folder = ROOT / folder_name
        lexer = read_text(folder / "lexer.l")
        parser = read_text(folder / "parser.y")

        if index > 0:
            body.append(xml_page_break())

        body.append(xml_paragraph(title, style="Heading1"))
        body.append(xml_paragraph(f"Folder: {folder_name}"))
        body.append(xml_paragraph(""))

        body.append(xml_paragraph("Lexer (lexer.l)", style="Heading2"))
        for line in lexer.splitlines():
            body.append(xml_code_paragraph(line))
        body.append(xml_paragraph(""))

        body.append(xml_paragraph("Parser (parser.y)", style="Heading2"))
        for line in parser.splitlines():
            body.append(xml_code_paragraph(line))
        body.append(xml_paragraph(""))

        body.append(xml_paragraph("Output Screenshot Placeholder", style="Heading2"))
        body.append(xml_paragraph("[ Paste output screenshot here ]", bold=True))
        body.append(xml_paragraph("______________________________________________________________"))
        body.append(xml_paragraph("______________________________________________________________"))
        body.append(xml_paragraph("______________________________________________________________"))
        body.append(xml_paragraph("______________________________________________________________"))

    sect = (
        "<w:sectPr>"
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"'
        ' w:header="720" w:footer="720" w:gutter="0"/>'
        "</w:sectPr>"
    )

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'mc:Ignorable="w14 wp14">'
        f"<w:body>{''.join(body)}{sect}</w:body>"
        "</w:document>"
    )


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""


ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


DOCUMENT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""


STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
</w:styles>
"""


APP_PROPS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>
"""


CORE_PROPS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Lex and Yacc Lab Programs</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
</cp:coreProperties>
"""


def build_docx():
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", ROOT_RELS)
        zf.writestr("docProps/app.xml", APP_PROPS)
        zf.writestr("docProps/core.xml", CORE_PROPS)
        zf.writestr("word/document.xml", build_document_xml())
        zf.writestr("word/styles.xml", STYLES)
        zf.writestr("word/_rels/document.xml.rels", DOCUMENT_RELS)


if __name__ == "__main__":
    build_docx()
    print(f"Generated: {OUTPUT}")
