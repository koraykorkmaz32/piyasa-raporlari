import os
from datetime import datetime
from google import genai

# ---------------------------------------------------------
# BURASI YAPAY ZEKA (GEMINI) KISMI
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

bugun = datetime.now().strftime("%Y-%m-%d")
tarih_formatli = datetime.now().strftime("%d %B %Y")

komut = f"""
Sen Wall Street kalitesinde rapor yazan uzman bir baş ekonomistsin. Bana bugünkü ({tarih_formatli}) Türkiye piyasalarıyla ilgili çok prestijli ve derinlikli bir günlük piyasa analiz raporu yaz. 
İçeriğinde şunlar olsun:
1. Piyasaların Genel Görünümü (BIST 100, Döviz, Altın)
2. Makroekonomik Gelişmeler
3. Şirket Gelişmeleri ve Mikro Veriler
4. Stratejik Kısa Vadeli Beklentiler
Yazı dilin çok profesyonel, elit ve akademik bir finans bülteni tarzında olsun. Hiçbir HTML veya Markdown işareti kullanma, sadece düz metin olarak yaz.
"""

print("Gemini'dan elit rapor isteniyor...")
yanit = client.models.generate_content(
    model='gemini-3.6-flash',
    contents=komut
)
spark_rapor_metni = yanit.text
print("Rapor başarıyla üretildi!")
# ---------------------------------------------------------

# ---------------------------------------------------------
# AKILLI METİN DİZGİSİ (Düz metni profesyonel bir tasarıma çevirir)
satirlar = spark_rapor_metni.split('\n')
islenmis_satirlar = []

for satir in satirlar:
    satir = satir.strip()
    if not satir:
        continue
    
    # Madde işaretlerini (1., 2. vb.) şık bir başlığa dönüştürür
    if satir[0].isdigit() and (satir[1] == '.' or (len(satir) > 2 and satir[2] == '.')):
        islenmis_satirlar.append(f"<h3 class='section-title'>{satir}</h3>")
    # İçinde ":" geçen yerleri (Örn: Borsa İstanbul:) kalın vurgu yapar
    elif ":" in satir and len(satir.split(":")[0]) < 40:
        parcalar = satir.split(":", 1)
        islenmis_satirlar.append(f"<p><strong class='highlight'>{parcalar[0]}:</strong>{parcalar[1]}</p>")
    else:
        islenmis_satirlar.append(f"<p>{satir}</p>")

html_rapor_icerigi = "\n".join(islenmis_satirlar)
# ---------------------------------------------------------

rapor_klasoru = "raporlar"
os.makedirs(rapor_klasoru, exist_ok=True)

