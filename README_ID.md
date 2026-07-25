# Smart Inventory API

Smart Inventory API adalah sistem backend untuk mengelola inventaris, pelanggan, pemasok, transaksi, dan proses pembayaran. Aplikasi ini dibangun dengan FastAPI agar mudah digunakan, cepat dikembangkan, dan siap diintegrasikan dengan layanan lain seperti Midtrans.

## Ringkasan proyek
Smart Inventory API dirancang untuk membantu tim operasional dan bisnis mengelola proses inventaris, pelanggan, pemasok, transaksi, serta pembayaran secara terpusat. Sistem ini menyediakan antarmuka backend yang aman, dapat dikembangkan, dan siap digunakan untuk kebutuhan operasional harian maupun integrasi dengan layanan pembayaran eksternal.

## Fitur utama
- Mengelola produk, pemasok, pelanggan, dan transaksi
- Sistem autentikasi untuk login, register, dan refresh token
- Endpoint AI sederhana untuk forecasting, rekomendasi, dan deteksi anomali
- Middleware keamanan, logging, CORS, rate limiting, dan header keamanan
- Integrasi pembayaran dengan Midtrans dan kerangka DOKU
- Webhook pembayaran untuk memproses status transaksi secara otomatis

## Persiapan awal
Ikuti langkah berikut agar aplikasi dapat berjalan di lingkungan lokal.

1. Buat dan aktifkan virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

2. Instal semua dependensi

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi

```bash
uvicorn app.main:app --reload
```

4. Jalankan pengujian

```bash
python -m pytest -q
```

5. Buka dokumentasi API

Setelah server berjalan, buka:

```text
http://localhost:8000/docs
```

Dokumentasi interaktif ini memudahkan Anda melihat seluruh endpoint yang tersedia.

## Struktur API
Semua endpoint utama menggunakan prefix:

```text
/api/v1
```

Beberapa endpoint penting:
- `/products` untuk mengelola produk
- `/suppliers` untuk mengelola pemasok
- `/customers` untuk mengelola pelanggan
- `/transactions` untuk mengelola transaksi
- `/auth` untuk registrasi, login, dan refresh token
- `/ai/*` untuk fitur AI demo
- `/payments/*` untuk alur pembayaran
- `/admin/payments/*` untuk operasi pembayaran oleh admin

## Peran pengguna
Aplikasi ini mendukung role-based access control. Role yang umum dipakai adalah:
- `admin` untuk operasi administratif
- `staff` untuk mengelola data operasional
- `user` untuk pengguna biasa

Jika Anda ingin memperluas sistem izin, role ini dapat dipakai untuk membatasi akses endpoint tertentu agar hanya user dengan hak tertentu yang bisa mengaksesnya.

## Panduan pembayaran Midtrans
Aplikasi ini sudah dilengkapi dengan alur pembayaran dasar yang siap diuji di sandbox Midtrans.

### Konfigurasi environment
Tambahkan variabel berikut ke file `.env`:

```bash
MIDTRANS_SERVER_KEY="SB-Mid-server-3JWScOa4pa0QJjHG4vAEzCmh"
MIDTRANS_CLIENT_KEY="SB-Mid-client-cSoG5C-yKiBSkgTj"
MIDTRANS_ENVIRONMENT="sandbox"
EMAIL_SYSTEM="jiwagila023@gmail.com"
PAYMENT_WEBHOOK_SECRET="change-me-in-production"
```

### Alur pembayaran
1. Buat transaksi terlebih dahulu melalui endpoint transaksi.
2. Panggil endpoint pembayaran untuk memulai proses pembayaran.
3. Midtrans akan mengirimkan notifikasi webhook saat status pembayaran berubah.
4. Sistem akan memperbarui status transaksi dan pembayaran secara otomatis.

### Endpoint pembayaran

#### 1. Memulai pembayaran
Endpoint ini dipakai untuk membuat record pembayaran baru untuk transaksi yang sudah ada.

```bash
curl -X POST http://localhost:8000/api/v1/payments/initiate \
  -H 'Content-Type: application/json' \
  -d '{"transaction_id": 1, "provider": "midtrans"}'
```

