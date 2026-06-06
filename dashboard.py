import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import random
from datetime import datetime

st.set_page_config(page_title="Financial Sentiment Analytics", layout="wide", page_icon="📈")

# ==========================================
# 1. CORE ENGINE & DATABASE INTERACTION
# ==========================================
def fetch_sentiment_data():
    conn = sqlite3.connect('market_sentiment.db')
    # Menarik seluruh riwayat log sentimen dari database
    df = pd.read_sql_query("SELECT * FROM news_sentiment_logs ORDER BY timestamp ASC", conn)
    conn.close()
    return df

def inject_single_live_feed(ticker, headline, score, label):
    conn = sqlite3.connect('market_sentiment.db')
    cursor = conn.cursor()
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO news_sentiment_logs (timestamp, asset_ticker, headline, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?, ?)
    ''', (waktu_sekarang, ticker, headline, score, label))
    conn.commit()
    conn.close()

def generate_mock_api_feed():
    headlines_pool = {
        'BTC': [
            ("Bitcoin breaks resistance level, target set for new all-time high", 0.85),
            ("Regulatory concerns spark minor sell-off in major crypto assets", -0.45),
            ("Institutional adoption surges as new spot ETFs gain heavy volume", 0.78),
            ("Whale wallets transfer huge volume to exchanges, downside risk expected", -0.60)
        ],
        'GOLD': [
            ("Gold prices hold steady amid global macroeconomic uncertainty", 0.15),
            ("Inflation fears push gold to near-record levels as safe haven", 0.65),
            ("Stronger dollar pressures gold futures causing a sudden drop", -0.55)
        ],
        'EUR/USD': [
            ("Central bank hints at upcoming interest rate cuts next quarter", -0.35),
            ("Economic growth data beats consensus, boosting local currency", 0.60)
        ]
    }
    ticker = random.choice(list(headlines_pool.keys()))
    headline, base_score = random.choice(headlines_pool[ticker])
    final_score = round(base_score + random.uniform(-0.1, 0.1), 2)
    final_score = max(min(final_score, 1.0), -1.0)
    
    label = 'BULLISH' if final_score > 0.2 else ('BEARISH' if final_score < -0.2 else 'NEUTRAL')
    return ticker, headline, final_score, label

# ==========================================
# 2. INTERFACE RENDERER
# ==========================================
st.title("📈 Market Sentiment Analytics Dashboard")
st.subheader("NLP-Driven Ingestion Pipeline & Live Psychology Tracker")
st.write("---")

# Load Data Awal
df_sentiment = fetch_sentiment_data()

# Sidebar: Tombol Trigger Ingestion Manual
st.sidebar.header("🔌 Live API Stream Gateway")
st.sidebar.write("Simulasikan penarikan berita finansial terbaru secara real-time.")
if st.sidebar.button("⚡ Fetch & Process New Headline"):
    t, h, s, l = generate_mock_api_feed()
    inject_single_live_feed(t, h, s, l)
    st.sidebar.success(f"Berhasil memproses headline untuk {t}!")
    # Re-fetch data setelah data baru masuk
    df_sentiment = fetch_sentiment_data()

if not df_sentiment.empty:
    # 3. KARTU METRIK UTAMA (KPI CARDS)
    total_headlines = len(df_sentiment)
    avg_score = df_sentiment['sentiment_score'].mean()
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="📊 Total Headline Diproses", value=f"{total_headlines} Berita")
    with m2:
        st.metric(label="🧠 Rata-Rata Skor Sentimen Pasar", value=f"{round(avg_score, 2)}", 
                  delta="Bullish Bias" if avg_score > 0 else "Bearish Bias")
    with m3:
        status_sistem = "ACTIVE" if total_headlines > 0 else "IDLE"
        st.metric(label="🟢 Status Pipeline Ingestion", value=status_sistem)
        
    st.write("---")
    
    # 4. GRID VISUALISASI UTAMA
    col1, col2 = st.columns([1.8, 1.2])
    
    with col1:
        st.markdown("### 📉 Tren Fluktuasi Sentimen Historis")
        # Line chart tren menggunakan Plotly
        fig_line = px.line(df_sentiment, x='timestamp', y='sentiment_score', color='asset_ticker',
                           title="Pergerakan Skor Sentimen Sentimen Per Aset",
                           labels={'sentiment_score': 'Skor Sentimen', 'timestamp': 'Waktu Deteksi'},
                           markers=True, color_discrete_sequence=px.colors.qualitative.Bold)
        fig_line.update_layout(height=400, yaxis_range=[-1.1, 1.1])
        st.plotly_chart(fig_line, use_container_width=True)
        
    with col2:
        st.markdown("### 📊 Proporsi Polaritas Pasar")
        # Bar chart sebaran klasifikasi sentimen
        fig_bar = px.histogram(df_sentiment, x='asset_ticker', color='sentiment_label',
                               title="Distribusi Klasifikasi Bullish vs Bearish",
                               barmode='group', color_discrete_map={'BULLISH': '#00CC96', 'BEARISH': '#EF553B', 'NEUTRAL': '#636EFA'})
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.write("---")
    
    # 5. HISTORICAL DATAFRAME FROM SQL
    st.markdown("### 🔍 Transkrip Audit Log Sentiment Terbaru (Live Query SQL)")
    st.dataframe(df_sentiment[['timestamp', 'asset_ticker', 'headline', 'sentiment_score', 'sentiment_label']].sort_values(by='timestamp', ascending=False), use_container_width=True)

else:
    st.info("Database `market_sentiment.db` masih kosong. Silakan klik tombol '⚡ Fetch & Process New Headline' di sidebar untuk mengalirkan data pertama.")