import cv2
import pytesseract
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration values from .env
tesseract_cmd = os.getenv("TESSERACT_PATH")
image_path = os.getenv("IMAGE_PATH")
output_dir = os.getenv("OUTPUT_DIR")

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

print("Starting image processing...")

# Generate a unique filename if one already exists
def get_unique_filename(base_path):
    if not os.path.exists(base_path):
        return base_path
    name, ext = os.path.splitext(base_path)
    i = 1
    while os.path.exists(f"{name} [{i}]{ext}"):
        i += 1
    return f"{name} [{i}]{ext}"

try:
    # Load the input image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image file not found or invalid path.")

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to improve OCR accuracy
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save processed image with a unique name
    base_output = os.path.join(output_dir, "image_processed.jpg")
    unique_output = get_unique_filename(base_output)
    cv2.imwrite(unique_output, thresh)
    print(f"Processed image saved as '{unique_output}'")

    # Extract text using Tesseract OCR
    print("Starting text extraction with Tesseract...")
    extracted_text = pytesseract.image_to_string(thresh, lang="ind")

    # Display OCR result
    print("\n" + "=" * 40)
    print("OCR TEXT EXTRACTION RESULT")
    print("=" * 40)
    print(extracted_text)

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error occurred: {e}")

print("\nProcess completed.")