Tujuan endpoint ini adalah menginisialisasi pembayaran berdasarkan transaksi tertentu dan mengirimkan data ke penyedia pembayaran yang dipilih.

#### 2. Menerima webhook Midtrans
Endpoint ini menerima notifikasi dari penyedia pembayaran. Saat webhook masuk, sistem akan memvalidasi tanda tangan, membaca status pembayaran, lalu mengubah status transaksi sesuai hasilnya.

Contoh payload webhook untuk status berhasil:

```bash
curl -X POST http://localhost:8000/api/v1/payments/webhook \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: <sha256-hmac-of-raw-body>' \
  -d '{
    "transaction_time": "2026-07-26 10:00:00",
    "transaction_status": "settlement",
    "transaction_id": "midtrans-sandbox-001",
    "order_id": "txn-1",
    "gross_amount": "10000.00",
    "currency": "IDR",
    "fraud_status": "accept",
    "payment_type": "bank_transfer",
    "status_code": "200",
    "status_message": "midtrans payment notification"
  }'
```

Contoh payload webhook untuk status gagal:

```bash
curl -X POST http://localhost:8000/api/v1/payments/webhook \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: <sha256-hmac-of-raw-body>' \
  -d '{
    "transaction_time": "2026-07-26 10:05:00",
    "transaction_status": "deny",
    "transaction_id": "midtrans-sandbox-002",
    "order_id": "txn-2",
    "gross_amount": "10000.00",
    "currency": "IDR",
    "fraud_status": "accept",
    "payment_type": "bank_transfer",
    "status_code": "201",
    "status_message": "transaction is denied"
  }'
```

Contoh payload webhook untuk status kadaluwarsa:

```bash
curl -X POST http://localhost:8000/api/v1/payments/webhook \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: <sha256-hmac-of-raw-body>' \
  -d '{
    "transaction_time": "2026-07-26 10:10:00",
    "transaction_status": "expire",
    "transaction_id": "midtrans-sandbox-003",
    "order_id": "txn-3",
    "gross_amount": "10000.00",
    "currency": "IDR",
    "fraud_status": "accept",
    "payment_type": "bank_transfer",
    "status_code": "202",
    "status_message": "transaction expired"
  }'
```

Status yang umum dipetakan oleh sistem:
- `settlement` atau `capture` → status internal `paid`
- `deny`, `cancel`, `failure`, `expire`, `expired` → status internal `failed`

Contoh respon sukses dari Midtrans yang lebih realistis:

```json
{
  "status_code": "201",
  "status_message": "Transaksi berhasil diproses",
  "transaction_id": "midtrans-sandbox-001",
  "order_id": "txn-1",
  "gross_amount": "10000.00",
  "currency": "IDR",
  "transaction_status": "settlement",
  "payment_type": "bank_transfer",
  "fraud_status": "accept"
}
```

#### 3. Melihat daftar pembayaran (admin)
Endpoint ini dipakai oleh admin untuk melihat seluruh record pembayaran yang pernah dibuat.

```bash
curl -X GET http://localhost:8000/api/v1/admin/payments/ \
  -H 'Authorization: Bearer <admin-token>'
```

#### 4. Mengulang pembayaran (admin)
Endpoint ini dipakai ketika admin ingin mengirim ulang proses pembayaran untuk record yang sama.

```bash
curl -X POST http://localhost:8000/api/v1/admin/payments/1/retry \
  -H 'Authorization: Bearer <admin-token>'
```

#### 5. Refund pembayaran (admin)
Endpoint ini dipakai untuk menandai pembayaran sebagai dikembalikan.

Request body:

```json
{}
```

Contoh request:

```bash
curl -X POST http://localhost:8000/api/v1/admin/payments/1/refund \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <admin-token>' \
  -d '{}'
```

Contoh respon JSON:

```json
{
  "success": true,
  "payment_id": 1,
  "status": "refunded"
}
```

#### 6. Membatalkan pembayaran (admin)
Endpoint ini dipakai untuk menandai pembayaran sebagai dibatalkan.

Request body:

```json
{}
```

Contoh request:

```bash
curl -X POST http://localhost:8000/api/v1/admin/payments/1/cancel \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <admin-token>' \
  -d '{}'
```

