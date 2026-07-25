# Smart Inventory API – Presentasi untuk Stakeholder

## Executive Summary

Smart Inventory API adalah platform backend yang dirancang khusus untuk mendukung proses operasional bisnis modern. Sistem ini menggabungkan manajemen inventaris, pengelolaan transaksi, dan integrasi pembayaran dalam satu solusi terpadu yang aman, scalable, dan mudah diintegrasikan dengan layanan pihak ketiga.

Dengan teknologi FastAPI terkini, aplikasi ini menjamin performa tinggi, dokumentasi otomatis, dan kemampuan deployment yang fleksibel. Tim dapat langsung memulai operasional tanpa perlu setup infrastructure yang rumit.

## Business Value

### 1. Efisiensi Operasional
- **Pengelolaan terpusat**: Satu platform untuk produk, pemasok, pelanggan, dan transaksi
- **Otomasi proses**: Webhook pembayaran memproses notifikasi pembayaran secara real-time
- **Laporan admin**: Fitur monitoring untuk melacak status pembayaran dan transaksi

### 2. Keamanan dan Keandalan
- Autentikasi berbasis token JWT untuk akses yang terkontrol
- Role-based access control (RBAC) untuk membatasi akses berdasarkan peran pengguna
- Webhook signature verification untuk memastikan notifikasi pembayaran asli
- Logging dan audit trail untuk compliance dan troubleshooting

### 3. Integrasi Pembayaran yang Fleksibel
- Dukungan sandbox Midtrans untuk testing tanpa risiko
- Arsitektur adapter-based untuk penambahan provider pembayaran baru
- Pemrosesan webhook idempotent untuk mencegah duplikasi transaksi
- API untuk refund, cancel, dan status inquiry pembayaran

### 4. Skalabilitas
- Dirancang dengan repository pattern dan dependency injection
- Database abstraction layer untuk kemudahan migrasi database
- Middleware untuk horizontal scaling dan load balancing

## Technical Overview

### Arsitektur
```
┌─────────────────┐
│   Client/App    │
├─────────────────┤
│  FastAPI Server │
│   (Port 8000)   │
├─────────────────┤
│   Auth Layer    │
│  (JWT + RBAC)   │
├─────────────────┤
│   Business      │
│   Services      │
├─────────────────┤
│  Repository     │
│  Layer          │
├─────────────────┤
│  Database       │
│ (MySQL/SQLite)  │
└─────────────────┘
         ↕
    ┌──────────────┐
    │   Midtrans   │
    │   (Payment)  │
    └──────────────┘
```

### Stack Teknologi
- **Framework**: FastAPI (Python 3.8+)
- **Database**: SQLAlchemy ORM (MySQL/SQLite compatible)
- **Authentication**: JWT + passlib
- **Request Validation**: Pydantic v2
- **Testing**: pytest + TestClient
- **Middleware**: Custom CORS, Rate Limiting, Security Headers, Logging

### Modul Utama
- **Models**: User, Product, Supplier, Customer, Transaction, Payment
- **Services**: Business logic untuk produk, customer, transaksi, pembayaran
- **Repositories**: Data access layer dengan base repository
- **Routers**: API endpoints terstruktur per resource
- **Middleware**: Security dan observability
- **Auth**: Login, register, token refresh, role-based access

## API Overview

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoint Kategori

#### A. Autentikasi
- `POST /auth/register` – Registrasi pengguna baru
- `POST /auth/login` – Login dan dapatkan token
- `POST /auth/refresh` – Perpanjang token

#### B. Inventaris
- `GET /products` – Daftar produk
- `POST /products` – Tambah produk
- `GET /suppliers` – Daftar pemasok
- `GET /customers` – Daftar pelanggan

#### C. Transaksi
- `GET /transactions` – Daftar transaksi
- `POST /transactions` – Buat transaksi
- `GET /transactions/{id}` – Detail transaksi

#### D. Pembayaran
- `POST /payments/initiate` – Mulai proses pembayaran
- `POST /payments/webhook` – Terima notifikasi dari Midtrans

