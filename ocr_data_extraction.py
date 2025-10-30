import cv2
import pytesseract
import os
import re
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

    print("Starting data parsing...")
    
    # Kita buat dictionary kosong untuk menyimpan hasil bersihnya
    data_ktp = {}

    # Pola Regex: cari kata "Nama", ikuti spasi/angka/titik dua, lalu ambil sisa barisnya
    try:
        match = re.search(r"NIK\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['NIK'] = match.group(1).strip()

        match = re.search(r"Nama\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Nama'] = match.group(1).strip()

        match = re.search(r"Jenis Kelamin\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Jenis Kelamin'] = match.group(1).strip()

        match = re.search(r"Gol\.?\s*Darah\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Golongan Darah'] = match.group(1).strip()

        match = re.search(r"Alamat\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Alamat'] = match.group(1).strip()

        match = re.search(r"RT/?RW\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['RT/RW'] = match.group(1).strip()

        match = re.search(r"Kel/?Desa\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Kel/Desa'] = match.group(1).strip()

        match = re.search(r"Kecamatan\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Kecamatan'] = match.group(1).strip()

        match = re.search(r"Agama\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Agama'] = match.group(1).strip()

        match = re.search(r"Status Perkawinan\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Status Perkawinan'] = match.group(1).strip()

        match = re.search(r"Pekerjaan\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Pekerjaan'] = match.group(1).strip()

        match = re.search(r"Kewarnegaraan\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Kewarnegaraan'] = match.group(1).strip()

        match = re.search(r"Berlaku Hingga\s*[:\-]?\s*(.*)", extracted_text)
        if match:
                data_ktp['Berlaku Hingga'] = match.group(1).strip()



    except Exception as e:
        print(f"Error parsing Nama: {e}")


    print("\n" + "=" * 40)
    print("HASIL EKSTRAKSI TERSTRUKTUR")
    print("=" * 40)
    
    for key, value in data_ktp.items():
        print(f"{key.ljust(20)}: {value}")

except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error occurred: {e}")

print("\nProcess completed.")
