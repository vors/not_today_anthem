#!/usr/bin/env python3
import argparse
import os

from pdf2image import convert_from_path
from PIL import Image


def process_pdf(input_pdf, output_pdf, dpi=200):
    """
    Convert a multi-page PDF into a single long-page PDF by stitching
    the pages vertically. Each PDF page is converted to an image and then combined.

    :param input_pdf: Path to the input PDF file.
    :param output_pdf: Path to save the output single-page PDF.
    :param dpi: DPI resolution for the conversion.
    """
    try:
        # Convert each page in the PDF to an image.
        images = convert_from_path(input_pdf, dpi=dpi)
    except Exception as e:
        print(f"Error converting {input_pdf} to images: {e}")
        return

    if not images:
        print(f"No pages found in {input_pdf}")
        return

    # Compute the maximum width and total height for the final image.
    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    # Create a new blank image (white background) that will hold all pages.
    stitched_image = Image.new("RGB", (max_width, total_height), color=(255, 255, 255))

    # Paste each page image into the correct vertical position.
    current_y = 0
    for img in images:
        stitched_image.paste(img, (0, current_y))
        current_y += img.height

    # Save the stitched image as a PDF.
    stitched_image.save(output_pdf, "PDF", resolution=dpi)
    print(f"Processed '{input_pdf}' -> '{output_pdf}'")


def process_folder(input_folder, output_folder, dpi=200):
    """
    Process each PDF file from the input folder and save a modified PDF
    (with a single long page) into the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = os.path.join(output_folder, filename)
            process_pdf(input_pdf_path, output_pdf_path, dpi)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert multi-page PDFs into a single long page PDF by stitching pages vertically."
    )
    parser.add_argument(
        "input_folder", help="Input folder containing PDFs (flat structure)"
    )
    parser.add_argument(
        "output_folder", help="Output folder where modified PDFs will be saved"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI resolution for converting pages (default: 200)",
    )
    args = parser.parse_args()

    process_folder(args.input_folder, args.output_folder, args.dpi)
