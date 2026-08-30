import os
from datetime import datetime

# Tarih ayarları
bugun = datetime.now().strftime("%Y-%m-%d")
rapor_klasoru = "raporlar"
os.makedirs(rapor_klasoru, exist_ok=True)

# 1. Günlük Raporu HTML Olarak Kaydet
rapor_dosyasi = f"{rapor_klasoru}/{bugun}.html"
rapor_icerik = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>{bugun} Piyasa Raporu</title></head>
<body>
    <a href="../index.html">Ana Sayfaya Dön</a>
    <h1>{bugun} Tarihli Piyasa Raporu</h1>
    <p>Buraya Spark üzerinden gelen günlük piyasa verileriniz eklenecek.</p>
</body>
</html>"""

with open(rapor_dosyasi, "w", encoding="utf-8") as f:
    f.write(rapor_icerik)

# 2. Ana Sayfayı (Arşivi) Güncelle
rapor_listesi = sorted(os.listdir(rapor_klasoru), reverse=True)
index_icerik = "<html><head><meta charset='utf-8'><title>Piyasa Raporları Arşivi</title></head><body>"
index_icerik += "<h1>Günlük Piyasa Raporları</h1><ul>"

for rapor in rapor_listesi:
    index_icerik += f"<li><a href='{rapor_klasoru}/{rapor}'>{rapor} Raporu</a></li>"

index_icerik += "</ul></body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_icerik)
