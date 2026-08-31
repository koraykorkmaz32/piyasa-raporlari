import os
from datetime import datetime
from google import genai # YENİ NESİL: Kütüphane değiştirildi

# ---------------------------------------------------------
# BURASI YAPAY ZEKA (GEMINI) KISMI
# GitHub'a kaydettiğimiz şifreyi (API Key) kullanarak istemciyi başlatıyoruz
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

bugun = datetime.now().strftime("%Y-%m-%d")
tarih_formatli = datetime.now().strftime("%d %B %Y")

# Gemini'a Rapor Yazdırma Komutu
komut = f"""
Sen uzman bir finansal analistsin. Bana bugünkü ({tarih_formatli}) Türkiye piyasalarıyla ilgili profesyonel bir günlük piyasa analiz raporu yaz. 
İçeriğinde şunlar olsun:
1. Piyasaların Genel Görünümü (BIST 100, Döviz, Altın)
2. Makroekonomik Gelişmeler
3. Şirket Gelişmeleri
4. Kısa Vadeli Beklentiler
Yazı dilin çok profesyonel, bülten tarzında ve ciddi olsun. Hiçbir HTML veya Markdown işareti kullanma, sadece düz metin olarak yaz. Sonuna yasal uyarı ekleme.
"""

print("Gemini'dan rapor isteniyor...")
# Yeni kütüphane ile içerik üretme komutu
yanit = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=komut,
)

# Yapay zekanın cevabını alıyoruz
spark_rapor_metni = yanit.text
print("Rapor başarıyla üretildi!")
# ---------------------------------------------------------

# Metni HTML'de düzgün göstermek için basit bir temizlik yapıyoruz:
html_rapor_icerigi = spark_rapor_metni.replace('\n', '<br><br>\n')

rapor_klasoru = "raporlar"
os.makedirs(rapor_klasoru, exist_ok=True)

# Şık Bülten / Makale Tasarımı
rapor_sayfasi = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <title>{bugun} Piyasa Raporu</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            background-color: #f0f2f5;
            color: #2c3e50;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 850px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        a.back-link {{
            display: inline-block;
            margin-bottom: 20px;
            color: #1890ff;
            text-decoration: none;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
        }}
        a.back-link:hover {{ text-decoration: underline; }}
        .rapor-metni {{
            font-size: 16px;
            text-align: justify;
        }}
        .yasal-uyari {{
            margin-top: 40px;
            padding: 15px;
            background-color: #fff3cd;
            color: #856404;
            border-left: 5px solid #ffeeba;
            font-size: 13px;
            font-family: 'Arial', sans-serif;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← Arşive Dön</a>
        
        <div class="rapor-metni">
            <!-- YAPAY ZEKADAN GELEN METİN BURAYA YAZDIRILIYOR -->
            <h2>Günlük Piyasa Analizi ve Detay Raporu ({tarih_formatli})</h2>
            {html_rapor_icerigi}
        </div>
        
        <!-- Sizin CSS'inizdeki Yasal Uyarı Kutusu -->
        <div class="yasal-uyari">
            <strong>Yasal Uyarı ve Sorumluluk Reddi Beyanı:</strong><br>
            Bu raporda yer alan her türlü bilgi, veri, analiz, yorum ve öngörüler genel bilgilendirme amacıyla yapay zeka tarafından hazırlanmış olup analistin kişisel piyasa değerlendirmelerini yansıtmaktadır. Kesin yatırım tavsiyesi niteliği taşımamaktadır.
        </div>
        
    </div>
</body>
</html>"""

# Raporu kaydet
rapor_dosyasi = f"{rapor_klasoru}/{bugun}.html"
with open(rapor_dosyasi, "w", encoding="utf-8") as f:
    f.write(rapor_sayfasi)

# Ana sayfa (Arşiv) tasarımı
rapor_listesi = sorted(os.listdir(rapor_klasoru), reverse=True)
index_icerik = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Piyasa Raporları Arşivi</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #eceff1; padding: 40px; }}
        .card {{ background: white; padding: 30px; max-width: 600px; margin: auto; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #1890ff; padding-bottom: 10px; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 15px 0; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        li:last-child {{ border-bottom: none; }}
        a {{ text-decoration: none; color: #1890ff; font-weight: bold; font-size: 16px; display: block; }}
        a:hover {{ color: #0056b3; transform: translateX(5px); transition: 0.3s; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>📑 Günlük Piyasa Bülteni Arşivi</h1>
        <p>Yayımlanmış piyasa analiz raporlarına aşağıdan ulaşabilirsiniz:</p>
        <ul>
"""

for rapor in rapor_listesi:
    index_icerik += f"<li>📅 <a href='{rapor_klasoru}/{rapor}'>{rapor.replace('.html', '')} Tarihli Piyasa Raporu</a></li>\n"

index_icerik += """
        </ul>
    </div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_icerik)
