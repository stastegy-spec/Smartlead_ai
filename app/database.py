"""
app/database.py — Veri Erişim Katmanı (Data Access Layer)
==========================================================
Veritabanı ile ilgili HER ŞEY bu dosyadadır:
    ✓ Tablo oluşturma (schema)
    ✓ Veri kaydetme (INSERT)
    ✓ Veri okuma (SELECT)
    ✗ İş mantığı YOK — bu routes.py veya services'te
    ✗ HTTP kavramları YOK — bu routes.py'de

Mimari Not (Repository Pattern):
    Bu dosya bir "Repository" görevi görür. Gelecekte SQLite'ı
    PostgreSQL veya MongoDB ile değiştirseniz bile, sadece bu
    dosyayı değiştirmeniz yeterli olacak. routes.py dokunulmaz kalır.
"""

import sqlite3
import logging
from datetime import datetime
from flask import Flask, g

# Modül düzeyinde logger — her modülün kendi logger'ı olmalı
logger = logging.getLogger(__name__)


def get_db_path(app: Flask) -> str:
    """Uygulama yapılandırmasından veritabanı yolunu döndürür."""
    return app.config["SQLITE_DB_PATH"]


def get_db(app: Flask) -> sqlite3.Connection:
    """
    İstek başına tek bir veritabanı bağlantısı sağlar.

    Flask'ın 'g' nesnesi: Her HTTP isteğine özel geçici depo.
    Bağlantıyı istek boyunca yeniden kullanmak performans açısından kritik.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            get_db_path(app),
            detect_types=sqlite3.PARSE_DECLTYPES,  # Python tiplerine otomatik dönüştür
        )
        # Sonuçları sözlük (dict) olarak döndür — index yerine sütun adı ile eriş
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    """
    İstek tamamlandığında veritabanı bağlantısını kapat.
    Flask'ın teardown_appcontext hook'u bu fonksiyonu otomatik çağırır.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app: Flask) -> None:
    """
    Veritabanı tablolarını oluşturur (yoksa).

    CREATE TABLE IF NOT EXISTS: Güvenli idempotent operasyon —
    her uygulama başlatımında çağrılabilir, var olan tabloyu silmez.
    """
    db_path = get_db_path(app)
    logger.info(f"Veritabanı başlatılıyor: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ── leads tablosu: Potansiyel müşteri kayıtları ─────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT    NOT NULL,              -- Müşteri adı soyadı
            phone     TEXT    NOT NULL,              -- Telefon numarası
            message   TEXT,                          -- İletmek istediği mesaj
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- Kayıt zamanı
        )
    """)

    # ── chat_history tablosu: AI konuşma geçmişi (opsiyonel) ────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT    NOT NULL,             -- Ziyaretçi oturumu
            role       TEXT    NOT NULL,             -- 'user' veya 'assistant'
            content    TEXT    NOT NULL,             -- Mesaj içeriği
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

    # Flask teardown hook'u: her istek sonunda bağlantıyı otomatik kapat
    app.teardown_appcontext(close_db)
    logger.info("Veritabanı tabloları hazır.")


# ─────────────────────────────────────────────────────────────────────────────
# CRUD Fonksiyonları (Create, Read, Update, Delete)
# ─────────────────────────────────────────────────────────────────────────────

def save_lead(app: Flask, name: str, phone: str, message: str = "") -> dict:
    """
    Yeni bir lead (müşteri adayı) veritabanına kaydeder.

    Args:
        app:     Flask uygulama örneği (bağlantı için gerekli)
        name:    Müşteri adı soyadı
        phone:   Telefon numarası
        message: Müşterinin bıraktığı ek mesaj

    Returns:
        Kaydedilen lead'in tüm bilgilerini içeren dict

    Raises:
        sqlite3.Error: Veritabanı yazma hatası durumunda
    """
    db = get_db(app)

    cursor = db.execute(
        "INSERT INTO leads (name, phone, message) VALUES (?, ?, ?)",
        (name, phone, message)
        # NOT: Parametreleri direkt string ile birleştirmeyin!
        # SQL Injection saldırısına kapı açar. Her zaman ? placeholder kullanın.
    )
    db.commit()

    # Yeni kaydedilen satırın ID'sini al ve tam kaydı döndür
    new_id = cursor.lastrowid
    lead = db.execute(
        "SELECT * FROM leads WHERE id = ?", (new_id,)
    ).fetchone()

    logger.info(f"Yeni lead kaydedildi: ID={new_id}, İsim={name}")
    return dict(lead)


def get_all_leads(app: Flask) -> list[dict]:
    """
    Tüm lead kayıtlarını en yeniden eskiye sıralar.

    Returns:
        Lead sözlüklerinden oluşan liste
    """
    db = get_db(app)
    leads = db.execute(
        "SELECT * FROM leads ORDER BY created_at DESC"
    ).fetchall()

    # sqlite3.Row nesnelerini JSON-serileştirilebilir dict'e dönüştür
    return [dict(lead) for lead in leads]


def get_lead_by_id(app: Flask, lead_id: int) -> dict | None:
    """
    ID'ye göre tek bir lead kaydını getirir.

    Returns:
        Lead dict'i veya None (bulunamazsa)
    """
    db = get_db(app)
    lead = db.execute(
        "SELECT * FROM leads WHERE id = ?", (lead_id,)
    ).fetchone()

    return dict(lead) if lead else None