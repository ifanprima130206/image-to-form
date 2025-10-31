import cv2
import pytesseract
import os
import re
from dotenv import load_dotenv

load_dotenv()

tesseract_cmd = os.getenv("TESSERACT_PATH")
image_path = os.getenv("IMAGE_PATH")
output_dir = os.getenv("OUTPUT_DIR")

pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

print("Starting image processing...")

def get_unique_filename(base_path):
    if not os.path.exists(base_path):
        return base_path
    name, ext = os.path.splitext(base_path)
    i = 1
    while os.path.exists(f"{name} [{i}]{ext}"):
        i += 1
    return f"{name} [{i}]{ext}"

try:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found or invalid path.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    os.makedirs(output_dir, exist_ok=True)

    base_output = os.path.join(output_dir, "image_processed.jpg")
    unique_output = get_unique_filename(base_output)
    cv2.imwrite(unique_output, thresh)
    print(f"Processed image saved as '{unique_output}'")

    print("Extracting text with Tesseract...")
    extracted_text = pytesseract.image_to_string(thresh, lang="ind")

    print("Parsing structured data...")

    data_ktp = {}
    lines = extracted_text.split('\n')

    for i, line in enumerate(lines):
        if re.search(r"NIK", line):
            try:
                parts = re.split(r"NIK\s*[:1\?]*\s*", line)
                if len(parts) > 1:
                    data_ktp['NIK'] = parts[1].strip().replace("?", "7")
            except Exception as e:
                print(f"Error parsing NIK with split: {e}")
        
        elif re.search(r"Nama", line):
            data_ktp['Nama'] = re.sub(r"Nama\s*[\W\d]*\s*", "", line).strip()
            
        elif re.search(r"TempatT[g]?i Lahir", line):
            data_ktp['Tempat/Tgl Lahir'] = re.sub(r"TempatT[g]?i Lahir\s*[:\-]?\s*", "", line).strip()

        elif re.search(r"A[tl]amat", line):
            data_ktp['Alamat'] = re.sub(r"A[tl]amat\s*[\W\d]*\s*", "", line).strip()

        elif re.search(r"Jenis Kelamin", line):
            match_jk = re.search(r"Jenis Kelamin\s*[\W\d]*\s*(.*?)\s*Gol\.", line)
            if match_jk:
                data_ktp['Jenis Kelamin'] = match_jk.group(1).strip()
            match_gol = re.search(r"Gol\.\s*Darah\s*[:\-]?\s*(.*)", line)
            if match_gol:
                data_ktp['Golongan Darah'] = match_gol.group(1).strip()
        
        elif re.search(r"Berlaku Hingga", line):
            value = re.sub(r"Berlaku Hingga\s*[:\-]?\s*", "", line).strip()
            if "SEUMUR HIDUP" in value:
                data_ktp['Berlaku Hingga'] = "SEUMUR HIDUP"
            else:
                data_ktp['Berlaku Hingga'] = value

        elif re.search(r"RT[I/]RW", line):
            try:
                parts = re.split(r"RT[I/]RW\s*[:1\?]*\s*", line)
                if len(parts) > 1:
                    raw_rt_rw = parts[1].strip() 
                    if len(raw_rt_rw) == 6:
                        formatted_rt_rw = f"{raw_rt_rw[0:3]}/{raw_rt_rw[3:]}"
                        data_ktp['RT/RW'] = formatted_rt_rw
                    else:
                        data_ktp['RT/RW'] = raw_rt_rw
            except Exception as e:
                print(f"Error parsing RT/RW with split: {e}")

                
            try:
                data_ktp['Kel/Desa'] = lines[i+1].replace(":", "").strip()
                data_ktp['Kecamatan'] = lines[i+2].replace(":", "").strip()
                data_ktp['Agama'] = re.sub(r"[\W\d]*", "", lines[i+3]).strip()
                data_ktp['Status Perkawinan'] = lines[i+4].replace(":", "").strip()
                pekerjaan_kotor = lines[i+5].replace(":", "").strip()
                data_ktp['Pekerjaan'] = pekerjaan_kotor.replace("JAKARTA TIMUR", "").strip()
                if "WNI" in pekerjaan_kotor:
                    data_ktp['Kewarganegaraan'] = "WNI"
            except IndexError:
                print("Warning: Reached end of text while parsing relative fields.")

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
