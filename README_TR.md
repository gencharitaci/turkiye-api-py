# Turkiye API (Python/FastAPI)

> **Language / Dil**: [English](README.md) | [Türkçe](README_TR.md)

**Versiyon 1.1.0** | **Production Hazır** ✅

TurkiyeAPI, Türkiye'nin il, ilçe, mahalle ve köy gibi idari bölünmeleri hakkında demografik ve coğrafi verilerle birlikte detaylı bilgiler sağlayan kapsamlı bir REST API'dir.

Bu, [Adem Kurtipek](https://github.com/ubeydeozdmr) tarafından geliştirilen orijinal [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) projesine dayanan bir Python/FastAPI implementasyonudur ve MIT Lisansı altında lisanslanmıştır.

## ✨ Özellikler

### Ana Özellikler

- **FastAPI Framework**: API'ler oluşturmak için modern, hızlı (yüksek performanslı) web framework
- **Çok Dilli Dokümantasyon**: İngilizce ve Türkçe desteğiyle otomatik dil algılama
- **Scalar Dokümantasyonu**: Modern UI ile güzel, interaktif API dokümantasyonu
- **OpenAPI Desteği**: Birden fazla dilde tam OpenAPI 3.0 spesifikasyonu
- **Tip Güvenliği**: Pydantic modelleriyle tam type hints
- **API Versiyonlama**: Sorunsuz geçişler için kapsamlı versiyonlama stratejisi (`/api/v1/...`)

### Güvenlik & Performans 🔒⚡

- **OWASP Güvenlik Başlıkları**: Tüm kritik güvenlik başlıkları uygulandı (CSP, X-Frame-Options, HSTS, vb.)
- **Güvenli Health Endpoint**: Opsiyonel kimlik doğrulama ile ortam-duyarlı detay seviyeleri
- **Redis Önbellekleme**: Otomatik anahtar üretimi ve 30 dakika TTL ile yüksek performanslı dağıtık önbellekleme
- **Rate Limiting**: Dağıtık deployment'lar için Redis destekli yerleşik istek sınırlama
- **CORS Yapılandırması**: Ortam-duyarlı Cross-Origin Resource Sharing
- **GZip Sıkıştırma**: Daha iyi performans için otomatik yanıt sıkıştırma

### Kalite & DevOps 🧪🚀

- **Kapsamlı Test**: Tüm katmanlarda 80+ test (data, services, API, middleware)
- **Otomatik İş Akışları**: Veri ve dokümantasyon senkronizasyonu için GitHub Actions
- **Pre-commit Hooks**: Otomatik kod kalitesi kontrolleri (Black, isort, flake8, Bandit, mypy)
- **Kod Kalitesi**: Mükemmel sürdürülebilirlik ile 9.0/10 kalite skoru
- **Production Hazır**: Docker, Gunicorn, kapsamlı deployment rehberleri ve production config şablonları

### İzleme & Gözlemlenebilirlik 📊

- **Prometheus Metrikleri**: `/metrics` endpoint'inde yerleşik metrikler
- **Yapılandırılmış Loglama**: Yapılandırılabilir seviyelerle JSON loglama
- **Health Check'ler**: Bağımlılık durumu izleme ile geliştirilmiş health endpoint

## Gereksinimler

- Python 3.8+
- pip

## Kurulum

1. Repository'yi klonlayın:

```bash
git clone https://github.com/gencharitaci/turkiye-api-py.git
cd turkiye-api-py
```

2. Virtual environment oluşturun:

```bash
python -m venv venv

# Windows'ta
venv\Scripts\activate

# macOS/Linux'ta
source venv/bin/activate
```

3. Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

4. `.env` dosyası oluşturun:

```bash
# Development için
cp .env.example .env

# Production için (önerilen)
cp .env.production.recommended .env
```

Ayarları özelleştirmek için `.env` dosyasını düzenleyin. Detaylar için [Yapılandırma](#yapılandırma) bölümüne bakın.

5. (Opsiyonel) Kod kalitesi için pre-commit hooks kurun:

```bash
pip install pre-commit
pre-commit install
```

## Uygulamayı Çalıştırma

### Development Modu

```bash
python run.py
```

API şu adreste erişilebilir olacaktır: `http://localhost:8181`

### Production Modu

Production ortamı için Gunicorn + Uvicorn workers veya Docker kullanmanızı öneriyoruz:

**Seçenek 1: Docker (Önerilen)**

```bash
docker-compose up -d
```

**Seçenek 2: Gunicorn**

```bash
gunicorn -c gunicorn.conf.py app.main:app
```

**Seçenek 3: Hızlı Başlangıç Scriptleri**

```bash
# Linux/Mac
chmod +x start-production.sh
./start-production.sh

# Windows
start-production.bat
```

Detaylı production deployment talimatları için [DEPLOYMENT_TR.md](docs/DEPLOYMENT_TR.md) veya [DEPLOYMENT_EN.md](docs/DEPLOYMENT_EN.md) dosyasına bakın.

## Yapılandırma

### Ortam Değişkenleri

Ana yapılandırma seçenekleri (tam liste için `.env.production.recommended` dosyasına bakın):

```env
# Uygulama
ENVIRONMENT=production
DEBUG=false
PORT=8181
WORKERS=4

# Güvenlik (Production için KRİTİK)
EXPOSE_SERVER_HEADER=false
HEALTH_CHECK_DETAILED=false
HEALTH_CHECK_AUTH_ENABLED=true
HEALTH_CHECK_PASSWORD=güvenli-şifreniz

# Redis (önbellekleme ve rate limiting için)
REDIS_URL=redis://localhost:6379/0

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100

# CORS
ALLOWED_ORIGINS=https://yourdomain.com
```

### Güvenlik Yapılandırması

**Production Güvenlik Kontrol Listesi**:

- ✅ Bilgi açığını en aza indirmek için `HEALTH_CHECK_DETAILED=false` ayarlayın
- ✅ Hassas ortamlar için `HEALTH_CHECK_AUTH_ENABLED=true` etkinleştirin
- ✅ Güçlü `HEALTH_CHECK_PASSWORD` belirleyin
- ✅ Teknoloji yığını açığını önlemek için `EXPOSE_SERVER_HEADER=false` tutun
- ✅ `ALLOWED_ORIGINS`'i gerçek domain'lerinizle yapılandırın
- ✅ Reverse proxy (nginx/Apache) ile HTTPS etkinleştirin

Tüm OWASP güvenlik başlıkları otomatik olarak uygulanır:

- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Content-Security-Policy (yapılandırıldı)
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy (geolocation, microphone, camera devre dışı)
- Strict-Transport-Security (sadece production)

## API Dokümantasyonu

Sunucu çalıştıktan sonra, dokümantasyona birden fazla dilde erişebilirsiniz:

- **Otomatik Dil Algılama**: <http://localhost:8181/docs> (Tarayıcı diline göre yönlendirir)
- **İngilizce Dokümantasyon**: <http://localhost:8181/docs/en> (Interactive Scalar UI)
- **Türkçe Dokümantasyon**: <http://localhost:8181/docs/tr> (İnteraktif Scalar UI)
- **İngilizce OpenAPI Spec**: <http://localhost:8181/openapi-en.json>
- **Türkçe OpenAPI Spec**: <http://localhost:8181/openapi-tr.json>

Dokümantasyon otomatik olarak tarayıcı dilinizi algılar ve içeriği İngilizce veya Türkçe olarak gösterir. Ayrıca sağ üst köşedeki dil seçici butonlarını kullanarak manuel olarak dil değiştirebilirsiniz.

Daha fazla detay için `/docs` endpoint'indeki interaktif dokümantasyona bakın.

## Dokümantasyon Rehberleri

`guides/` klasörü, [turkiye-api-docs](https://github.com/ubeydeozdmr/turkiye-api-docs) repository'sinden senkronize edilen kapsamlı dokümantasyon içerir.

**Otomatik Senkronizasyon**: Dokümantasyon her gün saat 02:00 UTC'de GitHub Actions ile otomatik olarak güncellenir.

**Manuel Senkronizasyon**:

```bash
# Linux/Mac
./scripts/sync-guides.sh

# Windows
scripts\sync-guides.bat
```

Senkronizasyon mekanizması hakkında detaylı bilgi için [GUIDES_SYNC.md](docs/GUIDES_SYNC.md) dosyasına bakın.

## Veri Senkronizasyonu

`app/data/` klasörü, [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) repository'sinden senkronize edilen idari verileri (iller, ilçeler, vb.) içerir.

**Otomatik Senkronizasyon**: Veriler her hafta Pazar günü saat 03:00 UTC'de GitHub Actions ile otomatik olarak güncellenir.

**Manuel Senkronizasyon**:

```bash
# Linux/Mac
./scripts/sync-data.sh

# Windows
scripts\sync-data.bat
```

**Özellikler**:

- ✅ Otomatik JSON doğrulama
- ✅ Güncelleme öncesi yedekleme
- ✅ Haftalık zamanlanmış senkronizasyon
- ✅ Manuel tetikleme mevcut

Veri senkronizasyonu hakkında detaylı bilgi için [DATA_SYNC.md](docs/DATA_SYNC.md) dosyasına bakın.

## API Endpoint'leri

### Health Check

- `GET /health` - Health check endpoint'i

### İller

- `GET /api/v1/provinces` - Opsiyonel filtrelerle tüm illeri getir
- `GET /api/v1/provinces/{id}` - ID'ye göre belirli ili getir

### İlçeler

- `GET /api/v1/districts` - Opsiyonel filtrelerle tüm ilçeleri getir
- `GET /api/v1/districts/{id}` - ID'ye göre belirli ilçeyi getir

### Mahalleler

- `GET /api/v1/neighborhoods` - Opsiyonel filtrelerle tüm mahalleleri getir
- `GET /api/v1/neighborhoods/{id}` - ID'ye göre belirli mahalleyi getir

### Köyler

- `GET /api/v1/villages` - Opsiyonel filtrelerle tüm köyleri getir
- `GET /api/v1/villages/{id}` - ID'ye göre belirli köyü getir

### Beldeler

- `GET /api/v1/towns` - Opsiyonel filtrelerle tüm beldeleri getir
- `GET /api/v1/towns/{id}` - ID'ye göre belirli beldeyi getir

## Query Parametreleri

Tüm liste endpoint'leri şu ortak query parametrelerini destekler:

- `name`: İsme göre filtrele (kısmi eşleşme)
- `minPopulation`: Minimum nüfus filtresi
- `maxPopulation`: Maksimum nüfus filtresi
- `offset`: Sayfalama offset'i
- `limit`: Sayfalama limiti
- `fields`: Döndürülecek alanların virgülle ayrılmış listesi
- `sort`: Alana göre sırala (azalan için `-` öneki kullan)

Ek filtreler endpoint'e göre değişir. Detaylar için interaktif dokümantasyona bakın.

## Örnek İstekler

### Tüm illeri getir

```bash
curl http://localhost:8181/api/v1/provinces
```

### Nüfusu 1 milyonun üzerinde olan illeri getir

```bash
curl http://localhost:8181/api/v1/provinces?minPopulation=1000000
```

### Belirli bir ili getir (İstanbul, id=34)

```bash
curl http://localhost:8181/api/v1/provinces/34
```

### Belirli bir ildeki ilçeleri getir

```bash
curl http://localhost:8181/api/v1/districts?provinceId=34
```

### Sadece belirli alanları getir

```bash
curl http://localhost:8181/api/v1/provinces?fields=id,name,population
```

## Test

Proje tüm katmanlarda kapsamlı test kapsamı içerir (80+ test).

### Testleri Çalıştırma

```bash
# Test bağımlılıklarını yükle
pip install pytest pytest-cov pytest-asyncio httpx

# Tüm testleri çalıştır
pytest tests/ -v

# Coverage raporu ile çalıştır
pytest tests/ -v --cov=app --cov-report=term-missing

# HTML coverage raporu ile çalıştır
pytest tests/ -v --cov=app --cov-report=html
# htmlcov/index.html dosyasını tarayıcıda açın
```

### Test Yapısı

```
tests/
├── test_data_loader.py              # DataLoader testleri (14 test)
├── test_api/
│   └── test_provinces_endpoint.py   # API entegrasyon testleri (19 test)
├── test_services/
│   ├── test_base_service.py         # Base service testleri (18 test)
│   └── test_province_service.py     # Province service testleri (18 test)
└── test_middleware/
    └── test_security.py             # Güvenlik middleware testleri (11 test)
```

**Mevcut Kapsam**: Şunları kapsayan 80+ test:

- ✅ Veri yükleme ve önbellekleme
- ✅ Service katmanı (filtreleme, sıralama, sayfalama)
- ✅ API endpoint'leri (tüm HTTP metodları ve hata durumları)
- ✅ Güvenlik middleware (tüm OWASP başlıkları)

Detaylı test rehberi için [TESTING.md](docs/TESTING.md) dosyasına bakın.

## Proje Yapısı

```
turkiye-api-py/
├── app/
│   ├── data/                 # JSON veri dosyaları
│   ├── i18n/                 # Uluslararasılaştırma
│   ├── middleware/           # İstek/yanıt middleware
│   │   ├── security.py       # Güvenlik başlıkları (YENİ)
│   │   ├── metrics.py        # Prometheus metrikleri
│   │   └── language.py       # Dil algılama
│   ├── models/               # Pydantic modelleri ve şemaları
│   ├── routers/              # API route handler'ları
│   ├── services/             # İş mantığı katmanı
│   │   ├── cache_service.py  # Redis önbellekleme servisi (YENİ)
│   │   ├── base_service.py   # Base service yardımcıları
│   │   └── *_service.py      # Domain servisleri
│   ├── main.py               # FastAPI uygulaması
│   ├── settings.py           # Yapılandırma yönetimi
│   └── scalar_docs.py        # API dokümantasyon kurulumu
├── tests/                    # Test suite (80+ test) (YENİ)
│   ├── test_api/             # API entegrasyon testleri
│   ├── test_services/        # Service birim testleri
│   ├── test_middleware/      # Middleware testleri
│   └── conftest.py           # Test fixture'ları
├── docs/                     # Dokümantasyon (YENİ)
│   ├── DEPLOYMENT_EN.md      # Deployment rehberi (İngilizce)
│   ├── DEPLOYMENT_TR.md      # Deployment rehberi (Türkçe)
│   ├── DATA_SYNC.md          # Veri senkronizasyon rehberi
│   ├── GUIDES_SYNC.md        # Dokümantasyon senkronizasyon rehberi
│   └── PRODUCTION_READINESS.md  # Production kontrol listesi
├── scripts/                  # Yardımcı scriptler (YENİ)
│   ├── sync-data.sh          # Veri senkronizasyon scripti (Linux/Mac)
│   ├── sync-data.bat         # Veri senkronizasyon scripti (Windows)
│   ├── sync-guides.sh        # Rehber senkronizasyon scripti (Linux/Mac)
│   └── sync-guides.bat       # Rehber senkronizasyon scripti (Windows)
├── .github/
│   └── workflows/
│       ├── sync-data.yml     # Veri senkronizasyon workflow (YENİ)
│       └── sync-guides.yml   # Rehber senkronizasyon workflow (YENİ)
├── requirements.txt          # Python bağımlılıkları
├── run.py                    # Development server runner
├── gunicorn.conf.py          # Production Gunicorn konfigürasyonu
├── Dockerfile                # Docker image tanımı
├── docker-compose.yml        # Docker Compose konfigürasyonu
├── .env.example              # Development environment şablonu
├── .env.production.recommended  # Production config şablonu (YENİ)
├── .pre-commit-config.yaml   # Pre-commit hooks (YENİ)
├── CHANGELOG.md              # Versiyon geçmişi (YENİ)
├── TESTING.md                # Test rehberi (YENİ)
├── IMPLEMENTATION_SUMMARY.md # Uygulama detayları (YENİ)
├── README.md                 # İngilizce README
└── README_TR.md              # Bu dosya (Türkçe)
```

## Teknoloji Yığını

### Ana Framework

- **FastAPI**: Modern Python web framework
- **Pydantic**: Python type annotations kullanarak veri validasyonu
- **Uvicorn**: ASGI server implementasyonu
- **Gunicorn**: Production WSGI/ASGI server

### Performans & Önbellekleme

- **Redis**: Dağıtık önbellekleme ve rate limiting
- **In-Memory Cache**: O(1) aramalar için önceden indexlenmiş veri yapıları

### Güvenlik

- **OWASP Başlıkları**: Kapsamlı güvenlik başlığı middleware
- **CORS Middleware**: Yapılandırılabilir cross-origin resource sharing
- **Rate Limiting**: Redis backend ile istek kısıtlama

### Dokümantasyon & API

- **Scalar**: Güzel, interaktif API dokümantasyon UI
- **OpenAPI 3.0**: Çoklu dil desteği ile tam spesifikasyon

### Test & Kalite

- **pytest**: 80+ test ile test framework
- **pytest-cov**: Kod coverage raporlama
- **pytest-asyncio**: Async test desteği
- **Black**: Kod formatlama
- **isort**: Import sıralama
- **flake8**: Linting
- **Bandit**: Güvenlik açığı tarama
- **mypy**: Statik tip kontrolü

### DevOps & İzleme

- **Docker**: Containerization
- **GitHub Actions**: Otomatik veri ve dokümantasyon senkronizasyonu
- **Prometheus**: Metrik toplama
- **Pre-commit**: Kod kalitesi için git hooks

## Kaynaklar

- [İlçe nüfusları](https://biruni.tuik.gov.tr/medas)
- [İlçe alanları](https://web.archive.org/web/20190416051733/https://www.harita.gov.tr/images/urun/il_ilce_alanlari.pdf)

## Katkıda Bulunma

Katkılar memnuniyetle karşılanır! Bu proje kapsamlı test ve otomatik kalite kontrolleri ile yüksek kalite standartlarını korur.

### Geliştirme İş Akışı

1. **Fork ve Clone**

   ```bash
   git clone https://github.com/KULLANICI_ADINIZ/turkiye-api-py.git
   cd turkiye-api-py
   ```

2. **Geliştirme Ortamını Kurun**

   ```bash
   python -m venv venv
   source venv/bin/activate  # veya Windows'ta venv\Scripts\activate
   pip install -r requirements.txt
   pip install pre-commit pytest pytest-cov
   pre-commit install
   ```

3. **Feature Branch Oluşturun**

   ```bash
   git checkout -b feature/yeni-ozellik-adi
   ```

4. **Kod ve Test Yazın**
   - Mevcut kod stilini takip edin (Black, isort, flake8 tarafından zorlanır)
   - Yeni özellikler için testler ekleyin (80%+ coverage koruyun)
   - Gerektiğinde dokümantasyonu güncelleyin

5. **Kalite Kontrollerini Çalıştırın**

   ```bash
   # Testleri çalıştır
   pytest tests/ -v --cov=app

   # Pre-commit hooks'u çalıştır
   pre-commit run --all-files
   ```

6. **Commit ve Push**

   ```bash
   git add .
   git commit -m "feat: özellik açıklaması"
   git push origin feature/yeni-ozellik-adi
   ```

7. **Pull Request Oluşturun**
   - Değişikliklerin net açıklamasını sağlayın
   - İlgili issue'lara referans verin
   - Tüm testlerin ve kalite kontrollerinin yerel olarak geçtiğinden emin olun

### Kodlama Standartları

- **Kod Stili**: 120 karakter satır uzunluğu ile Black formatlama
- **Import Sıralama**: Black profili ile isort
- **Type Hints**: Tüm public fonksiyonlar ve metodlar için gerekli
- **Docstrings**: Tüm public sınıflar ve fonksiyonlar için gerekli
- **Test**: Yeni kod için minimum 80% kod coverage
- **Güvenlik**: Tüm kodlar Bandit tarafından taranır

### Pull Request Kuralları

- ✅ Tüm testler geçmeli
- ✅ Kod coverage azalmamalı
- ✅ Pre-commit hooks geçmeli
- ✅ Net commit mesajları (conventional commits tercih edilir)
- ✅ Önemli değişiklikler için CHANGELOG.md güncelleyin
- ✅ Büyük değişiklikler için önce bir issue açın

### Kalite Kontrollerini Yerel Olarak Çalıştırma

Kod kalitesini sağlamak için commit öncesi bu kontrolleri yerel olarak çalıştırın:

```bash
# Test matrisi (Python 3.8-3.11)
pytest tests/ -v --cov=app

# Linting
black --check app/ tests/
isort --check app/ tests/
flake8 app/ tests/
mypy app/

# Güvenlik
bandit -r app/ -ll
```

### Dokümantasyon

Yeni özellikler eklerken:

- README.md'yi güncelleyin (İngilizce ve Türkçe)
- `app/scalar_docs.py` dosyasındaki API dokümantasyonuna örnekler ekleyin
- Yapılandırma değişirse DEPLOYMENT rehberlerini güncelleyin
- CHANGELOG.md'ye giriş ekleyin

Turkiye API'ye katkıda bulunduğunuz için teşekkürler! 🎉

## Teşekkürler

Bu proje, [Adem Kurtipek](https://github.com/ubeydeozdmr) tarafından geliştirilen orijinal [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) projesine dayanmaktadır.

**Python İmplementasyonu**: Adem Kurtipek

- E-posta: [gncharitaci@gmail.com](mailto:gncharitaci@gmail.com)
- GitHub: [@gencharitaci](https://github.com/gencharitaci)
- Repository: [turkiye-api-py](https://github.com/gencharitaci/turkiye-api-py)

**Orijinal Geliştirici**: Adem Kurtipek

- E-posta: [ubeydeozdmr@gmail.com](mailto:ubeydeozdmr@gmail.com)
- Telegram: [@ubeydeozdmr](https://t.me/ubeydeozdmr)
- GitHub: [@ubeydeozdmr](https://github.com/ubeydeozdmr)

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

Orijinal [turkiye-api](https://github.com/ubeydeozdmr/turkiye-api) projesine dayanır, o da MIT lisanslıdır.