# ---------------------------------------------------------
# 1. ELİT RAPOR SAYFASI TASARIMI
rapor_sayfasi = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tarih_formatli} | Kurumsal Piyasa Analizi</title>
    <!-- Google Fonts: Inter ve Playfair Display -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #0b1c31;    /* Koyu Kurumsal Lacivert */
            --accent: #c5a059;     /* Şık Altın/Bronz */
            --bg: #f7f9fc;         /* Yumuşak Arka Plan */
            --text-main: #2d3748;  /* Okunabilir Koyu Gri */
            --text-light: #718096; /* İkincil Metinler */
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.8;
        }}
        .navbar {{
            background-color: var(--primary);
            padding: 25px 0;
            text-align: center;
            border-bottom: 4px solid var(--accent);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .navbar h1 {{
            font-family: 'Playfair Display', serif;
            color: #ffffff;
            margin: 0;
            font-size: 26px;
            letter-spacing: 3px;
            text-transform: uppercase;
        }}
        .container {{
            max-width: 850px;
            margin: 40px auto;
            background: #ffffff;
            padding: 60px 70px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
        }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            color: var(--text-light);
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 40px;
            transition: color 0.3s;
        }}
        .back-link:hover {{ color: var(--accent); }}
        .back-link::before {{
            content: '←';
            margin-right: 8px;
            font-size: 18px;
        }}
        .report-header {{
            text-align: center;
            margin-bottom: 50px;
        }}
        .report-date {{
            color: var(--accent);
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 2px;
            text-transform: uppercase;
            display: block;
            margin-bottom: 15px;
        }}
        .report-title {{
            font-family: 'Playfair Display', serif;
            font-size: 38px;
            color: var(--primary);
            margin: 0;
            line-height: 1.3;
        }}
        .divider {{
            width: 70px;
            height: 3px;
            background-color: var(--accent);
            margin: 30px auto 0;
        }}
        .report-content p {{
            margin-bottom: 20px;
            font-size: 16px;
            color: #4a5568;
            text-align: justify;
        }}
        .section-title {{
            font-family: 'Playfair Display', serif;
            color: var(--primary);
            font-size: 22px;
            margin-top: 40px;
            margin-bottom: 15px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 10px;
        }}
        .highlight {{
            color: var(--primary);
            font-weight: 600;
        }}
        .disclaimer {{
            margin-top: 60px;
            padding: 25px 30px;
            background-color: #f8fafc;
            border-left: 4px solid var(--accent);
            font-size: 13px;
            color: var(--text-light);
            border-radius: 0 8px 8px 0;
        }}
        .disclaimer strong {{
            color: var(--primary);
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        @media (max-width: 768px) {{
            .container {{ padding: 30px 25px; margin: 20px; }}
            .report-title {{ font-size: 28px; }}
        }}
    </style>
</head>
<body>
    <div class="navbar">
        <h1>GLOBAL MARKETS & STRATEGY</h1>
    </div>
    <div class="container">
        <a href="../index.html" class="back-link">Arşive Dön</a>
        
        <div class="report-header">
            <span class="report-date">{tarih_formatli}</span>
            <h2 class="report-title">Günlük Piyasa Analizi ve Makro Strateji Raporu</h2>
            <div class="divider"></div>
        </div>
        
        <div class="report-content">
            {html_rapor_icerigi}
        </div>
        
        <div class="disclaimer">
            <strong>Yasal Uyarı ve Sorumluluk Reddi Beyanı</strong>
            Bu raporda yer alan her türlü bilgi, veri, analiz, yorum ve öngörüler genel bilgilendirme amacıyla yapay zeka sistemleri tarafından derlenmiş olup analistin kişisel piyasa değerlendirmelerini yansıtmaktadır. Kesin yatırım tavsiyesi niteliği taşımamaktadır. Finansal piyasalar doğası gereği volatilite barındırır, nihai kararlar kullanıcıya aittir.
        </div>
    </div>
</body>
</html>"""

with open(f"{rapor_klasoru}/{bugun}.html", "w", encoding="utf-8") as f:
    f.write(rapor_sayfasi)


# ---------------------------------------------------------
# 2. ELİT ANA SAYFA (ARŞİV) TASARIMI
rapor_listesi = sorted(os.listdir(rapor_klasoru), reverse=True)

index_icerik = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Piyasa Bülteni | Arşiv</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0b1c31;
            --accent: #c5a059;
            --bg: #f7f9fc;
            --card-bg: #ffffff;
            --text-main: #2d3748;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 0;
        }
        .header {
            background: var(--primary);
            padding: 70px 20px;
            text-align: center;
            color: white;
            border-bottom: 5px solid var(--accent);
        }
        .header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 42px;
            margin: 0 0 15px 0;
            letter-spacing: 1px;
        }
        .header p {
            font-size: 18px;
            color: #cbd5e0;
            font-weight: 300;
            max-width: 600px;
            margin: 0 auto;
        }
        .container {
            max-width: 800px;
            margin: -40px auto 60px auto;
            padding: 0 20px;
            position: relative;
            z-index: 10;
        }
        .report-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .report-card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 25px 35px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
            text-decoration: none;
            color: var(--text-main);
            border-left: 4px solid transparent;
            transition: all 0.3s ease;
        }
        .report-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.08);
            border-left-color: var(--accent);
        }
        .card-left {
            display: flex;
            align-items: center;
            gap: 25px;
        }
        .date-badge {
            background: #edf2f7;
            color: var(--primary);
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.5px;
        }
        .card-title {
            font-weight: 500;
            font-size: 17px;
        }
        .card-arrow {
            color: var(--accent);
            font-weight: bold;
            font-size: 22px;
            transition: transform 0.3s ease;
        }
        .report-card:hover .card-arrow {
            transform: translateX(6px);
        }
        @media (max-width: 600px) {
            .card-left { flex-direction: column; align-items: flex-start; gap: 10px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Global Markets</h1>
        <p>Kurumsal kalitede, günlük finansal analiz ve makro strateji raporları arşivi.</p>
    </div>
    
    <div class="container">
        <div class="report-list">
"""

for rapor in rapor_listesi:
    dosya_adi = rapor.replace('.html', '')
    index_icerik += f"""
            <a href='{rapor_klasoru}/{rapor}' class="report-card">
                <div class="card-left">
                    <span class="date-badge">{dosya_adi}</span>
                    <span class="card-title">Günlük Piyasa Analizi</span>
                </div>
                <span class="card-arrow">→</span>
            </a>
"""

index_icerik += """
        </div>
    </div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_icerik)
