
from PIL import Image, ExifTags
from pathlib import Path
from collections import Counter
import json
import os

# ==========================================
# PROGRAM ANALISIS METADATA FOTO
# ==========================================

print("=" * 60)
print("          PROGRAM ANALISIS METADATA FOTO")
print("=" * 60)

# Masukkan nama atau lokasi foto
lokasi_foto = input(
    "\nMasukkan nama/lokasi foto (contoh: foto.jpg): "
).strip().strip('"')

foto = Path(lokasi_foto)

# Periksa keberadaan foto
if not foto.is_file():
    print("\nERROR: File foto tidak ditemukan!")
    print("Pastikan lokasi dan nama file sudah benar.")

else:
    try:
        # Baca foto
        with Image.open(foto) as img:
            format_foto = img.format
            lebar, tinggi = img.size
            mode = img.mode
            ukuran_byte = foto.stat().st_size
            total_piksel = lebar * tinggi

            # Ubah salinan gambar menjadi RGB untuk analisis warna
            rgb = img.convert("RGB")

            # ======================================
            # 1. INFORMASI DASAR FOTO
            # ======================================
            print("\n[1] INFORMASI DASAR FOTO")
            print("-" * 40)
            print("Nama file       :", foto.name)
            print("Lokasi file     :", foto.resolve())
            print("Format          :", format_foto)
            print("Ukuran file     :", f"{ukuran_byte:,} byte")
            print("Ukuran file     :", f"{ukuran_byte / 1024:.2f} KB")
            print("Lebar           :", lebar, "piksel")
            print("Tinggi          :", tinggi, "piksel")
            print("Resolusi        :", f"{lebar} x {tinggi}")
            print("Jumlah piksel   :", f"{total_piksel:,}")
            print("Mode warna asli :", mode)
            print("Rasio aspek     :", f"{lebar / tinggi:.3f}")

            # ======================================
            # 2. ANALISIS SUSUNAN ANGKA CITRA
            # ======================================
            print("\n[2] ANALISIS SUSUNAN ANGKA CITRA")
            print("-" * 40)
            print("Citra digital tersusun dari piksel.")
            print("Setiap piksel RGB mempunyai 3 nilai:")
            print("R = Red (merah)")
            print("G = Green (hijau)")
            print("B = Blue (biru)")
            print()
            print("Jumlah piksel      :", f"{total_piksel:,}")
            print("Jumlah nilai RGB   :", f"{total_piksel * 3:,}")
            print("Rentang nilai RGB  : 0 sampai 255")
            print("Perkiraan data RGB :",
                  f"{total_piksel * 3:,} nilai angka")

            # Tampilkan beberapa contoh piksel
            print("\nContoh nilai RGB:")
            batas_x = min(5, lebar)
            batas_y = min(5, tinggi)

            for y in range(batas_y):
                for x in range(batas_x):
                    nilai_rgb = rgb.getpixel((x, y))
                    print(
                        f"Piksel (x={x}, y={y}) = {nilai_rgb}"
                    )

            # ======================================
            # 3. STATISTIK WARNA RGB
            # ======================================
            print("\n[3] STATISTIK WARNA RGB")
            print("-" * 40)

            statistik = {}

            for indeks, nama in enumerate(["R", "G", "B"]):
                kanal = rgb.getchannel(indeks)
                minimum, maksimum = kanal.getextrema()
                rata_rata = sum(kanal.getdata()) / total_piksel

                statistik[nama] = {
                    "minimum": minimum,
                    "maksimum": maksimum,
                    "rata_rata": round(rata_rata, 2)
                }

                print(f"Kanal {nama}:")
                print("  Nilai minimum :", minimum)
                print("  Nilai maksimum:", maksimum)
                print("  Nilai rata-rata:", round(rata_rata, 2))

            # ======================================
            # 4. METADATA EXIF
            # ======================================
            print("\n[4] METADATA EXIF")
            print("-" * 40)

            exif = img.getexif()
            metadata_exif = {}

            if exif:
                for tag_id, value in exif.items():
                    nama_tag = ExifTags.TAGS.get(
                        tag_id, str(tag_id)
                    )

                    # Ubah data bytes menjadi teks hex
                    if isinstance(value, bytes):
                        value = value.hex()

                    # Pastikan dapat disimpan ke JSON
                    metadata_exif[nama_tag] = str(value)
                    print(f"{nama_tag}: {value}")
            else:
                print("Tidak ditemukan metadata EXIF.")

            # ======================================
            # 5. METADATA GPS
            # ======================================
            print("\n[5] METADATA GPS")
            print("-" * 40)

            gps_data = {}

            if exif:
                try:
                    gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)

                    for tag_id, value in gps_ifd.items():
                        nama_tag = ExifTags.GPSTAGS.get(
                            tag_id, str(tag_id)
                        )

                        gps_data[nama_tag] = str(value)
                        print(f"{nama_tag}: {value}")

                    if not gps_data:
                        print("Tidak ada informasi GPS.")
                except (KeyError, AttributeError, TypeError):
                    print("Informasi GPS tidak tersedia.")
            else:
                print("Tidak ada informasi GPS.")

            # ======================================
            # 6. INFORMASI TAMBAHAN
            # ======================================
            print("\n[6] INFORMASI TAMBAHAN")
            print("-" * 40)

            print("File dapat dibaca :", "Ya")
            print("Format gambar     :", format_foto)
            print("Total kanal RGB   :", 3)
            print("Rentang warna     :", "0-255 per kanal")

            if total_piksel >= 8_000_000:
                kategori = "Resolusi tinggi"
            elif total_piksel >= 2_000_000:
                kategori = "Resolusi menengah"
            else:
                kategori = "Resolusi di bawah 2 megapiksel"

            print("Kategori resolusi :", kategori)

            # ======================================
            # 7. SIMPAN HASIL KE JSON
            # ======================================
            hasil = {
                "informasi_file": {
                    "nama": foto.name,
                    "format": format_foto,
                    "ukuran_byte": ukuran_byte,
                    "lokasi": str(foto.resolve())
                },
                "informasi_citra": {
                    "lebar": lebar,
                    "tinggi": tinggi,
                    "total_piksel": total_piksel,
                    "megapiksel": round(
                        total_piksel / 1_000_000, 2
                    ),
                    "mode_warna_asli": mode,
                    "rasio_aspek": round(lebar / tinggi, 3)
                },
                "analisis_rgb": {
                    "jumlah_nilai_rgb": total_piksel * 3,
                    "statistik": statistik,
                    "contoh_5x5_piksel": [
                        [
                            list(rgb.getpixel((x, y)))
                            for x in range(batas_x)
                        ]
                        for y in range(batas_y)
                    ]
                },
                "metadata_exif": metadata_exif,
                "metadata_gps": gps_data
            }

            nama_json = foto.stem + "_hasil_analisis.json"
            lokasi_json = Path.cwd() / nama_json

            with open(
                lokasi_json, "w", encoding="utf-8"
            ) as file:
                json.dump(
                    hasil,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            # ======================================
            # 8. SELESAI
            # ======================================
            print("\n[7] HASIL ANALISIS")
            print("-" * 40)
            print("Analisis berhasil dilakukan!")
            print("File hasil JSON:", lokasi_json.resolve())
            print("\n" + "=" * 60)
            print("              PROGRAM SELESAI")
            print("=" * 60)

    except Exception as error:
        print("\nTerjadi kesalahan saat menganalisis foto:")
        print(error)
