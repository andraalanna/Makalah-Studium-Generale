# Makalah-Studium-Generale

**Analisis Perdagangan Elektronik (HS 84–85)** 🔧

Proyek ini mengolah data ekspor dan impor komoditas HS 84 dan HS 85 (elektronik) dari file Excel BPS, lalu menghasilkan tabel ringkasan, neraca perdagangan, dan grafik.

---

## 📌 Ringkasan
- Membaca file mentah di `data/raw/` (file ekspor gabungan dan file impor per-tahun).
- Menyusun tabel ringkas untuk ekspor dan impor HS84 & HS85 (2020–2025).
- Menghitung neraca perdagangan (export − import) per tahun.
- Menyimpan output di `outputs/tables/` dan grafik di `outputs/figures/`.

---

## 🔧 Dependencies
Pastikan Python 3.10+ terpasang.

Install dependency:

```bash
python -m pip install -r requirements.txt
```

Rekomendasi di `requirements.txt`:
- pandas >= 1.5
- openpyxl >= 3.1
- matplotlib >= 3.8

---

## 📁 Struktur data (harus ada di `data/raw/`)
- `exim_ekspor_2020_2024.xlsx` — file ekspor 2020–2024
- `exim_ekspor_2025.xlsx` — file ekspor 2025
- `exim_impor_YYYY.xlsx` — file impor per tahun (contoh: `exim_impor_2020.xlsx`, dst.)

> Catatan: Nama file harus sesuai pola di atas karena script mencari file berdasarkan pola tersebut.

---

## ▶️ Cara menjalankan
Jalankan script utama dari folder proyek (root):

```bash
python -m src.main
```

Script akan:
1. Membangun tabel ekspor jika file `outputs/tables/ekspor_ringkas_hs84_85_2020_2025.csv` belum ada atau kosong.
2. Membangun tabel impor dari file `exim_impor_*.xlsx` jika `outputs/tables/impor_ringkas_hs84_85_2020_2025.csv` belum ada atau kosong.
3. Menghasilkan `neraca_hs84_85_2020_2025.csv` dan versi `.xlsx` di `outputs/tables/`.
4. Menyimpan grafik di `outputs/figures/`.

---

## 🧩 Modul penting
- `src/bps_reader.py` — fungsi pembaca file Excel BPS (mengekstrak kolom Totals, HS codes).
- `src/export_pipeline.py` — menyusun tabel ekspor dari file Excel gabungan.
- `src/import_pipeline.py` — menyusun tabel impor dari file per-tahun.
- `src/trade_balance.py` — menggabungkan ekspor + impor menjadi neraca perdagangan.
- `src/plot_trade.py` — membuat grafik export vs import dan neraca.
- `src/main.py` — entrypoint yang mengorkestrasi seluruh alur.
- `src/config.py` — konstanta path (ubah jika perlu).

---

## ✅ Output yang dihasilkan
- `outputs/tables/ekspor_ringkas_hs84_85_2020_2025.csv` / `.xlsx`
- `outputs/tables/impor_ringkas_hs84_85_2020_2025.csv` / `.xlsx`
- `outputs/tables/neraca_hs84_85_2020_2025.csv` / `.xlsx`
- Grafik di `outputs/figures/`

---

## 💡 Tips & Troubleshooting
- Jika muncul error `FileNotFoundError`, pastikan file Excel input ada dan namanya sesuai pola yang dicari (`exim_ekspor_*.xlsx` atau `exim_impor_*.xlsx`).
- Untuk debugging, buka `src/main.py` dan jalankan hanya `_ensure_exports()` atau `_ensure_imports()` agar lebih cepat memeriksa pipeline tertentu.
- Kode mengharapkan kolom 'Totals' di header file impor; jika tidak ada, pembaca akan memunculkan error.

---

## 📝 Lisensi & Kontak
- Penulis: Andra
- Jika perlu bantuan lebih lanjut atau ingin saya taruh README di root repo juga, beri tahu saya.

