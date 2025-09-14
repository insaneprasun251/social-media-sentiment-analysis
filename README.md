# Social Media Sentiment Analysis

This project is an interactive web app built with **Python** and **Streamlit** for performing **sentiment analysis** on real-time social media data.  
It fetches posts and comments from platforms like Twitter, Instagram, YouTube, Facebook, LinkedIn, and Reddit, and applies NLP techniques to classify sentiments as **Positive, Negative, or Neutral**.

---

## 🚀 Features

- Multi-platform support: Twitter, Instagram, YouTube, Facebook, LinkedIn, Reddit
- Real-time sentiment analysis of social media posts
- Visualization of results with charts and graphs
- Export options for further analysis
- Simple and interactive Streamlit UI

---

## 🛠️ Project Structure

```
├── Home.py                # Main Streamlit app entry point
├── sentiment_analysis.py  # Core logic for fetching & analyzing data
├── config.py              # Configuration (API keys, thresholds, parameters)
├── requirements.txt       # Dependencies
├── pages/                 # Additional app pages for Streamlit
└── README.md              # Project documentation
```

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/insaneprasun251/social-media-sentiment-analysis.git
   cd social-media-sentiment-analysis
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your API keys in `config.py`.

---

## ▶️ Usage

Run the Streamlit app:
```bash
streamlit run Home.py
```

Open the app in your browser at **http://localhost:8501/**.

---

## 📊 Example Outputs

- **Sentiment Distribution Pie Chart**
- **Trend Line of Positive/Negative mentions over time**
- **Table of analyzed posts with predicted sentiment**

---

## ⚠️ Notes

- APIs may require proper credentials and are subject to rate limits.
- Accuracy depends on text preprocessing and the sentiment model used.
- Social media slang, sarcasm, and multilingual posts may affect results.

---

## 🔮 Future Improvements

- Transformer-based models (BERT, RoBERTa) for better accuracy
- Multilingual sentiment analysis support
- Real-time alerts for sudden sentiment changes
- Modular plugin-like architecture for adding more platforms

---

## 🤝 Contributing

Contributions are welcome! Please fork this repo, create a new branch, and submit a pull request.
