# Sistem Rental Alat (Django)

Aplikasi web manajemen rental alat (kamera, drone, lighting, dll) dibangun dengan Django.
Mencakup 6 modul data sesuai kebutuhan:

1. **Data Pengguna** (app `accounts`) — custom User model dengan role Admin/Petugas.
2. **Data Alat** (app `alat`) — CRUD alat, hanya Admin yang bisa tambah/edit/hapus.
3. **Data Penyewaan** (app `penyewaan`) — transaksi sewa alat, kalkulasi otomatis lama sewa & total biaya.
4. **Data Pengembalian** (app `pengembalian`) — pencatatan pengembalian, hitung denda keterlambatan otomatis.
5. **Data Pembayaran** (app `pembayaran`) — pencatatan pembayaran, validasi terhadap sisa tagihan.
6. **Data Laporan** (app `laporan`) — dashboard + 5 laporan (alat tersedia, alat disewa, pendapatan, riwayat penyewaan, data pengembalian).

## Validasi yang diimplementasikan

Semua input tidak boleh kosong (field wajib) dan divalidasi secara kompleks & realistis, di antaranya:

- **Password**: minimal 8 karakter, wajib ada huruf besar, huruf kecil, angka, dan simbol (`accounts/validators.py`).
- **Email & username**: format valid, unik, tidak boleh duplikat.
- **Nomor telepon**: harus format nomor Indonesia yang valid (regex `08xxxxxxxxxx`).
- **Nomor inventaris alat**: format baku `AB-0001`, unik.
- **Tahun pembelian**: tidak boleh sebelum 1990 atau melebihi tahun berjalan.
- **Warna**: hanya huruf.
- **Harga sewa**: harus lebih besar dari Rp1.000.
- **Tanggal sewa**: tidak boleh di masa lalu; tanggal kembali (rencana) harus setelah tanggal sewa; durasi maksimal 90 hari.
- **Alat**: hanya bisa disewa jika berstatus "Tersedia"; status otomatis berubah menjadi "Disewa" saat transaksi dibuat.
- **Pengembalian**: tanggal tidak boleh sebelum tanggal sewa atau di masa depan; catatan kerusakan **wajib diisi** (minimal 10 karakter) jika kondisi alat bukan "Baik"; keterlambatan & denda dihitung otomatis (10% harga sewa harian per hari telat); status alat otomatis diperbarui (Tersedia/Rusak/Maintenance).
- **Pembayaran**: jumlah harus > 0; tanggal tidak boleh sebelum tanggal sewa atau di masa depan; jumlah pembayaran berstatus "Lunas" tidak boleh melebihi sisa tagihan penyewaan terkait.

Validasi diterapkan berlapis: di level `Form` (client-facing, pesan error rapi) **dan** di level `Model.clean()` /
`full_clean()` (agar tetap konsisten walau data dimasukkan lewat Django Admin atau shell).

## Cara menjalankan

```bash
# 1. Buat virtual environment (opsional tapi disarankan)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependency
pip install -r requirements.txt

# 3. Migrasi database
python manage.py makemigrations
python manage.py migrate

# 4. Buat akun superuser (untuk akses /admin/ dan role Admin)
python manage.py createsuperuser

# 5. Jalankan server
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` di browser.

- Halaman **daftar akun**: `/akun/daftar/` — user baru bisa memilih role Admin/Petugas saat registrasi
  (di aplikasi nyata, sebaiknya batasi opsi ini hanya untuk superuser/admin yang membuatkan akun,
  bukan self-registration bebas).
- Panel admin Django: `/admin/`

## Struktur Project

```
rental_app/
├── manage.py
├── requirements.txt
├── rental_project/       # settings, urls, wsgi/asgi
├── accounts/             # Data Pengguna (custom User, login, registrasi)
├── alat/                 # Data Alat
├── penyewaan/             # Data Penyewaan
├── pengembalian/          # Data Pengembalian
├── pembayaran/            # Data Pembayaran
├── laporan/               # Dashboard & Laporan
├── templates/             # base.html, pagination.html
└── static/css/style.css
```

## Catatan

- Database default: SQLite (file `db.sqlite3`, otomatis dibuat saat migrate). Bisa diganti ke PostgreSQL/MySQL
  dengan mengubah `DATABASES` di `rental_project/settings.py`.
- `SECRET_KEY` di `settings.py` masih nilai development — **wajib diganti** sebelum deploy ke production,
  dan set `DEBUG = False` serta `ALLOWED_HOSTS` yang sesuai.
- Field turunan (lama_penyewaan, total_biaya, keterlambatan, denda_keterlambatan) dihitung otomatis oleh
  sistem — tidak diinput manual oleh user, sehingga tidak bisa dimanipulasi lewat form.
