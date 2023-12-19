from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.text import WD_LINE_SPACING
from docx.enum.section import WD_SECTION 

def format_manuscript(file_path):
    doc = Document(file_path)

    # 1. Set margins and bleeds
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # 2. Headers, footers, and page numbers
    # This is more complex and depends on your specific requirements

    # 3. Font and Size
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    # 4. Indents, spaces, and rags
    for paragraph in doc.paragraphs:
        paragraph_format = paragraph.paragraph_format
        paragraph_format.first_line_indent = Inches(0.3)
        paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_THREE

        # Justify alignment
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

    # 5. Widows and orphans (handled automatically in Word)

    # 6. Page Breaks
    # Use doc.add_page_break() where needed

    # 7. Trim size (handled during printing, not in Word doc)

    # 8. Chapters formatting
    # You need to identify where new chapters start and ensure they begin on the right page

    # Save the formatted document
    formatted_file_path = "formatted_" + file_path
    doc.save(formatted_file_path)
    return formatted_file_path

# Example usage
formatted_file = format_manuscript('path_to_your_manuscript.docx')
