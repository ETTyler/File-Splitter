import fitz
import os
import argparse
import re
from PyPDF2 import PdfWriter, PdfReader
import sys


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


def split_pdf(input_pdf_path, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the PDF using PyMuPDF
    pdf_document = fitz.open(input_pdf_path)

    # Load the PDF using PyPDF2 for writing
    pdf_reader = PdfReader(input_pdf_path)

    # Extract names and corresponding pages
    name_pages = extract_names_and_pages(pdf_document)

    # Split and save individual PDFs
    for name, pages in name_pages.items():
        writer = PdfWriter()
        for page_num in pages:
            writer.add_page(pdf_reader.pages[page_num])
        # Sanitize the name for use in filenames
        safe_name = re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")
        output_pdf_path = os.path.join(output_dir, f"{safe_name}-P11D.pdf")
        with open(output_pdf_path, "wb") as output_pdf_file:
            writer.write(output_pdf_file)
            print(f"Created {output_pdf_path}")

    print("PDF split completed.")


def main():
    parser = argparse.ArgumentParser(
        description="Split PDF based on the second line of each page."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="P11Ds",
        help='Output directory to store split PDFs (default: "P11Ds")',
    )

    args = parser.parse_args()

    input_pdf = None
    while not input_pdf:
        input_pdf = input(
            "Please enter the name of the PDF file (in the current directory): "
        )
        if not os.path.isfile(input_pdf):
            print(f"The file '{input_pdf}' does not exist. Please try again.")
            input_pdf = None

    split_pdf(input_pdf, args.output_dir)


if __name__ == "__main__":
    main()
