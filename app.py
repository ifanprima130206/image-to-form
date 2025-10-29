import cv2
import pytesseract
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get paths from .env
tesseract_cmd = os.getenv("TESSERACT_PATH")
image_path = os.getenv("IMAGE_PATH")
output_path = os.getenv("OUTPUT_PATH")

# Set Tesseract command path
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

print("Starting image processing...")

try:
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image file not found or incorrect path.")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding for better OCR accuracy
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    print("Image processed successfully (grayscale & thresholding applied).")

    # Save processed image
    cv2.imwrite(output_path, thresh)
    print(f"Processed image saved as '{output_path}'.")

    # OCR extraction
    print("Starting text extraction with Tesseract...")
    extracted_text = pytesseract.image_to_string(thresh, lang="ind")

    print("\n" + "=" * 40)
    print("OCR TEXT EXTRACTION RESULT")
    print("=" * 40)
    print(extracted_text)

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error occurred: {e}")

print("\nProcess completed.")
