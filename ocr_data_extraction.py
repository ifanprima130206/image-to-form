import cv2
import pytesseract
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration values
tesseract_cmd = os.getenv("TESSERACT_PATH")
image_path = os.getenv("IMAGE_PATH")
output_dir = os.getenv("OUTPUT_DIR")

# Set Tesseract command path
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

print("Starting image processing...")

# Generate unique filename if duplicate exists
def get_unique_filename(base_path):
    if not os.path.exists(base_path):
        return base_path
    name, ext = os.path.splitext(base_path)
    i = 1
    while os.path.exists(f"{name} [{i}]{ext}"):
        i += 1
    return f"{name} [{i}]{ext}"

try:
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found or invalid path.")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply threshold for better OCR accuracy
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Create output directory if not exist
    os.makedirs(output_dir, exist_ok=True)

    # Save processed image
    base_output = os.path.join(output_dir, "image_processed.jpg")
    unique_output = get_unique_filename(base_output)
    cv2.imwrite(unique_output, thresh)
    print(f"Processed image saved as '{unique_output}'")

    # Run OCR
    print("Extracting text with Tesseract...")
    extracted_text = pytesseract.image_to_string(thresh, lang="ind")

    print("Parsing structured data...")

    # Store cleaned extraction results
    data_ktp = {}

    # Regex patterns to extract KTP fields
    patterns = {
        "NIK": r"NIK\s*[:\-]?\s*(.*)",
        "Nama": r"Nama\s*[:\-]?\s*(.*)",
        "Jenis Kelamin": r"Jenis Kelamin\s*[:\-]?\s*(.*)",
        "Golongan Darah": r"Gol\.?\s*Darah\s*[:\-]?\s*(.*)",
        "Alamat": r"Alamat\s*[:\-]?\s*(.*)",
        "RT/RW": r"RT/?RW\s*[:\-]?\s*(.*)",
        "Kel/Desa": r"Kel/?Desa\s*[:\-]?\s*(.*)",
        "Kecamatan": r"Kecamatan\s*[:\-]?\s*(.*)",
        "Agama": r"Agama\s*[:\-]?\s*(.*)",
        "Status Perkawinan": r"Status Perkawinan\s*[:\-]?\s*(.*)",
        "Pekerjaan": r"Pekerjaan\s*[:\-]?\s*(.*)",
        "Kewarnegaraan": r"Kewarnegaraan\s*[:\-]?\s*(.*)",
        "Berlaku Hingga": r"Berlaku Hingga\s*[:\-]?\s*(.*)"
    }

    # Extract each field
    for key, pattern in patterns.items():
        match = re.search(pattern, extracted_text)
        if match:
            data_ktp[key] = match.group(1).strip()

    # Display structured results
    print("\n" + "=" * 40)
    print("STRUCTURED EXTRACTION RESULT")
    print("=" * 40)
    for key, value in data_ktp.items():
        print(f"{key.ljust(20)}: {value}")

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error occurred: {e}")

print("\nProcess completed.")
