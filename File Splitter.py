import fitz
import os
import re
from PyPDF2 import PdfWriter, PdfReader

# create output directory
output_dir = "P11D_PDFs"
os.makedirs(output_dir, exist_ok=True)

# Set file path to HMRC produced PDF
input_pdf_path = ""
pdf_document = fitz.open(input_pdf_path)
pdf_reader = PdfReader(input_pdf_path)


# Function to extract names and corresponding pages
def extract_names_and_pages(pdf_document):
    name_pages = {}
    num_pages = len(pdf_document)
    for page_num in range(1, num_pages):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        lines = text.split("\n")
        if len(lines) > 1:
            name = lines[1].strip()
            if name not in name_pages:
                name_pages[name] = []
            name_pages[name].append(page_num)
    return name_pages


# Gets the name from each page and the corresponding page number so they can be split into individual PDFs
name_pages = extract_names_and_pages(pdf_document)

# Saves the PDFs to the directory of the script
for name, pages in name_pages.items():
    writer = PdfWriter()
    for page_num in pages:
        writer.add_page(pdf_reader.pages[page_num])
    # Sanitize the name for use in filenames
    safe_name = re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")
    output_pdf_path = os.path.join(output_dir, f"{safe_name}_P11D.pdf")
    with open(output_pdf_path, "wb") as output_pdf_file:
        writer.write(output_pdf_file)
        print(f"Created {output_pdf_path}")

print("PDF split completed.")