Contoh respon JSON:

```json
{
  "success": true,
  "payment_id": 1,
  "status": "canceled"
}
```

## Catatan penting
- Untuk lingkungan produksi, gunakan secret manager dan verifikasi signature yang lebih spesifik sesuai penyedia pembayaran.
- Webhook sebaiknya diolah secara idempotent agar tidak terjadi duplikasi pemrosesan.
- Saat webhook menunjukkan status `paid`, transaksi akan otomatis dipindahkan ke status `completed`.

## Cara test dari Postman
Bagian ini dibuat supaya tim non-teknis bisa mencoba alur pembayaran dengan mudah.

### 1. Jalankan aplikasi lokal
Pastikan server berjalan terlebih dahulu:

```bash
uvicorn app.main:app --reload
```

### 2. Buka Postman
Buat request baru dengan metode yang sesuai.

### 3. Test endpoint pembayaran
#### A. Buat pembayaran
- Method: `POST`
- URL: `http://localhost:8000/api/v1/payments/initiate`
- Body: raw JSON

```json
{
  "transaction_id": 1,
  "provider": "midtrans"
}
```

#### B. Test webhook sukses
- Method: `POST`
- URL: `http://localhost:8000/api/v1/payments/webhook`
- Header: `Content-Type: application/json`
- Header: `X-Signature: <nilai tanda tangan yang sama dengan body>`
- Body: raw JSON

```json
{
  "transaction_time": "2026-07-26 10:00:00",
  "transaction_status": "settlement",
  "transaction_id": "midtrans-sandbox-001",
  "order_id": "txn-1",
  "gross_amount": "10000.00",
  "currency": "IDR",
  "fraud_status": "accept",
  "payment_type": "bank_transfer",
  "status_code": "200",
  "status_message": "midtrans payment notification"
}
```

#### C. Test webhook gagal
Gunakan body yang sama, tetapi ubah `transaction_status` menjadi `deny`.

#### D. Test webhook kadaluwarsa
Gunakan body yang sama, tetapi ubah `transaction_status` menjadi `expire`.

### 4. Test endpoint admin
Untuk melihat daftar pembayaran atau melakukan refund/cancel, gunakan token admin pada header Authorization.

```text
Authorization: Bearer <admin-token>
```

Contoh endpoint:
- `GET http://localhost:8000/api/v1/admin/payments/`
- `POST http://localhost:8000/api/v1/admin/payments/1/refund`
- `POST http://localhost:8000/api/v1/admin/payments/1/cancel`

### 5. Cek hasil
Setelah request dikirim, pastikan:
- status pembayaran berubah sesuai webhook
- transaksi berubah menjadi `completed` saat pembayaran sukses
- transaksi berubah menjadi `failed` atau `expired` saat webhook menunjukkan kondisi tersebut

## Contoh respon admin
Endpoint admin berikut mengembalikan data ringkas mengenai status pembayaran yang telah diproses:

```json
[
  {
    "id": 1,
    "transaction_id": 7,
    "amount": 10000.0,
    "status": "paid",
    "provider": "midtrans",
    "provider_payment_id": "midtrans-sandbox-001"
  }
]
```

Endpoint ini dapat dipakai untuk monitoring internal, audit, maupun pelacakan status pembayaran oleh tim operasional atau stakeholder.

## Versi formal untuk stakeholder atau client
Proyek ini dikembangkan sebagai solusi backend yang mendukung pengelolaan inventaris dan transaksi secara terstruktur, dengan fokus pada keamanan, skalabilitas, dan kemudahan integrasi. Fitur pembayaran yang tersedia saat ini dirancang untuk mendukung alur transaksi yang aman dan transparan, termasuk pemrosesan webhook, pemantauan status pembayaran, serta tindakan administratif seperti refund dan cancel.

Tujuan utama implementasi ini adalah memberikan fondasi sistem yang siap digunakan untuk proses bisnis nyata, dengan dokumentasi yang memadai sehingga tim internal maupun mitra eksternal dapat memahami alur kerja secara cepat.

## Pengujian
Pengujian untuk alur pembayaran, webhook, dan akses admin sudah tersedia di folder `tests`.
