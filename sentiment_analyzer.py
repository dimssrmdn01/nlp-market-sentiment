import pandas as pd
import numpy as np
import re

berita_pasar = [
    "Bitcoin price breaks historical resistance, signaling massive bull run ahead",
    "Fears of strict government regulations trigger panic selling in crypto market",
    "Ethereum network upgrade successfully completed with high adoption rate",
    "Whales dump millions of dollars in assets as inflation concerns rise",
    "Gold prices remain steady and unchanged during the weekend market closure"
]

kamus_sentimen = {
    'bull': 2, 'break': 1, 'resistance': 1, 'success': 2, 'upgrade': 1,
    'adoption': 1, 'gain': 1, 'growth': 1, 'support': 1,
    'panic': -2, 'sell': -1, 'dump': -2, 'fear': -1, 'crash': -2,
    'inflation': -1, 'drop': -1, 'risk': -1, 'decline': -1
}

def bersihkan_teks(teks):
    teks = teks.lower()
    teks = re.sub(r'[^a-zA-Z\s]', '', teks)
    tokens = teks.split()
    return tokens

def hitung_skor_sentimen(tokens):
    skor = 0
    for token in tokens:
        if token in kamus_sentimen:
            skor += kamus_sentimen[token]
    return skor

def kategorisasi_sentimen(skor):
    if skor > 0:
        return "🟢 BULLISH"
    elif skor < 0:
        return "🔴 BEARISH"
    else:
        return "⚪ NEUTRAL"

print("=== 🤖 NLP FINANCIAL SENTIMENT ENGINE ===")
print("Berhasil memuat pipeline pemrosesan teks murni.\n")

data_analisis = []
for teks in berita_pasar:
    tokens_bersih = bersihkan_teks(teks)
    skor = hitung_skor_sentimen(tokens_bersih)
    label = kategorisasi_sentimen(skor)
    
    data_analisis.append({
        'Headline Berita': teks,
        'Skor': skor,
        'Sentimen': label
    })

df_sentimen = pd.DataFrame(data_analisis)
print(df_sentimen.to_string(index=False))

print("\n" + "="*50 + "\n")
total_bullish = np.sum(df_sentimen['Sentimen'] == "🟢 BULLISH")
total_bearish = np.sum(df_sentimen['Sentimen'] == "🔴 BEARISH")
indeks_sentimen = (total_bullish - total_bearish) / len(berita_pasar)

print("--- 📊 RINGKASAN INDEKS SENTIMEN PASAR ---")
print(f"Total Berita Bullish : {total_bullish}")
print(f"Total Berita Bearish : {total_bearish}")
print(f"Indeks Agregat Pasar : {indeks_sentimen:.2f}")