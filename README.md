#  nlp-market-sentiment (Pro Version)

An institutional-grade real-time financial sentiment ingestion pipeline and predictive psychology analytics engine. Designed for quantitative analysis across digital assets, commodities, and forex markets (BTC, GOLD, EUR/USD), this system ingests live market headlines, computes NLP sentiment polarity indices, archives logs into a structured relational SQL database, and renders historical trend metrics.

---

##  Key Features

* **Real-Time Data Ingestion Pipeline:** Simulates an active API gateway ingestion stream that pulls highly volatile macroeconomic headlines periodically.
* **NLP Polarity Scoring Rule:** Implements automated processing to evaluate headlines, mapping numerical sentiments onto strict operational boundaries (-1.0 to +1.0) and classifying market states into Bullish, Bearish, or Neutral.
* **Persistent SQL Storage Layer:** Integrates an `SQLite3` database engine (`market_sentiment.db`) to ensure transactional persistence and permanent data auditing.
* **Live Analytics Dashboard:** Built on top of Streamlit and Plotly Express to visualize sentiment fluctuations, running rolling averages, and group polarity distribution ratios.

---

##  Repository Structure

* `dashboard.py` - Production script housing the Streamlit graphical interface, Plotly interactive trend monitors, and live manual API fetch triggers.
* `sentiment_pipeline.py` - Standalone ingestion engine simulating terminal-based streaming and database logging operations.

---

##  Tech Stack & Dependencies

* **Language:** Python
* **GUI & Reactive Components:** Streamlit
* **Geospatial & Statistical Plots:** Plotly Express
* **Database Architecture:** SQLite3 (Native Python Module)
* **Data Manipulation Pipelines:** Pandas, NumPy

---

##  Installation & Deployment Guide

1. **Clone the Repository:**
```bash
   git clone [https://github.com/dimssrmdn01/nlp-market-sentiment.git](https://github.com/dimssrmdn01/nlp-market-sentiment.git)
   cd nlp-market-sentiment
   ```

2. **Install Core Analytical Libraries:**
```bash
   pip install streamlit plotly pandas numpy
   ```

3. **Initialize Ingestion Stream via Terminal (Optional):**
```bash
   python sentiment_pipeline.py
   ```

4. **Launch the Live Sentiment Dashboard:**
```bash
   streamlit run dashboard.py
   ```

---

##  Database Schema & Compliance Standard

| Field Name | Storage Class | System Importance |
| :--- | :--- | :--- |
| **timestamp** | TEXT | Temporal registration for time-series drift calculations. |
| **asset_ticker** | TEXT | Relational target key isolating market assets (BTC, GOLD, EUR/USD). |
| **headline** | TEXT | Raw natural language string ingested from market news vendors. |
| **sentiment_score** | REAL | Float bounded between $-1.0$ and $+1.0$ tracking market psychology severity. |
| **sentiment_label** | TEXT | Categorical flag routing trading signals (BULLISH, BEARISH, NEUTRAL). |
