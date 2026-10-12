# Analisis Metadata Foto Menggunakan Python

## Deskripsi
Project ini merupakan tugas mata kuliah Citra Digital untuk menganalisis metadata foto dan membuktikan bahwa citra digital tersusun dari data numerik atau nilai piksel.

## Tujuan
- Membaca informasi dasar foto.
- Mengetahui dimensi dan jumlah piksel.
- Menampilkan contoh nilai piksel RGB.
- Menghitung statistik warna RGB.
- Memeriksa metadata EXIF dan GPS.
- Menyimpan hasil analisis ke dalam file JSON.

## Teknologi
- Python
- Pillow
- JSON
- Visual Studio Code

## File Project
- `analisis_metadata.py`: program utama analisis foto.
- `foto.jpg`: gambar yang dianalisis.
- `foto_hasil_analisis.json`: hasil analisis dalam format JSON.

## Cara Menjalankan

Install library Pillow:

```bash
pip install Pillow
```

Jalankan program:

```bash
python analisis_metadata.py
```

Masukkan nama atau lokasi foto ketika diminta oleh program.

## Kesimpulan
Citra digital tersusun dari piksel yang memiliki nilai numerik. Pada gambar RGB, setiap piksel mempunyai tiga komponen warna, yaitu merah, hijau, dan biru.