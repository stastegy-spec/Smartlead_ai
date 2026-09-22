# SmartLead AI - Yapay Zekâ Destekli Müşteri Asistanı ve Yönetim Paneli

Bu proje, ziyaretçilerle yapay zekâ üzerinden etkileşim kuran ve onların iletişim bilgilerini (lead) güvenli bir şekilde toplayarak veritabanına kaydeden ölçeklenebilir bir **SmartLead AI** iskeletidir.

## Projenin Amacı ve Özellikleri
* **Yapay Zekâ Sohbet Botu:** Ziyaretçilerin sorularını Groq API (Llama modeli) kullanarak anında ve akıllıca yanıtlar.
* **Lead Toplama:** Müşteri adaylarının ad, telefon, e-posta ve mesaj bilgilerini toplar.
* **Güvenli Veritabanı:** SQLite altyapısı ve SQL Injection koruması ile verileri güvenle saklar.
* **Modüler Mimari:** Sorumlulukların ayrılığı ilkesine (`database.py`, `ai_service.py`, `routes.py`) tam uyumlu olarak tasarlanmıştır.
* **Wix Velo Entegrasyonu:** Ön yüzde Wix arayüzü ile RESTful API üzerinden haberleşir.

---

## Hedef Mimari (Dosya Düzeni)


Smartlead_ai/
├── run.py                  # Sunucuyu başlatan giriş noktası
├── config.py               # Ortam ve uygulama ayarları
├── requirements.txt        # Proje bağımlılıkları
├── .env                    # Gizli anahtarlar (Git'e eklenmez)
├── .gitignore
│
└── app/
    ├── __init__.py         # Uygulama fabrikası (create_app)
    ├── database.py         # Veritabanı işlemleri (SQLite)
    ├── routes.py           # HTTP rotaları ve API uç noktaları
    ├── templates/          # HTML şablonları
    └── services/
        └── ai_service.py   # Groq Yapay Zekâ servis entegrasyonu

        

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Groq API Anahtarı Nasıl Alınır?

Yapay zekâ modelini çalıştırmak için Groq üzerinden ücretsiz bir API anahtarına ihtiyacın var:

    console.groq.com adresine git ve ücretsiz bir hesap oluştur.

    Giriş yaptıktan sonra sol menüden veya profil alanından "API Keys" sekmesini seç.

    "Create API Key" butonuna tıklayarak kendine bir isim ver ve anahtarını oluştur.

    gsk_ ile başlayan bu anahtarı güvenli bir yere kopyala (bu anahtarı bir daha tam olarak göremezsin, kaybedersen yeniden oluşturman gerekir).

    
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Kurulum ve Çalıştırma

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

1. Depoyu Klonlayın: 

git clone [https://github.com/stastegy-spec/Smartlead_ai.git](https://github.com/stastegy-spec/Smartlead_ai.git)
cd Smartlead_ai

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

2. Sanal Ortam (Venv) Oluşturun ve Aktif Edin:

python -m venv venv

# Windows için:
venv\Scripts\activate

# Mac/Linux için:
source venv/bin/activate

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

3. Bağımlılıkları Yükleyin:

pip install -r requirements.txt


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

4. .env Dosyası Oluşturun:
Proje kök dizinine bir .env dosyası ekleyin ve şu bilgileri tanımlayın:

SECRET_KEY=gizli-anahtariniz
GROQ_API_KEY=gsk_sizin_groq_api_anahtarini

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

5. Sunucuyu Başlatın:

python run.py

Sunucu varsayılan olarak http://localhost:5000 adresinde çalışacaktır.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

6. Render.com Üzerinden Canlıya Alma (Yayınlama)

Projeyi internet üzerinden erişilebilir hale getirmek ve Wix sitene bağlamak için Render kullanıyoruz:

    render.com adresine git ve GitHub hesabınla giriş yap.

    Panelde üst kısımdaki "New +" butonuna tıkla ve "Web Service" seçeneğini seç.

    GitHub depolarından Smartlead_ai projesini seç ve "Connect" de.
    
-
    Açılan ayar sayfasında şu bilgileri doldur:
    

        Name: Projine bir isim ver (örn. smartlead-ai)

        Environment: Python 3

        Build Command: pip install -r requirements.txt

        Start Command: gunicorn run:app
        
-
    Sayfanın alt kısmındaki "Advanced" veya "Environment Variables" bölümüne gelerek şu gizli değişkenleri ekle:

        Key: GROQ_API_KEY -> Value: gsk_... (Groq'tan aldığın anahtar)

        Key: SECRET_KEY -> Value: rastgele-gizli-bir-kelime
        

    En alttaki "Create Web Service" butonuna basarak dağıtımı (deploy) başlat.

    Birkaç dakika içinde kurulum tamamlanacak ve sana https://siten-adi.onrender.com şeklinde bir canlı URL verilecektir. Wix kodundaki fetch adresini bu URL ile güncellemeyi unutma!


