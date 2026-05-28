import streamlit as st
import joblib

# Konfigurasi Halaman
st.set_page_config(page_title="Market Sentiment Engine", page_icon="🧠", layout="centered")

# Mengambil "Otak" AI dari folder Models
@st.cache_resource
def load_ai_brain():
    model = joblib.load('Models/sentiment_model.pkl')
    vectorizer = joblib.load('Models/tfidf_vectorizer.pkl')
    return model, vectorizer

model, vectorizer = load_ai_brain()

# Antarmuka UI (User Interface)
st.title("📰 Market Sentiment NLP Analyzer")
st.markdown("""
**Institutional AI Engine | Natural Language Processing**
Mesin kecerdasan buatan berbasis *Term Frequency-Inverse Document Frequency* (TF-IDF) dan *Naive Bayes Classifier* untuk mengekstrak sentimen pasar dari headline berita finansial secara *real-time*.
""")
st.divider()

# Input Berita
st.subheader("Market Catalyst Input")
news_input = st.text_area(
    "Masukkan Headline Berita Ekonomi / Kripto (Bahasa Inggris):", 
    "Federal Reserve announces surprise interest rate hike, crashing tech stocks"
)

# Tombol Eksekusi
if st.button("Analisis Sentimen (Run NLP) 🧠"):
    if news_input.strip() == "":
        st.warning("Teks tidak boleh kosong! Masukkan berita terlebih dahulu.")
    else:
        with st.spinner("Membedah struktur sintaksis dan probabilitas kata..."):
            # Proses Vektorisasi (Mengubah teks jadi angka)
            vectorized_text = vectorizer.transform([news_input])
            
            # Prediksi menggunakan model Naive Bayes
            prediction = model.predict(vectorized_text)[0]
            
            st.divider()
            st.subheader("Hasil Analisis AI:")
            
            # Format Output berdasarkan Sentimen
            if prediction == "Bullish":
                st.success(f"**📈 STATUS: {prediction.upper()} (SANGAT POSITIF)**")
                st.markdown("> **Interpretasi Mesin:** Sentimen pasar merespons katalis ini dengan optimisme tinggi. Potensi apresiasi harga aset / *uptrend*.")
            elif prediction == "Bearish":
                st.error(f"**🩸 STATUS: {prediction.upper()} (SANGAT NEGATIF)**")
                st.markdown("> **Interpretasi Mesin:** Terdeteksi kepanikan atau ketidakpastian. Potensi *sell-off* / tekanan jual yang tinggi di pasar.")
            else:
                st.info(f"**⚖️ STATUS: {prediction.upper()} (NETRAL)**")
                st.markdown("> **Interpretasi Mesin:** Berita ini bersifat informatif standar. Tidak ada probabilitas katalis pergerakan arah yang signifikan.")