#### E. Admin
- `GET /admin/payments/` – Daftar semua pembayaran
- `POST /admin/payments/{id}/retry` – Ulangi pembayaran
- `POST /admin/payments/{id}/refund` – Refund pembayaran
- `POST /admin/payments/{id}/cancel` – Batalkan pembayaran

### Status Pembayaran
| Status | Arti | Aksi Berikutnya |
|--------|------|-----------------|
| `pending` | Menunggu pembayaran | Pelanggan transfer dana |
| `paid` | Pembayaran diterima | Transaksi completed otomatis |
| `failed` | Pembayaran ditolak | Admin dapat retry |
| `expired` | Waktu pembayaran habis | Admin dapat retry atau cancel |
| `refunded` | Uang dikembalikan | Transaksi ditandai refunded |
| `canceled` | Pembayaran dibatalkan | Transaksi ditandai canceled |

## Deployment Notes

### Prasyarat
- Python 3.8 atau lebih baru
- pip untuk package management
- Database (MySQL atau SQLite)
- Akun Midtrans untuk integrasi pembayaran

### Instalasi

1. Clone repository dan masuk ke folder
```bash
git clone <repository-url>
cd sales_py
```

2. Buat virtual environment
```bash
python -m venv venv
source venv/bin/activate  # di macOS/Linux
# atau
venv\Scripts\activate  # di Windows
```

3. Instal dependencies
```bash
pip install -r requirements.txt
```

4. Konfigurasi environment
```bash
# Edit file .env
MIDTRANS_SERVER_KEY="SB-Mid-server-3JWScOa4pa0QJjHG4vAEzCmh"
MIDTRANS_CLIENT_KEY="SB-Mid-client-cSoG5C-yKiBSkgTj"
MIDTRANS_ENVIRONMENT="sandbox"
EMAIL_SYSTEM="jiwagila023@gmail.com"
PAYMENT_WEBHOOK_SECRET="change-me-in-production"
SECRET_KEY="your-secure-key"
DATABASE_URL="sqlite:///./smart_inventory.db"
```

5. Jalankan aplikasi
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing
```bash
python -m pytest -q
```

Expected output:
```
28 passed in 1.70s
```

### Production Deployment

#### Via Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Via Cloud Platform (GCP/AWS/Azure)
1. Set environment variables di platform
2. Deploy container atau Python app
3. Configure webhook URL di Midtrans dashboard:
   - Success: `https://your-domain.com/api/v1/payments/webhook`
4. Monitor logs untuk memastikan webhook diterima dengan baik

### Security Checklist
- ✅ Environment variable untuk secrets (tidak di-hardcode)
- ✅ HTTPS enforcement di production
- ✅ Webhook signature verification
- ✅ Rate limiting pada API endpoints
- ✅ CORS properly configured
- ✅ SQL injection protection (via SQLAlchemy ORM)
- ✅ JWT token expiration
- ✅ Role-based access control pada admin endpoints

### Monitoring
Rekomendasi tools untuk production:
- **Logging**: ELK Stack, Datadog, atau CloudWatch
- **APM**: New Relic, DataDog APM
- **Alerting**: PagerDuty, Opsgenie untuk notifikasi urgent
- **Dashboard**: Grafana untuk visualisasi metrics

### Maintenance
- Review dan update dependencies setiap bulan
- Monitor API performance dan error rates
- Backup database secara berkala
- Test disaster recovery plan quarterly
- Update Midtrans SDK saat ada versi baru

## Roadmap Fitur
- [ ] Multi-currency support untuk transaksi internasional
- [ ] Advanced reporting dan analytics dashboard
- [ ] Integrasi dengan provider pembayaran lain (DOKU, GCash, Alipay)
- [ ] Mobile app untuk tracking transaksi
- [ ] AI-powered forecasting untuk inventory optimization
- [ ] Subscription/billing management

## Support dan Contact
Untuk pertanyaan teknis atau kebutuhan customization, silakan hubungi tim development atau kirim inquiry ke email support.

---

**Dokumen ini disiapkan untuk presentasi kepada stakeholder dan client. Untuk detail teknis lebih lanjut, referensi ke README.md dan dokumentasi API di `/docs` endpoint.**
