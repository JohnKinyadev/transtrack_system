from fpdf import FPDF


def simple_pdf_report(title, rows, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Helvetica", size=10)
    for row in rows:
        pdf.multi_cell(0, 8, " | ".join(str(value) for value in row))
    pdf.output(output_path)
    return output_path
