import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
import contractions

vader = SentimentIntensityAnalyzer()

NEGATION_WORDS = {
    "not", "no", "never", "none", "nobody", "nowhere", "neither", "nor",
    "cannot", "can't", "don't", "doesn't", "didn't", "won't", "isn't",
    "aren't", "wasn't", "weren't"
}

def remove_html(text):
    return re.sub(r'<[^>]+>', ' ', text)

def remove_urls(text):
    return re.sub(r'http\S+|www\.\S+', '', text)

def demojize_text(text):
    txt = emoji.demojize(text)
    txt = re.sub(r':([a-zA-Z0-9_+-]+):', r' \1 ', txt)
    return txt

def normalize_elongated_word(word):
    return re.sub(r'(.)\1{2,}', r'\1\1', word)

def expand_contractions(text):
    return contractions.fix(text)

def simple_negation_marking(text, scope=3):
    words = text.split()
    out = []
    neg = 0
    for w in words:
        lw = w.lower()
        if lw in NEGATION_WORDS:
            out.append(w)
            neg = scope
            continue
        if neg > 0:
            out.append('NOT_' + w)
            neg -= 1
        else:
            out.append(w)
    return ' '.join(out)

def basic_clean(text):
    if text is None:
        return ''
    text = str(text).strip().lower()
    text = remove_html(text)
    text = expand_contractions(text)
    text = demojize_text(text)
    text = remove_urls(text)
    text = ' '.join(normalize_elongated_word(w) for w in text.split())
    text = simple_negation_marking(text)
    text = re.sub(r'[^a-z0-9_\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def textblob_score(text):
    try:
        return TextBlob(text).sentiment.polarity
    except:
        return 0.0

def vader_score(text):
    return vader.polarity_scores(text)["compound"]

def custom_lexicon_score(text, lex):
    words = text.split()
    score = 0.0
    count = 0
    for w in words:
        if w.startswith('NOT_'):
            base = w[4:]
            if base in lex:
                score -= lex[base]
                count += 1
        else:
            if w in lex:
                score += lex[w]
                count += 1
    return score / count if count else 0.0

def ensemble_score(tb, vd, custom, weights=None):
    if weights is None:
        weights = {"tb": 0.4, "vader": 0.4, "custom": 0.2}
    total = 0
    denom = 0
    if tb is not None:
        total += tb * weights["tb"]
        denom += weights["tb"]
    if vd is not None:
        total += vd * weights["vader"]
        denom += weights["vader"]
    if custom is not None:
        total += custom * weights["custom"]
        denom += weights["custom"]
    return total / denom if denom else 0

def label_from_score(score):
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    return "Neutral"

def analyze_sentiment(df, text_col="text"):
    custom_lex = {
        "amazing": 0.9, "awesome": 0.9, "fantastic": 0.8, "excellent": 0.8,
        "good": 0.6, "great": 0.7, "best": 0.9, "love": 0.8, "happy": 0.7,
        "satisfied": 0.6, "worth": 0.5,
        "bad": -0.6, "poor": -0.7, "terrible": -0.9, "worst": -0.9,
        "hate": -0.9, "disappointing": -0.8, "awful": -0.8,
        "bumper": 0.7, "surplus": 0.2, "shortage": -0.6, "deficit": -0.6,
        "profit": 0.8, "loss": -0.8, "pest": -0.7, "drought": -0.8,
    }

    df = df.copy()
    df["_clean_text"] = df[text_col].apply(basic_clean)
    df["tb_score"] = df["_clean_text"].apply(textblob_score)
    df["vader_score"] = df["_clean_text"].apply(vader_score)
    df["custom_score"] = df["_clean_text"].apply(lambda t: custom_lexicon_score(t, custom_lex))
    df["ensemble"] = df.apply(lambda r: ensemble_score(r["tb_score"], r["vader_score"], r["custom_score"]), axis=1)
    df["sentiment"] = df["ensemble"].apply(label_from_score)
    return df