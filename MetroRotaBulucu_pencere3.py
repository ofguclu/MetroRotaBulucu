import os
from google.colab import files

html_icerik = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>İstanbul Raylı Sistemler & Metrobüs Rota Bulucu</title>
<style>
  :root {
    --bg: #f1f5f9;
    --card: #ffffff;
    --text: #0f172a;
    --muted: #64748b;
    --border: #e2e8f0;
    --primary: #1d4ed8;
    --primary-hover: #1e40af;
    --accent-bg: #eff6ff;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: var(--bg); color: var(--text); line-height: 1.5; padding-bottom: 48px; }

  /* Header */
  header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    color: white;
    padding: 20px 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  }
  .header-inner {
    max-width: 1020px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }
  .header-title h1 { font-size: 1.35rem; font-weight: 700; display: flex; align-items: center; gap: 10px; }
  .header-title p { font-size: 0.85rem; color: #cbd5e1; margin-top: 2px; }
  .btn-guide {
    background: rgba(255,255,255,0.14);
    color: white;
    border: 1px solid rgba(255,255,255,0.28);
    padding: 8px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.88rem;
    font-weight: 600;
    transition: 0.2s;
  }
  .btn-guide:hover { background: rgba(255,255,255,0.24); }

  /* Main Container */
  .container { max-width: 1020px; margin: 24px auto; padding: 0 16px; }

  /* Search Panel */
  .search-card {
    background: var(--card);
    border-radius: 14px;
    padding: 22px;
    box-shadow: 0 2px 10px rgba(15,23,42,0.06);
    border: 1px solid var(--border);
  }
  .inputs-grid {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 12px;
    align-items: end;
  }
  @media (max-width: 720px) {
    .inputs-grid { grid-template-columns: 1fr; }
    .swap-btn { justify-self: center; transform: rotate(90deg); }
  }
  .field-group { position: relative; }
  .field-group label {
    display: block;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 6px;
  }
  .station-input {
    width: 100%;
    padding: 12px 14px;
    border: 2px solid var(--border);
    border-radius: 10px;
    font-size: 0.98rem;
    font-weight: 500;
    color: var(--text);
    transition: border-color 0.2s;
  }
  .station-input:focus { outline: none; border-color: var(--primary); }

  /* Autocomplete Dropdown */
  .autocomplete-list {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    background: white;
    border: 1px solid var(--border);
    border-radius: 10px;
    max-height: 250px;
    overflow-y: auto;
    box-shadow: 0 10px 25px rgba(0,0,0,0.14);
    z-index: 50;
    display: none;
  }
  .autocomplete-item {
    padding: 10px 14px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f8fafc;
    font-size: 0.92rem;
  }
  .autocomplete-item:hover, .autocomplete-item.active { background: var(--accent-bg); }
  .mini-badges { display: flex; gap: 4px; flex-wrap: wrap; }
  .mini-badge {
    font-size: 0.68rem;
    font-weight: 700;
    color: white;
    padding: 2px 6px;
    border-radius: 4px;
  }

  .swap-btn {
    background: #f8fafc;
    border: 1px solid var(--border);
    width: 44px;
    height: 44px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text);
    transition: 0.2s;
  }
  .swap-btn:hover { background: #e2e8f0; }

  .controls-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid var(--border);
  }
  .filters { display: flex; flex-wrap: wrap; gap: 16px; font-size: 0.88rem; color: #334155; }
  .filters label { display: flex; align-items: center; gap: 6px; cursor: pointer; user-select: none; }
  .btn-search {
    background: var(--primary);
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: 10px;
    font-size: 0.98rem;
    font-weight: 700;
    cursor: pointer;
    transition: 0.2s;
  }
  .btn-search:hover { background: var(--primary-hover); }

  /* Quick Examples */
  .quick-examples {
    margin-top: 12px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    font-size: 0.82rem;
    color: var(--muted);
  }
  .chip-example {
    background: #f8fafc;
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 999px;
    cursor: pointer;
    color: #334155;
    transition: 0.15s;
  }
  .chip-example:hover { background: var(--accent-bg); border-color: #93c5fd; color: var(--primary); }

  /* Results Section */
  .results-header {
    margin: 24px 0 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .results-header h2 { font-size: 1.1rem; color: var(--text); }
  .results-hint { font-size: 0.83rem; color: var(--muted); }

  /* Accordion Route Cards */
  .route-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    margin-bottom: 12px;
    overflow: hidden;
    transition: box-shadow 0.2s, border-color 0.2s;
  }
  .route-card:hover { border-color: #93c5fd; box-shadow: 0 4px 14px rgba(15,23,42,0.06); }
  .route-card.open { border-color: var(--primary); box-shadow: 0 6px 18px rgba(29,78,216,0.1); }

  .route-summary {
    padding: 16px 20px;
    cursor: pointer;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    user-select: none;
  }
  .route-summary-left { flex: 1; min-width: 260px; }
  .route-tag-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
  .alt-number {
    font-weight: 800;
    font-size: 0.85rem;
    color: var(--primary);
    background: var(--accent-bg);
    padding: 3px 9px;
    border-radius: 6px;
  }
  .alt-badge {
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
    background: #f1f5f9;
    color: #334155;
  }
  .alt-badge.best { background: #dcfce7; color: #166534; }

  .line-chain {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
  }
  .line-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 7px;
    color: white;
    font-size: 0.82rem;
    font-weight: 700;
    box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  }
  .chain-arrow { color: #94a3b8; font-weight: 700; font-size: 0.9rem; }

  .route-summary-right {
    display: flex;
    align-items: center;
    gap: 18px;
  }
  .metrics { text-align: right; }
  .metric-time { font-size: 1.12rem; font-weight: 800; color: var(--text); }
  .metric-sub { font-size: 0.8rem; color: var(--muted); }
  .toggle-indicator {
    background: #f8fafc;
    border: 1px solid var(--border);
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--primary);
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .route-card.open .toggle-indicator { background: var(--primary); color: white; border-color: var(--primary); }

  /* Accordion Body (Details) */
  .route-details {
    display: none;
    border-top: 1px solid var(--border);
    background: #fafbfc;
    padding: 20px 22px;
  }
  .route-card.open .route-details { display: block; }

  .timeline { position: relative; padding-left: 24px; }
  .timeline-step {
    position: relative;
    padding-bottom: 20px;
    border-left: 4px solid #cbd5e1;
    padding-left: 18px;
  }
  .timeline-step:last-child { border-left-color: transparent; padding-bottom: 0; }
  .step-dot {
    position: absolute;
    left: -11px;
    top: 2px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: white;
    border: 4px solid var(--primary);
  }
  .step-header {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
  }
  .step-station { font-weight: 700; font-size: 0.98rem; color: var(--text); }
  .step-direction { font-size: 0.86rem; color: #334155; margin-bottom: 6px; }
  .stops-toggle {
    background: white;
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    color: #475569;
    cursor: pointer;
    display: inline-block;
    margin-top: 2px;
  }
  .stops-toggle:hover { background: #f1f5f9; }
  .intermediate-stops {
    display: none;
    margin-top: 8px;
    padding: 10px 12px;
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 0.82rem;
    color: #475569;
  }
  .intermediate-stops.show { display: block; }
  .transfer-note {
    margin-top: 10px;
    padding: 8px 12px;
    background: #fef3c7;
    border-left: 3px solid #f59e0b;
    border-radius: 6px;
    font-size: 0.84rem;
    color: #92400e;
    font-weight: 500;
  }

  /* Modal for Lines Guide */
  .modal-backdrop {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(15,23,42,0.55);
    z-index: 100;
    align-items: center;
    justify-content: center;
    padding: 16px;
  }
  .modal-backdrop.show { display: flex; }
  .modal-box {
    background: white;
    width: 100%;
    max-width: 820px;
    max-height: 85vh;
    border-radius: 14px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .modal-head {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .modal-close {
    background: #f1f5f9;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    font-size: 1.1rem;
    cursor: pointer;
  }
  .modal-body { padding: 18px 20px; overflow-y: auto; }
  .guide-lines-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
  }
  .guide-line-btn {
    border: none;
    color: white;
    padding: 6px 11px;
    border-radius: 7px;
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    opacity: 0.88;
  }
  .guide-line-btn:hover, .guide-line-btn.active { opacity: 1; outline: 2px solid #0f172a; }
  .guide-stops-list {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    padding: 14px;
    background: #f8fafc;
    border-radius: 10px;
    border: 1px solid var(--border);
  }
  .guide-stop-chip {
    background: white;
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.84rem;
  }
  .empty-state {
    text-align: center;
    padding: 42px 20px;
    color: var(--muted);
    background: white;
    border-radius: 12px;
    border: 1px dashed var(--border);
  }
</style>
</head>
<body>

<header>
  <div class="header-inner">
    <div class="header-title">
      <h1>🚇 İstanbul Hızlı Ulaşım Rota Bulucu</h1>
      <p>Metro, Marmaray, Metrobüs, Tramvay ve Füniküler hatları için alternatifli aktarma rehberi</p>
    </div>
    <button class="btn-guide" onclick="openGuide()">📋 Hatlar & Duraklar Rehberi</button>
  </div>
</header>

<div class="container">
  <div class="search-card">
    <div class="inputs-grid">
      <div class="field-group">
        <label for="fromInput">Nereden (Başlangıç İstasyonu)</label>
        <input type="text" id="fromInput" class="station-input" placeholder="Örn: Kadıköy, Kağıthane, Beylikdüzü..." autocomplete="off">
        <div id="fromList" class="autocomplete-list"></div>
      </div>

      <button class="swap-btn" title="Durakları Değiştir" onclick="swapStations()">⇄</button>

      <div class="field-group">
        <label for="toInput">Nereye (Varış İstasyonu)</label>
        <input type="text" id="toInput" class="station-input" placeholder="Örn: Sabiha Gökçen Havalimanı, Taksim..." autocomplete="off">
        <div id="toList" class="autocomplete-list"></div>
      </div>
    </div>

    <div class="controls-row">
      <div class="filters">
        <label><input type="checkbox" id="useMetrobus" checked> Metrobüs (34) dahil</label>
        <label><input type="checkbox" id="includeConstruction"> İnşaat halindeki hatları göster (M12 vb.)</label>
      </div>
      <button class="btn-search" onclick="findRoutes()">Rota Bul</button>
    </div>

    <div class="quick-examples">
      <span>Hızlı Örnekler:</span>
      <span class="chip-example" onclick="setExample('Kağıthane', 'Kadıköy')">Kağıthane → Kadıköy</span>
      <span class="chip-example" onclick="setExample('Beylikdüzü Sondurak', 'Sabiha Gökçen Havalimanı')">Beylikdüzü → Sabiha Gökçen</span>
      <span class="chip-example" onclick="setExample('İstanbul Havalimanı', 'Sultanahmet')">İstanbul Havalimanı → Sultanahmet</span>
      <span class="chip-example" onclick="setExample('Taksim', 'Boğaziçi Üniversitesi / Hisarüstü')">Taksim → Hisarüstü</span>
    </div>
  </div>

  <div id="resultsContainer"></div>
</div>

<!-- Hatlar Rehberi Modal -->
<div id="guideModal" class="modal-backdrop" onclick="if(event.target===this) closeGuide()">
  <div class="modal-box">
    <div class="modal-head">
      <h3 style="font-size:1.05rem;">İstanbul Raylı Sistemler & Metrobüs Hatları</h3>
      <button class="modal-close" onclick="closeGuide()">✕</button>
    </div>
    <div class="modal-body">
      <div id="guideLines" class="guide-lines-grid"></div>
      <h4 id="guideSelectedTitle" style="margin-bottom:10px; font-size:0.95rem;"></h4>
      <div id="guideStops" class="guide-stops-list"></div>
    </div>
  </div>
</div>

<script>
// Sistem Tipleri (Lejant Görseline Göre)
const LINES = {
  "B1": {
    code: "B1",
    type: "TCDD Banliyö Trenleri",
    name: "Halkalı - Gebze Marmaray",
    color: "#4b5563",
    avgMinPerStop: 2.4,
    status: "active",
    stops: [
      "Halkalı", "Mustafa Kemal", "Küçükçekmece", "Florya", "Florya Akvaryum", "Yeşilköy", "Yeşilyurt",
      "Ataköy", "Bakırköy", "Yenimahalle", "Zeytinburnu (Marmaray)", "Kazlıçeşme", "Yenikapı", "Sirkeci",
      "Üsküdar", "Ayrılık Çeşmesi", "Söğütlüçeşme", "Feneryolu", "Göztepe (Marmaray)", "Erenköy",
      "Suadiye", "Bostancı", "Küçükyalı", "İdealtepe", "Süreyya Plajı", "Maltepe", "Cevizli",
      "Atalar", "Başak", "Kartal", "Yunus", "Pendik", "Kaynarca", "Tersane", "Güzelyalı",
      "Aydıntepe", "İçmeler", "Tuzla", "Çayırova", "Fatih", "Osmangazi", "Darıca", "Gebze"
    ]
  },
  "U3": {
    code: "U3",
    type: "TCDD Banliyö Trenleri",
    name: "Sirkeci - Kazlıçeşme Raylı Sistem",
    color: "#be123c",
    avgMinPerStop: 2.5,
    status: "active",
    stops: [
      "Sirkeci", "Cankurtaran", "Kumkapı", "Yenikapı", "Cerrahpaşa", "Kocamustafapaşa", "Yedikule", "Kazlıçeşme"
    ]
  },
  "M1A": {
    code: "M1A",
    type: "Metro",
    name: "Yenikapı - Atatürk Havalimanı",
    color: "#dc2626",
    avgMinPerStop: 2.0,
    status: "active",
    stops: [
      "Yenikapı", "Aksaray", "Emniyet - Fatih", "Topkapı - Ulubatlı", "Bayrampaşa - Maltepe",
      "Sağmalcılar", "Kocatepe", "Otogar", "Terazidere", "Davutpaşa - YTÜ", "Merter",
      "Zeytinburnu", "Bakırköy - İncirli", "Bahçelievler", "Ataköy - Şirinevler", "Yenibosna",
      "DTM - İstanbul Fuar Merkezi", "Atatürk Havalimanı"
    ]
  },
  "M1B": {
    code: "M1B",
    type: "Metro",
    name: "Yenikapı - Kirazlı",
    color: "#e11d48",
    avgMinPerStop: 2.0,
    status: "active",
    stops: [
      "Yenikapı", "Aksaray", "Emniyet - Fatih", "Topkapı - Ulubatlı", "Bayrampaşa - Maltepe",
      "Sağmalcılar", "Kocatepe", "Otogar", "Esenler", "Menderes", "Üçyüzlü", "Bağcılar Meydan", "Kirazlı"
    ]
  },
  "M2": {
    code: "M2",
    type: "Metro",
    name: "Yenikapı - Hacıosman",
    color: "#16a34a",
    avgMinPerStop: 2.1,
    status: "active",
    stops: [
      "Yenikapı", "Vezneciler - İstanbul Ü.", "Haliç", "Şişhane", "Taksim", "Osmanbey",
      "Şişli - Mecidiyeköy", "Gayrettepe", "Levent", "4. Levent", "Sanayi Mahallesi",
      "İTÜ - Ayazağa", "Atatürk Oto Sanayi", "Darüşşafaka", "Hacıosman"
    ]
  },
  "M2_SEY": {
    code: "M2",
    type: "Metro",
    name: "Sanayi Mahallesi - Seyrantepe",
    color: "#15803d",
    avgMinPerStop: 2.0,
    status: "active",
    stops: ["Sanayi Mahallesi", "Seyrantepe"]
  },
  "M3": {
    code: "M3",
    type: "Metro",
    name: "Bakırköy Sahil - Kayaşehir Merkez",
    color: "#0284c7",
    avgMinPerStop: 2.1,
    status: "active",
    stops: [
      "Bakırköy Sahil", "Özgürlük Meydanı", "İncirli", "Haznedar", "İlkyuva", "Yıldıztepe",
      "Molla Gürani", "Kirazlı", "Yenimahalle (M3)", "Mahmutbey", "İSTOÇ", "İkitelli Sanayi",
      "Turgut Özal", "Siteler", "Başak Konutları", "Başakşehir - Metrokent",
      "Onurkent", "Şehir Hastanesi", "Toplu Konutlar", "Kayaşehir Merkez"
    ]
  },
  "M4": {
    code: "M4",
    type: "Metro",
    name: "Kadıköy - Sabiha Gökçen Havalimanı",
    color: "#db2777",
    avgMinPerStop: 2.1,
    status: "active",
    stops: [
      "Kadıköy", "Ayrılık Çeşmesi", "Acıbadem", "Ünalan", "Göztepe", "Yenisahra", "Kozyatağı",
      "Bostancı (M4)", "Küçükyalı (M4)", "Maltepe (M4)", "Huzurevi", "Gülsuyu", "Esenkent",
      "Hastane - Adliye", "Soğanlık", "Kartal (M4)", "Yakacık - Adnan Kahveci", "Pendik (M4)",
      "Tavşantepe", "Fevzi Çakmak - Hastane", "Yayalar - Şeyhli", "Kurtköy", "Sabiha Gökçen Havalimanı"
    ]
  },
  "M5": {
    code: "M5",
    type: "Metro",
    name: "Üsküdar - Samandıra Merkez",
    color: "#6b21a8",
    avgMinPerStop: 2.1,
    status: "active",
    stops: [
      "Üsküdar", "Fıstıkağacı", "Bağlarbaşı", "Altunizade", "Kısıklı", "Bulgurlu", "Ümraniye",
      "Çarşı", "Yamanevler", "Çakmak", "Ihlamurkuyu", "Altınşehir", "İmam Hatip Lisesi",
      "Dudullu", "Necip Fazıl", "Çekmeköy", "Meclis", "Sarıgazi", "Sancaktepe Şehir Hastanesi",
      "Sancaktepe", "Samandıra Merkez"
    ]
  },
  "M6": {
    code: "M6",
    type: "Mini Metro",
    name: "Levent - Boğaziçi Ü. / Hisarüstü",
    color: "#a16207",
    avgMinPerStop: 2.0,
    status: "active",
    stops: ["Levent", "Nispetiye", "Etiler", "Boğaziçi Üniversitesi / Hisarüstü"]
  },
  "M7": {
    code: "M7",
    type: "Metro",
    name: "Yıldız - Mahmutbey",
    color: "#ec4899",
    avgMinPerStop: 2.0,
    status: "active",
    stops: [
      "Yıldız", "Fulya", "Mecidiyeköy", "Çağlayan", "Kağıthane", "Nurtepe", "Alibeyköy",
      "Çırçır", "Veysel Karani - Akşemsettin", "Yeşilpınar", "Kazım Karabekir", "Yenimahalle (M7)",
      "Karadeniz Mahallesi", "Tekstilkent - Giyimkent", "Oruç Reis", "Göztepe Mahallesi", "Mahmutbey"
    ]
  },
  "M8": {
    code: "M8",
    type: "Metro",
    name: "Bostancı - Parseller",
    color: "#2563eb",
    avgMinPerStop: 2.1,
    status: "active",
    stops: [
      "Bostancı", "Emin Ali Paşa", "Ayşekadın", "Kozyatağı", "Küçükbakkalköy", "İçerenköy",
      "Kayışdağı", "Mevlana", "İMES", "MODOKO - KEYAP", "Dudullu", "Huzur", "Parseller"
    ]
  },
  "M9": {
    code: "M9",
    type: "Metro",
    name: "Ataköy - Olimpiyat",
    color: "#eab308",
    avgMinPerStop: 2.1,
    status: "active",
    stops: [
      "Ataköy", "Yenibosna", "Çobançeşme", "29 Ekim Cumhuriyet", "Doğu Sanayi", "Mimar Sinan",
      "15 Temmuz", "Halkalı Caddesi", "Atatürk Mahallesi", "Bahariye", "MASKO",
      "İkitelli Sanayi", "Ziya Gökalp Mahallesi", "Olimpiyat"
    ]
  },
  "M11": {
    code: "M11",
    type: "Metro",
    name: "Gayrettepe - İstanbul Havalimanı - Arnavutköy",
    color: "#9333ea",
    avgMinPerStop: 3.2,
    status: "active",
    stops: [
      "Gayrettepe", "Kağıthane", "Hasdal", "Kemerburgaz", "Göktürk", "İhsaniye",
      "İstanbul Havalimanı", "Kargo Terminali", "Taşoluk", "Arnavutköy Hastane"
    ]
  },
  "M12": {
    code: "M12",
    type: "Metro",
    name: "60. Yıl Parkı - Kazım Karabekir (İnşaat)",
    color: "#84cc16",
    avgMinPerStop: 2.0,
    status: "construction",
    stops: [
      "60. Yıl Parkı", "Tütüncü Mehmet Efendi", "Sahrayıcedit", "Yenisahra", "Ataşehir",
      "Finans Merkezi", "Site", "Atakent", "Çarşı", "SBÜ Hastanesi", "Kazım Karabekir (M12)"
    ]
  },
  "T1": {
    code: "T1",
    type: "Çağdaş Tramvay",
    name: "Kabataş - Bağcılar",
    color: "#1e3a8a",
    avgMinPerStop: 1.9,
    status: "active",
    stops: [
      "Kabataş", "Fındıklı", "Tophane", "Karaköy", "Eminönü", "Sirkeci", "Gülhane",
      "Sultanahmet", "Çemberlitaş", "Beyazıt - Kapalıçarşı", "Laleli - İstanbul Ü.", "Aksaray",
      "Yusufpaşa", "Haseki", "Fındıkzade", "Çapa - Şehremini", "Pazartekke", "Topkapı",
      "Cevizlibağ", "Merkezefendi", "Seyitnizam - Akşemsettin", "Mithatpaşa", "Zeytinburnu",
      "Mehmet Akif", "Merter Tekstil Merkezi", "Güngören", "Akıncılar", "Soğanlı",
      "Yavuz Selim", "Güneştepe", "Bağcılar Merkez"
    ]
  },
  "T2": {
    code: "T2",
    type: "Nostaljik Tramvay",
    name: "Taksim - Tünel",
    color: "#65a30d",
    avgMinPerStop: 2.2,
    status: "active",
    stops: ["Taksim", "Ağa Camii", "Galatasaray", "Odakule", "Tünel"]
  },
  "T3": {
    code: "T3",
    type: "Moda Tramvay",
    name: "Kadıköy - Moda Ring",
    color: "#9a3412",
    avgMinPerStop: 2.0,
    status: "active",
    stops: [
      "Kadıköy", "İskele Camii", "Çarşı (Moda)", "Altıyol", "Bahariye (Moda)", "Kilise",
      "Moda İlkokulu", "Moda Caddesi", "Mühürdar", "Damga Sokak"
    ]
  },
  "T4": {
    code: "T4",
    type: "Çağdaş Tramvay",
    name: "Topkapı - Mescid-i Selam",
    color: "#ea580c",
    avgMinPerStop: 2.0,
    status: "active",
    stops: [
      "Topkapı", "Fetihkapı", "Vatan", "Edirnekapı", "Şehitlik", "Demirkapı", "Topçular",
      "Rami", "Uluyol - Bereç", "Sağmalcılar (T4)", "Bosna - Çukurçeşme", "Ali Fuat Başgil",
      "Taşköprü", "Karadeniz", "KİPTAŞ - Venezia", "Cumhuriyet Mahallesi", "50. Yıl - Baştabya",
      "Hacı Şükrü", "Yeni Mahalle", "Sultançiftliği", "Cebeci", "Mescid-i Selam"
    ]
  },
  "T5": {
    code: "T5",
    type: "Çağdaş Tramvay",
    name: "Eminönü - Alibeyköy Cep Otogarı",
    color: "#7c3aed",
    avgMinPerStop: 2.0,
    status: "active",
    stops: [
      "Eminönü", "Küçükpazar", "Cibali", "Fener", "Balat", "Ayvansaray", "Feshane",
      "Eyüpsultan Teleferik", "Eyüpsultan Devlet Hastanesi", "Silahtarağa Mahallesi",
      "Üniversite", "Alibeyköy Merkez", "Alibeyköy Metro", "Alibeyköy Cep Otogarı"
    ]
  },
  "F1": {
    code: "F1",
    type: "Füniküler / Tünel",
    name: "Taksim - Kabataş",
    color: "#ca8a04",
    avgMinPerStop: 3.0,
    status: "active",
    stops: ["Taksim", "Kabataş"]
  },
  "F2": {
    code: "F2",
    type: "Füniküler / Tünel",
    name: "Karaköy - Beyoğlu (Tünel)",
    color: "#57534e",
    avgMinPerStop: 2.5,
    status: "active",
    stops: ["Karaköy", "Tünel"]
  },
  "F4": {
    code: "F4",
    type: "Füniküler / Tünel",
    name: "Boğaziçi Ü. / Hisarüstü - Aşiyan",
    color: "#78350f",
    avgMinPerStop: 3.0,
    status: "active",
    stops: ["Boğaziçi Üniversitesi / Hisarüstü", "Aşiyan"]
  },
  "TF1": {
    code: "TF1",
    type: "Teleferikler",
    name: "Maçka - Taşkışla",
    color: "#0d9488",
    avgMinPerStop: 3.5,
    status: "active",
    stops: ["Maçka", "Taşkışla"]
  },
  "TF2": {
    code: "TF2",
    type: "Teleferikler",
    name: "Eyüp - Piyer Loti",
    color: "#0f766e",
    avgMinPerStop: 3.0,
    status: "active",
    stops: ["Eyüpsultan Teleferik", "Piyer Loti"]
  },
  "34": {
    code: "34",
    type: "Metrobüs",
    name: "Beylikdüzü - Söğütlüçeşme",
    color: "#b45309",
    avgMinPerStop: 2.0,
    status: "active",
    stops: [
      "Beylikdüzü Sondurak", "Beykent", "Cumhuriyet Mahallesi (Metrobüs)", "Beylikdüzü Belediye",
      "Beylikdüzü", "Güzelyurt", "Haramidere", "Haramidere Sanayi", "Saadetdere Mahallesi",
      "Mustafa Kemal Paşa", "Cihangir - Üniversite Mahallesi", "Avcılar Merkez", "Şükrübey",
      "İBB Sosyal Tesisler", "Küçükçekmece", "Cennet Mahallesi", "Florya (Metrobüs)", "Beşyol",
      "Sefaköy", "Yenibosna", "Şirinevler", "Bahçelievler", "İncirli", "Zeytinburnu",
      "Merter", "Cevizlibağ", "Topkapı", "Bayrampaşa - Maltepe", "Edirnekapı",
      "Ayvansaray - Eyüpsultan", "Halıcıoğlu", "Okmeydanı", "Darülaceze - PERPA",
      "Okmeydanı Hastane", "Çağlayan", "Mecidiyeköy", "Zincirlikuyu", "15 Temmuz Şehitler Köprüsü",
      "Burhaniye", "Altunizade", "Acıbadem (Metrobüs)", "Uzunçayır", "Fikirtepe", "Söğütlüçeşme"
    ]
  }
};

// Yaya Aktarma Tünelleri / Yakın İstasyon Eşleşmeleri
const TRANSFER_LINKS = [
  ["Şişli - Mecidiyeköy", "Mecidiyeköy", 4],
  ["Gayrettepe", "Zincirlikuyu", 6],
  ["Ünalan", "Uzunçayır", 5],
  ["Özgürlük Meydanı", "Bakırköy", 4],
  ["İncirli", "Bakırköy - İncirli", 3],
  ["Ataköy - Şirinevler", "Şirinevler", 3],
  ["Alibeyköy", "Alibeyköy Metro", 3],
  ["Karadeniz Mahallesi", "KİPTAŞ - Venezia", 3],
  ["Bağcılar Meydan", "Bağcılar Merkez", 4],
  ["Aksaray", "Yusufpaşa", 4],
  ["Vezneciler - İstanbul Ü.", "Laleli - İstanbul Ü.", 4],
  ["Şişhane", "Tünel", 3],
  ["Karaköy", "Eminönü", 6],
  ["Kadıköy", "Ayrılık Çeşmesi", 5],
  ["Bostancı", "Bostancı (M4)", 5],
  ["Maltepe", "Maltepe (M4)", 6],
  ["Kartal", "Kartal (M4)", 6],
  ["Pendik", "Pendik (M4)", 6]
];

function formatLineLabel(lineKey) {
  const l = LINES[lineKey];
  return `${l.code} - ${l.type}`;
}

// Tüm benzersiz durakları ve hangi hatların geçtiğini çıkar
function buildStationIndex(includeConstruction) {
  const map = new Map();
  Object.entries(LINES).forEach(([key, line]) => {
    if (line.status === "construction" && !includeConstruction) return;
    line.stops.forEach(stop => {
      if (!map.has(stop)) map.set(stop, []);
      if (!map.get(stop).includes(key)) map.get(stop).push(key);
    });
  });
  return map;
}

// Autocomplete Kurulumu
function setupAutocomplete(inputId, listId) {
  const input = document.getElementById(inputId);
  const list = document.getElementById(listId);

  function renderSuggestions(query) {
    const includeConst = document.getElementById("includeConstruction").checked;
    const stationMap = buildStationIndex(includeConst);
    const q = query.trim().toLocaleLowerCase("tr-TR");
    list.innerHTML = "";

    const matches = Array.from(stationMap.keys())
      .filter(st => !q || st.toLocaleLowerCase("tr-TR").includes(q))
      .sort((a, b) => {
        const aStarts = a.toLocaleLowerCase("tr-TR").startsWith(q) ? 0 : 1;
        const bStarts = b.toLocaleLowerCase("tr-TR").startsWith(q) ? 0 : 1;
        return aStarts - bStarts || a.localeCompare(b, "tr");
      })
      .slice(0, 25);

    if (matches.length === 0) {
      list.style.display = "none";
      return;
    }

    matches.forEach(st => {
      const div = document.createElement("div");
      div.className = "autocomplete-item";
      const lines = stationMap.get(st);
      const badgesHtml = lines.map(lk =>
        `<span class="mini-badge" style="background:${LINES[lk].color}">${LINES[lk].code}</span>`
      ).join("");
      div.innerHTML = `<span>${st}</span><div class="mini-badges">${badgesHtml}</div>`;
      div.onclick = () => {
        input.value = st;
        list.style.display = "none";
      };
      list.appendChild(div);
    });
    list.style.display = "block";
  }

  input.addEventListener("input", () => renderSuggestions(input.value));
  input.addEventListener("focus", () => renderSuggestions(input.value));
  document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !list.contains(e.target)) {
      list.style.display = "none";
    }
  });
}

setupAutocomplete("fromInput", "fromList");
setupAutocomplete("toInput", "toList");

function swapStations() {
  const f = document.getElementById("fromInput");
  const t = document.getElementById("toInput");
  [f.value, t.value] = [t.value, f.value];
  if (f.value && t.value) findRoutes();
}

function setExample(from, to) {
  document.getElementById("fromInput").value = from;
  document.getElementById("toInput").value = to;
  findRoutes();
}

// Çizge Oluşturma ve Çoklu Alternatif Arama (K-En Kısa Yol Yaklaşımı)
function buildGraph(useMetrobus, includeConstruction) {
  const adj = new Map();
  const addEdge = (u, v, cost, lineKey, type, note = "") => {
    if (!adj.has(u)) adj.set(u, []);
    adj.get(u).push({ to: v, cost, lineKey, type, note });
  };

  Object.entries(LINES).forEach(([lineKey, line]) => {
    if (!useMetrobus && lineKey === "34") return;
    if (line.status === "construction" && !includeConstruction) return;

    for (let i = 0; i < line.stops.length; i++) {
      const st = line.stops[i];
      const node = `${st}||${lineKey}`;

      // Aynı duraktaki diğer hatlara aktarma
      Object.entries(LINES).forEach(([otherKey, otherLine]) => {
        if (otherKey === lineKey) return;
        if (!useMetrobus && otherKey === "34") return;
        if (otherLine.status === "construction" && !includeConstruction) return;
        if (otherLine.stops.includes(st)) {
          addEdge(node, `${st}||${otherKey}`, 5, otherKey, "transfer", `${st} istasyonunda ${formatLineLabel(otherKey)} hattına aktarma`);
        }
      });

      // Ardışık duraklar
      if (i + 1 < line.stops.length) {
        const nextSt = line.stops[i + 1];
        const nextNode = `${nextSt}||${lineKey}`;
        addEdge(node, nextNode, line.avgMinPerStop, lineKey, "ride");
        addEdge(nextNode, node, line.avgMinPerStop, lineKey, "ride");
      }
    }
  });

  // Yaya aktarma tünelleri
  TRANSFER_LINKS.forEach(([stA, stB, walkMin]) => {
    Object.entries(LINES).forEach(([keyA, lineA]) => {
      if (!useMetrobus && keyA === "34") return;
      if (lineA.status === "construction" && !includeConstruction) return;
      if (!lineA.stops.includes(stA)) return;

      Object.entries(LINES).forEach(([keyB, lineB]) => {
        if (!useMetrobus && keyB === "34") return;
        if (lineB.status === "construction" && !includeConstruction) return;
        if (!lineB.stops.includes(stB)) return;

        addEdge(`${stA}||${keyA}`, `${stB}||${keyB}`, walkMin, keyB, "walk_transfer",
          `${stA} → ${stB} yaya aktarma bağlantısı (~${walkMin} dk yürüme) ile ${formatLineLabel(keyB)} hattına geçiş`);
        addEdge(`${stB}||${keyB}`, `${stA}||${keyA}`, walkMin, keyA, "walk_transfer",
          `${stB} → ${stA} yaya aktarma bağlantısı (~${walkMin} dk yürüme) ile ${formatLineLabel(keyA)} hattına geçiş`);
      });
    });
  });

  return adj;
}

function dijkstra(adj, startStation, endStation, penaltyConfig = {}) {
  const dist = new Map();
  const prev = new Map();
  const visited = new Set();
  const pq = [];

  for (const node of adj.keys()) {
    if (node.startsWith(startStation + "||")) {
      dist.set(node, 0);
      pq.push({ node, cost: 0 });
    }
  }

  while (pq.length > 0) {
    pq.sort((a, b) => a.cost - b.cost);
    const { node, cost } = pq.shift();
    if (visited.has(node)) continue;
    visited.add(node);

    const [currStation] = node.split("||");
    if (currStation === endStation) {
      const path = [];
      let curr = node;
      while (curr) {
        path.unshift(curr);
        curr = prev.get(curr);
      }
      return path;
    }

    const edges = adj.get(node) || [];
    for (const edge of edges) {
      if (visited.has(edge.to)) continue;
      let extra = 0;
      if (edge.type === "transfer" || edge.type === "walk_transfer") {
        extra += penaltyConfig.transferPenalty || 0;
      }
      if (penaltyConfig.penalizedLines && penaltyConfig.penalizedLines.includes(edge.lineKey)) {
        extra += 18;
      }
      const newCost = cost + edge.cost + extra;
      if (newCost < (dist.get(edge.to) ?? Infinity)) {
        dist.set(edge.to, newCost);
        prev.set(edge.to, { from: node, edge });
        pq.push({ node: edge.to, cost: newCost });
      }
    }
  }
  return null;
}

function parsePath(rawPath, adj) {
  if (!rawPath || rawPath.length === 0) return null;
  const segments = [];
  let totalMin = 0;
  let totalStops = 0;

  let currentSeg = null;

  for (let i = 0; i < rawPath.length; i++) {
    const item = rawPath[i];
    if (typeof item === "string") {
      // Başlangıç düğümü
      const [st, lk] = item.split("||");
      currentSeg = {
        lineKey: lk,
        from: st,
        to: st,
        stops: [st],
        duration: 0,
        transferNoteBefore: ""
      };
    } else {
      // { from, edge } yapısı değil, prev map'i düzeltelim
    }
  }
  return null;
}

// Temiz Dijkstra & Yol Ayrıştırıcı
function searchSingleRoute(adj, startStation, endStation, penaltyConfig = {}) {
  const dist = new Map();
  const parent = new Map();
  const visited = new Set();
  const pq = [];

  for (const node of adj.keys()) {
    if (node.startsWith(startStation + "||")) {
      dist.set(node, 0);
      pq.push({ node, cost: 0 });
    }
  }

  let endNode = null;

  while (pq.length > 0) {
    pq.sort((a, b) => a.cost - b.cost);
    const { node, cost } = pq.shift();
    if (visited.has(node)) continue;
    visited.add(node);

    const [st] = node.split("||");
    if (st === endStation) {
      endNode = node;
      break;
    }

    for (const edge of (adj.get(node) || [])) {
      if (visited.has(edge.to)) continue;
      let extra = 0;
      if (edge.type === "transfer" || edge.type === "walk_transfer") {
        extra += penaltyConfig.transferPenalty || 0;
      }
      if (penaltyConfig.penalizedLines && penaltyConfig.penalizedLines.includes(edge.lineKey)) {
        extra += 22;
      }
      const nextCost = cost + edge.cost + extra;
      if (nextCost < (dist.get(edge.to) ?? Infinity)) {
        dist.set(edge.to, nextCost);
        parent.set(edge.to, { prevNode: node, edge });
        pq.push({ node: edge.to, cost: nextCost });
      }
    }
  }

  if (!endNode) return null;

  const steps = [];
  let curr = endNode;
  while (parent.has(curr)) {
    const { prevNode, edge } = parent.get(curr);
    steps.unshift({ fromNode: prevNode, toNode: curr, edge });
    curr = prevNode;
  }

  if (steps.length === 0) return null;

  // Adımları hat segmentlerine dönüştür
  const segments = [];
  let firstStation = steps[0].fromNode.split("||")[0];
  let firstLine = steps[0].fromNode.split("||")[1];
  let seg = {
    lineKey: firstLine,
    from: firstStation,
    to: firstStation,
    stops: [firstStation],
    minutes: 0,
    transferNote: ""
  };

  for (const s of steps) {
    const [toSt, toLine] = s.toNode.split("||");
    if (s.edge.type === "ride") {
      seg.to = toSt;
      seg.stops.push(toSt);
      seg.minutes += s.edge.cost;
    } else {
      if (seg.stops.length > 1) {
        segments.push(seg);
      }
      seg = {
        lineKey: toLine,
        from: toSt,
        to: toSt,
        stops: [toSt],
        minutes: s.edge.cost,
        transferNote: s.edge.note
      };
    }
  }
  if (seg.stops.length > 1) {
    segments.push(seg);
  }

  if (segments.length === 0) return null;

  // Yön bilgisi hesapla
  segments.forEach(sg => {
    const lineStops = LINES[sg.lineKey].stops;
    const idxFrom = lineStops.indexOf(sg.from);
    const idxTo = lineStops.indexOf(sg.to);
    sg.direction = idxTo > idxFrom ? `${lineStops[lineStops.length - 1]} Yönü` : `${lineStops[0]} Yönü`;
  });

  const totalStops = segments.reduce((acc, s) => acc + (s.stops.length - 1), 0);
  const totalMinutes = Math.round(segments.reduce((acc, s) => acc + s.minutes, 0));
  const signature = segments.map(s => `${s.lineKey}:${s.from}->${s.to}`).join("|");

  return {
    segments,
    transfers: segments.length - 1,
    totalStops,
    totalMinutes,
    signature
  };
}

function findRoutes() {
  const fromVal = document.getElementById("fromInput").value.trim();
  const toVal = document.getElementById("toInput").value.trim();
  const useMetrobus = document.getElementById("useMetrobus").checked;
  const includeConst = document.getElementById("includeConstruction").checked;
  const container = document.getElementById("resultsContainer");

  if (!fromVal || !toVal) {
    container.innerHTML = `<div class="empty-state">Lütfen başlangıç ve varış duraklarını seçin.</div>`;
    return;
  }
  if (fromVal === toVal) {
    container.innerHTML = `<div class="empty-state">Başlangıç ve varış durağı aynı seçildi.</div>`;
    return;
  }

  const stationIndex = buildStationIndex(includeConst);
  if (!stationIndex.has(fromVal) || !stationIndex.has(toVal)) {
    container.innerHTML = `<div class="empty-state">Girilen istasyon adları haritada bulunamadı. Lütfen açılan listeden bir durak seçin.</div>`;
    return;
  }

  const adj = buildGraph(useMetrobus, includeConst);

  // Farklı kriterlerle en fazla 4 benzersiz alternatif üret
  const strategies = [
    { label: "Önerilen (En Hızlı)", config: { transferPenalty: 3 } },
    { label: "En Az Aktarma", config: { transferPenalty: 25 } },
    { label: "Alternatif Koridor 1", config: { transferPenalty: 4, penalizedLines: [] } },
    { label: "Alternatif Koridor 2", config: { transferPenalty: 4, penalizedLines: [] } }
  ];

  const found = [];
  const seenSignatures = new Set();

  // 1. Önerilen
  const r1 = searchSingleRoute(adj, fromVal, toVal, strategies[0].config);
  if (r1) {
    r1.tag = "Önerilen";
    r1.isBest = true;
    found.push(r1);
    seenSignatures.add(r1.signature);
  }

  // 2. En az aktarmalı
  const r2 = searchSingleRoute(adj, fromVal, toVal, strategies[1].config);
  if (r2 && !seenSignatures.has(r2.signature)) {
    r2.tag = "En Az Aktarma";
    r2.isBest = false;
    found.push(r2);
    seenSignatures.add(r2.signature);
  }

  // 3. İlk rotadaki ana hattı cezalandırarak alternatif koridor bul
  if (r1) {
    const mainLine = r1.segments.reduce((a, b) => a.stops.length > b.stops.length ? a : b).lineKey;
    const r3 = searchSingleRoute(adj, fromVal, toVal, { transferPenalty: 4, penalizedLines: [mainLine] });
    if (r3 && !seenSignatures.has(r3.signature)) {
      r3.tag = "Alternatif Hat";
      r3.isBest = false;
      found.push(r3);
      seenSignatures.add(r3.signature);
    }

    // 4. Farklı ara hatları cezalandırarak 4. alternatif
    const usedLines = r1.segments.map(s => s.lineKey);
    for (const lk of usedLines) {
      const r4 = searchSingleRoute(adj, fromVal, toVal, { transferPenalty: 2, penalizedLines: [lk] });
      if (r4 && !seenSignatures.has(r4.signature)) {
        r4.tag = "Alternatif Güzergah";
        r4.isBest = false;
        found.push(r4);
        seenSignatures.add(r4.signature);
        if (found.length >= 4) break;
      }
    }
  }

  if (found.length === 0) {
    container.innerHTML = `<div class="empty-state">Seçilen filtrelerle bu iki durak arasında uygun bir raylı sistem/metrobüs rotası bulunamadı.</div>`;
    return;
  }

  renderResults(fromVal, toVal, found);
}

function renderResults(fromVal, toVal, routes) {
  const container = document.getElementById("resultsContainer");

  let html = `
    <div class="results-header">
      <h2>${fromVal} → ${toVal} (${routes.length} Alternatif Rota)</h2>
      <span class="results-hint">Detayları ve durak listesini görmek için bir alternatifin üzerine tıklayın</span>
    </div>
  `;

  routes.forEach((route, idx) => {
    const pillsHtml = route.segments.map(seg => {
      const line = LINES[seg.lineKey];
      return `<span class="line-pill" style="background:${line.color}">${formatLineLabel(seg.lineKey)}</span>`;
    }).join(`<span class="chain-arrow">➔</span>`);

    const transferText = route.transfers === 0 ? "Direkt (Aktarmasız)" : `${route.transfers} Aktarma`;

    // Akordeon Detay İçeriği
    const stepsHtml = route.segments.map((seg, sIdx) => {
      const line = LINES[seg.lineKey];
      const stopCount = seg.stops.length - 1;
      const midStops = seg.stops.slice(1, -1);
      const midId = `mid_${idx}_${sIdx}`;

      return `
        ${seg.transferNote ? `<div class="transfer-note">🔄 <strong>Aktarma:</strong> ${seg.transferNote}</div><br>` : ""}
        <div class="timeline-step" style="border-left-color:${line.color}">
          <div class="step-dot" style="border-color:${line.color}"></div>
          <div class="step-header">
            <span class="step-station">${seg.from}</span>
            <span class="line-pill" style="background:${line.color}">${formatLineLabel(seg.lineKey)}</span>
          </div>
          <div class="step-direction">
            <strong>${seg.direction}</strong> istikametine binin • <strong>${stopCount} durak</strong> (~${Math.round(seg.minutes)} dk) → <strong>${seg.to}</strong> durağında inin.
          </div>
          ${midStops.length > 0 ? `
            <button class="stops-toggle" onclick="event.stopPropagation(); document.getElementById('${midId}').classList.toggle('show')">
              Ara durakları göster/gizle (${midStops.length} durak)
            </button>
            <div id="${midId}" class="intermediate-stops">
              ${midStops.join(" • ")}
            </div>
          ` : ""}
        </div>
      `;
    }).join("");

    html += `
      <div class="route-card" id="routeCard_${idx}">
        <div class="route-summary" onclick="toggleCard(${idx})">
          <div class="route-summary-left">
            <div class="route-tag-row">
              <span class="alt-number">${idx + 1}. Alternatif</span>
              <span class="alt-badge ${route.isBest ? "best" : ""}">${route.tag}</span>
            </div>
            <div class="line-chain">${pillsHtml}</div>
          </div>
          <div class="route-summary-right">
            <div class="metrics">
              <div class="metric-time">~${route.totalMinutes} dk</div>
              <div class="metric-sub">${transferText} • ${route.totalStops} durak</div>
            </div>
            <div class="toggle-indicator" id="toggleBtn_${idx}">
              <span>Detayları Gör</span> ▾
            </div>
          </div>
        </div>
        <div class="route-details">
          <div class="timeline">
            ${stepsHtml}
            <div class="timeline-step">
              <div class="step-dot" style="border-color:#16a34a; background:#16a34a;"></div>
              <div class="step-station">🏁 ${toVal} (Varış)</div>
            </div>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function toggleCard(idx) {
  const card = document.getElementById(`routeCard_${idx}`);
  const btn = document.getElementById(`toggleBtn_${idx}`);
  const isOpen = card.classList.toggle("open");
  btn.innerHTML = isOpen ? `<span>Detayları Gizle</span> ▴` : `<span>Detayları Gör</span> ▾`;
}

// Hatlar & Duraklar Rehberi Modal Fonksiyonları
function openGuide() {
  const modal = document.getElementById("guideModal");
  const linesDiv = document.getElementById("guideLines");
  linesDiv.innerHTML = "";

  const keys = Object.keys(LINES);
  keys.forEach((key, i) => {
    const line = LINES[key];
    const btn = document.createElement("button");
    btn.className = "guide-line-btn" + (i === 0 ? " active" : "");
    btn.style.background = line.color;
    btn.textContent = formatLineLabel(key);
    btn.onclick = () => {
      document.querySelectorAll(".guide-line-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      showLineStops(key);
    };
    linesDiv.appendChild(btn);
  });

  showLineStops(keys[0]);
  modal.classList.add("show");
}

function showLineStops(key) {
  const line = LINES[key];
  document.getElementById("guideSelectedTitle").textContent =
    `${formatLineLabel(key)} — ${line.name} (${line.stops.length} Durak)`;
  const stopsDiv = document.getElementById("guideStops");
  stopsDiv.innerHTML = line.stops.map((s, idx) =>
    `<span class="guide-stop-chip"><strong>${idx + 1}.</strong> ${s}</span>`
  ).join("");
}

function closeGuide() {
  document.getElementById("guideModal").classList.remove("show");
}
</script>
</body>
</html>
"""

dosya_adi = "MetroRotaBulucu.html"
with open(dosya_adi, "w", encoding="utf-8") as f:
    f.write(html_icerik)

print(f"✅ '{dosya_adi}' başarıyla oluşturuldu ({os.path.getsize(dosya_adi) / 1024:.1f} KB).")
files.download(dosya_adi)