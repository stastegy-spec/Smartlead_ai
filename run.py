"""
run.py — Uygulamanın Giriş Noktası (Entry Point)
=================================================
Bu dosyanın tek sorumluluğu: Flask uygulamasını başlatmak.
İş mantığı burada YOK. Sadece "anahtar çevirme" işlemi.

Mimari Not:
    Bu ayrım sayesinde ileride Gunicorn, uWSGI gibi
    production WSGI sunucularına geçiş tek satır değişiklikle
    yapılabilir.
"""

from app import create_app

# Uygulama fabrikasından (factory) örneği al
app = create_app()

if __name__ == "__main__":
    # Sadece doğrudan çalıştırıldığında (python run.py) devreye girer
    # Production'da Gunicorn bu bloğu ATLAR
    app.run(
        host="0.0.0.0",   # Tüm ağ arayüzlerinden erişime izin ver
        port=5000,
        debug=True         # Production'da mutlaka False yapın!
    )