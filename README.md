# 🛍️ AI Humanisation & Personalised Shopping & Productivity Agent

An intelligent, multi-step agent designed to save hours of manual online shopping for busy individuals. It personalizes recommendations according to your exact sizing and style preferences, searches across major Indian and international e-commerce platforms (Amazon, Myntra, Ajio, Flipkart, Noon), forensically filters out fake/bot reviews and low-quality sellers, compares effective prices with coupons/bank offers, and provides direct verified purchase links.

---

## 🏗️ Project Architecture

```
Humanisation@dubai AI/
│
├── app.py              # Streamlit Web UI (Sidebar preferences, chat interface, cards, comparison table)
├── agent.py            # Core Agent Logic (4-Step Workflow: Persona Analyzer, Deep Search, Review Audit, Price Arbitrage)
├── requirements.txt    # Python dependencies (streamlit, google-genai, tavily-python, pandas, etc.)
├── .env                # API keys configuration file
├── .env.example        # Example environment variables template
└── README.md           # Documentation & instructions
```

---

## ⚡ The 4-Step Agent Workflow

1. **Step 1: Requirement Analyzer (Personalization & Persona Mapping)**
   - Synthesizes user natural language requests with saved sidebar preferences (sizes, brand affinities, budget range, style).
   - Formulates targeted search strategies for e-commerce engines.
2. **Step 2: Multi-Platform Deep Search**
   - Uses Tavily Search API to query targeted e-commerce platforms (`Amazon.in`, `Myntra`, `Ajio`, `Flipkart`, `Noon`).
3. **Step 3: Authenticity & Fake Review Guardian**
   - Applies Gemini 2.5 Flash reasoning to evaluate customer review distribution, detect bot review patterns, verify seller credentials, and confirm fabric composition integrity.
4. **Step 4: Cross-Platform Price & Genuine Offer Comparison**
   - Calculates effective prices taking into account active coupons (e.g. `FESTIVE10`, `AJIOMANIA`) and instant bank card discounts (e.g. HDFC/ICICI 10% off).
   - Generates the Top 3 Genuine Recommendations and a side-by-side comparison matrix.

---

## 🚀 Setup & Execution

### 1. Configure API Keys
Obtain your API keys:
- **Gemini API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Tavily Search API Key**: [Tavily AI](https://tavily.com)

Place them in the `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```
*(Alternatively, you can paste them directly into the Streamlit sidebar during runtime!)*

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit App
```bash
streamlit run app.py
```
Then open [http://localhost:8501](http://localhost:8501) in your browser.
