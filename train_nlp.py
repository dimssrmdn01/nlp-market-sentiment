import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# 1. Pastikan folder Models tersedia
os.makedirs('Models', exist_ok=True)

# 2. EKSPANSI DATASET: Menyuntikkan Variasi Teks Finansial yang Seimbang
data = {
    'headline': [
        # --- KELOMPOK FEDERAL RESERVE (Menghilangkan Bias) ---
        "Federal Reserve cuts interest rates to stimulate economic growth",
        "Fed hints at upcoming rate cuts, boosting investor confidence",
        "Federal Reserve dovish stance ignites massive stock market rally",
        "Federal Reserve announces surprise interest rate hike, crashing tech stocks",
        "Fed aggressive rate hikes spark widespread recession fears",
        "Federal Reserve hawkish tone dampens market sentiment, stocks slide",
        "Federal Reserve keeps interest rates unchanged at current levels",
        
        # --- KELOMPOK BULLISH (Sentimen Positif / Uptrend) ---
        "Bitcoin surges past historic highs as institutional adoption accelerates",
        "Tech giants report record-breaking Q2 earnings, shares skyrocket",
        "Gold prices hit new all-time high amid surging safe-haven demand",
        "Oil prices rally strongly following unexpected supply constraints",
        "E-commerce sector sees massive revenue growth during holiday season",
        "Corporate profits jump by 15 percent, beating Wall Street consensus",
        
        # --- KELOMPOK BEARISH (Sentimen Negatif / Downtrend) ---
        "Crypto market loses billions in sudden panic selling wave",
        "Manufacturing sector activity shrinks at fastest pace in three years",
        "S&P 500 plunges as global supply chain disruptions worsen",
        "Crude oil prices collapse as global demand weakens dramatically",
        "Banking stocks tumble after major regional lender faces liquidity crisis",
        "Regulatory crackdown on tech monopolies triggers heavy market sell-off",
        
        # --- KELOMPOK NEUTRAL (Informasi Standar / Konsolidasi) ---
        "Company XYZ reports standard Q3 earnings matching analyst estimates",
        "Market trading volume remains flat ahead of national holiday",
        "New regulatory framework for corporate tax introduced by government",
        "Analysts project stable economic growth for the next fiscal quarter",
        "Gold prices consolidate in a narrow range during morning session",
        "Central bank releases its monthly statistical report on inflation data"
    ],
    'sentiment': [
        # Label untuk Fed
        "Bullish", "Bullish", "Bullish", "Bearish", "Bearish", "Bearish", "Neutral",
        # Label Bullish
        "Bullish", "Bullish", "Bullish", "Bullish", "Bullish", "Bullish",
        # Label Bearish
        "Bearish", "Bearish", "Bearish", "Bearish", "Bearish", "Bearish",
        # Label Neutral
        "Neutral", "Neutral", "Neutral", "Neutral", "Neutral", "Neutral"
    ]
}

df = pd.DataFrame(data)
print(f"Dataset baru berhasil disuntikkan! Total data latih: {len(df)} headline.")
print("Memulai ekstraksi fitur TF-IDF...")

# 3. Text Vectorization (TF-IDF) dengan N-Grams
# ngram_range=(1,2) membuat AI tidak hanya membaca per kata, tapi juga kombinasi 2 kata (misal: 'rate hike')
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
model = MultinomialNB()

# Transformasi teks ke matriks angka
X = vectorizer.fit_transform(df['headline'])
y = df['sentiment']

# Latih ulang model probabilitas
model.fit(X, y)

# 4. Ekspor Ulang Otak AI yang Baru
joblib.dump(model, 'Models/sentiment_model.pkl')
joblib.dump(vectorizer, 'Models/tfidf_vectorizer.pkl')

print("RE-TRAINING SELESAI! Otak AI baru yang lebih jenius berhasil di-ekspor!")