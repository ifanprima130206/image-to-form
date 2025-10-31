## 🧠 **Tujuan Program**

Kode ini berfungsi untuk melakukan **OCR (Optical Character Recognition)** khusus pada **KTP (Kartu Tanda Penduduk Indonesia)**.
Program ini membaca teks dari gambar menggunakan **Tesseract** OCR, dengan bantuan **OpenCV** untuk pra-pemrosesan gambar seperti konversi ke grayscale dan thresholding.

----------

## ⚙️ **Library yang Digunakan**

1.  **cv2 (OpenCV)** — untuk memproses gambar (grayscale & thresholding).
    
2.  **pytesseract** — untuk mengekstrak teks dari gambar menggunakan Tesseract.
    
3.  **os** — untuk mengelola path file dan direktori.
    
4.  **dotenv** — untuk memuat variabel konfigurasi dari file `.env`.
    

----------

## 📁 **Struktur dan Alur Program**

### 1. **Load Environment Variables**

```python
load_dotenv()
tesseract_cmd = os.getenv("TESSERACT_PATH")
image_path = os.getenv("IMAGE_PATH")
output_dir = os.getenv("OUTPUT_DIR")

```

-   Program membaca konfigurasi dari file `.env`, misalnya:
    
    ```
    TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
    IMAGE_PATH=D:\project\ocr\kartu.jpg
    OUTPUT_DIR=D:\project\ocr\output
    
    ```
    
-   Nilai ini digunakan agar path tidak perlu diketik ulang di dalam kode.
    

----------

### 2. **Set Path ke Tesseract**

```python
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

```

-   Menghubungkan pytesseract dengan lokasi file `tesseract.exe` di sistem.
    

----------

### 3. **Cek dan Buat Nama File Unik**

```python
def get_unique_filename(base_path):
    if not os.path.exists(base_path):
        return base_path
    name, ext = os.path.splitext(base_path)
    i = 1
    while os.path.exists(f"{name} [{i}]{ext}"):
        i += 1
    return f"{name} [{i}]{ext}"

```

-   Jika `image_processed.jpg` sudah ada, maka otomatis membuat nama baru:
    
    -   `image_processed [1].jpg`
        
    -   `image_processed [2].jpg`, dan seterusnya.
        
-   Mencegah file lama tertimpa.
    

----------

### 4. **Pemrosesan Gambar**

```python
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

```

Langkah-langkahnya:

-   Membaca gambar dari path.
    
-   Mengubah gambar ke **grayscale** untuk mengurangi noise.
    
-   Melakukan **thresholding Otsu** agar teks lebih kontras → hasilnya hitam-putih bersih.
    

----------

### 5. **Membuat Folder Output (Jika Belum Ada)**

```python
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

```

-   Membuat folder otomatis jika belum ada.
    

----------

### 6. **Simpan Gambar Hasil Proses**

```python
cv2.imwrite(unique_output, thresh)
print(f"Processed image saved as '{unique_output}'")

```

-   Menyimpan gambar hasil pemrosesan (grayscale + thresholding) ke folder output.
    

----------

### 7. **Ekstraksi Teks dengan Tesseract**

```python
extracted_text = pytesseract.image_to_string(thresh, lang="ind")

```

-   Menjalankan OCR pada gambar hasil pra-pemrosesan.
    
-   Menggunakan bahasa **Indonesia (`lang="ind"`)**, pastikan bahasa ini sudah diinstal di Tesseract.
    

----------

### 8. **Menampilkan Hasil OCR**

```python
print("=" * 40)
print("OCR TEXT EXTRACTION RESULT")
print("=" * 40)
print(extracted_text)

```

-   Menampilkan teks hasil ekstraksi langsung di terminal.
    

----------

### 9. **Penanganan Error**

```python
except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error occurred: {e}")

```

-   Menangani error jika:
    
    -   Path gambar tidak ditemukan.
        
    -   Tesseract belum terinstal / path salah.
        
    -   Atau error lain yang tidak terduga.
        

----------

## ✅ **Output yang Dihasilkan**

1.  File gambar hasil pemrosesan disimpan di `OUTPUT_DIR` (contoh: `image_processed.jpg`).
    
2.  Teks hasil OCR muncul di terminal:
    
    ```
    ========================================
    OCR TEXT EXTRACTION RESULT
    ========================================
    [hasil teks dari gambar]
    
    ```
    

----------

## 🧩 **Kesimpulan**

Script ini sudah **lengkap dan modular**, dengan fitur:

-   ✅ Penggunaan `.env` untuk konfigurasi fleksibel.
    
-   ✅ Deteksi otomatis file duplikat.
    
-   ✅ Pembersihan gambar otomatis untuk akurasi OCR tinggi.
    
-   ✅ Penanganan error yang aman.
    

----------

Apakah kamu mau saya bantu tambahkan versi yang **menyimpan hasil teks ke file `.txt` otomatis** di folder output juga (selain print di terminal)?