"""
config.py — Merkezi Yapılandırma Yönetimi
==========================================
Tüm ortam değişkenleri ve sabit ayarlar BURADAN okunur.
Hiçbir kod dosyası doğrudan os.environ okumaz; hepsi bu sınıfı kullanır.
"""

import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


class Config:
    """Temel yapılandırma sınıfı — tüm ortamlar bu sınıftan türer."""

    # ── Güvenlik ────────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # ── Veritabanı ──────────────────────────────────────────────────────────
    SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH", "smartlead.db")

    # ── Yapay Zekâ API ──────────────────────────────────────────────────────
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

    # Hangi AI sağlayıcı kullanılacak
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

    # ── İşletme Kimliği (System Prompt'un temeli) ───────────────────────────
    BUSINESS_NAME = os.environ.get("BUSINESS_NAME", "ENDORAY")
    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        (
            "Sen ENDORAY markasının yapay zekâ asistanısın. "
            "Endoray; KOBİ'ler, girişimciler ve dijitalde varlığını güçlendirmek isteyen markalar için "
            "yapay zekâ destekli sosyal medya yönetimi, viral video kurguları ve dijital içerik danışmanlığı "
            "sunan yeni nesil bir dijital ajanstır. Geleneksel ajans süreçlerini yapay zekâ teknolojileriyle "
            "entegre ederek markaların içerik üretim ve pazarlama süreçlerini hızlandırır, maliyetleri düşürür "
            "ve yüksek etkileşimli çözümler sağlar. "
            "Yanıtların kısa, profesyonel, çözüm odaklı ve Türkçe olmalıdır. "
            "Kullanıcı hizmetlerle ilgilendiğinde adını ve telefon numarasını almaya yönlendir."
        ),
    )

    # ── CORS İzin Verilen Kaynaklar ──────────────────────────────────────────
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    """Geliştirme ortamı — debug açık, verbose loglar."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production ortamı — debug kapalı, güvenlik maksimum."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Test ortamı — in-memory veritabanı kullanılır."""
    DEBUG = True
    TESTING = True
    SQLITE_DB_PATH = ":memory:"


# Ortam adına göre yapılandırma seçici
config_selector = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}