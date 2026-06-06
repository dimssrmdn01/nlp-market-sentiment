import pandas as pd
import numpy as np
import sqlite3
import time
import random
from datetime import datetime

# ==========================================
# 1. INITIALIZATION & DATABASE LAYER
# ==========================================
def init_sentiment_db():
    conn = sqlite3.connect('market_sentiment.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_sentiment_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            asset_ticker TEXT,
            headline TEXT,
            sentiment_score REAL,
            sentiment_label TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_sentiment_to_sql(ticker, headline, score, label):
    conn = sqlite3.connect('market_sentiment.db')
    cursor = conn.cursor()
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO news_sentiment_logs (timestamp, asset_ticker, headline, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?)
    ''', (waktu_sekarang, ticker, headline, score, label))
    conn.commit()
    conn.close()

# ==========================================
# 2. MOCK LIVE FINANCIAL API STREAM
# ==========================================
def simulate_market_news_api():
    headlines_pool = {
        'BTC': [
            ("Bitcoin breaks resistance level, target set for new all-time high", 0.85),
            ("Regulatory concerns spark minor sell-off in major crypto assets", -0.45),
            ("Institutional adoption surges as new spot ETFs gain heavy volume", 0.78),
            ("Whale wallets transfer huge volume to exchanges, downside risk expected", -0.60),
            ("Network hash rate hits record high, reinforcing security metrics", 0.50)
        ],
        'GOLD': [
            ("Gold prices hold steady amid global macroeconomic uncertainty", 0.15),
            ("Inflation fears push gold to near-record levels as safe haven", 0.65),
            ("Stronger dollar pressures gold futures causing a sudden drop", -0.55),
            ("Central banks continue aggressive gold accumulation strategies", 0.70)
        ],
        'EUR/USD': [
            ("Central bank hints at upcoming interest rate cuts next quarter", -0.35),
            ("Economic growth data beats consensus, boosting local currency", 0.60),
            ("Trade deficit widens causing temporary market volatility", -0.40)
        ]
    }
    
    ticker = random.choice(list(headlines_pool.keys()))
    headline, base_score = random.choice(headlines_pool[ticker])
    
    # Suntik sedikit noise statistik agar score tidak selalu kaku
    final_score = round(clip_value(base_score + random.uniform(-0.1, 0.1), -1.0, 1.0), 2)
    
    if final_score > 0.2:
        label = 'BULLISH'
    elif final_score < -0.2:
        label = 'BEARISH'
    else:
        label = 'NEUTRAL'
        
    return ticker, headline, final_score, label

def clip_value(val, min_val, max_val):
    return max(min(val, max_val), min_val)

# ==========================================
# 3. CORE INGESTION PIPELINE EXECUTION
# ==========================================
init_sentiment_db()

print("=== 📈 REAL-TIME FINANCIAL SENTIMENT INGESTION PIPELINE ===")
print("Memulai pemantauan API berita pasar finansial... (Tekan Ctrl+C untuk berhenti)\n")

try:
    # Jalankan simulasi ingestion sebanyak 5 iterasi awal secara otomatis
    for i in range(1, 6):
        ticker, headline, score, label = simulate_market_news_api()
        
        # Eksekusi pipeline pengolahan dan komit ke database SQL
        save_sentiment_to_sql(ticker, headline, score, label)
        
        print(f"[LOG {i}] Berhasil memproses data dari API Feed:")
        print(f" └─ Aset      : {ticker}")
        print(f" └─ Headline  : \"{headline}\"")
        print(f" └─ Sentimen  : {score} ({label})")
        print(f" └─ Database  : Terkunci ke `market_sentiment.db` 🔒\n")
        
        # Delay simulasi jeda waktu streaming data
        time.sleep(1.5)
        
    print("="*60)
    print("🔍 VERIFIKASI DATA PERSISTENCE: ISI DATABASE SAAT INI")
    print("="*60)
    
    conn = sqlite3.connect('market_sentiment.db')
    df_preview = pd.read_sql_query("SELECT * FROM news_sentiment_logs ORDER BY id DESC LIMIT 5", conn)
    conn.close()
    
    print(df_preview.to_string(index=False))

except KeyboardInterrupt:
    print("\nPipeline dihentikan dengan aman oleh pengguna.")