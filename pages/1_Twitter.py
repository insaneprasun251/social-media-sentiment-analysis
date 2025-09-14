import streamlit as st
import config
import sentiment_analysis
from composio import Composio
import pandas as pd
import matplotlib.pyplot as plt

composio = Composio(api_key=config.COMPOSIO_API_KEY)

st.title("Twitter")
st.write("It fetches tweets via Composio API, process the text for sentiment analysis, and visualize the result on a dashboard")

query = st.text_input("Enter the keyword to search")
posts = st.text_input("Enter the no. of posts you want to fetch (must be > or = 10)", 10)

def get_data(q, p, uid):
    id = []
    text = []
    result = composio.tools.execute(
                "TWITTER_RECENT_SEARCH",
                arguments={
                    "query": q + " -is:retweet -is:reply",
                    "max_results": p,
                    "tweet__fields": ["id", "text"]
                },
                user_id=uid
            )
    for i in result["data"]["data"]:
        id.append(i["id"])
        text.append(i["text"])
    data = {"id": id, "text": text}
    return data

def visualize_sentiments(result):
    sentiment_counts = result["sentiment"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=["#66bb6a", "#ef5350", "#ffee58"]
    )
    ax.axis("equal")
    plt.title("Sentiment Analysis Distribution")
    return fig

def show_data(data):
    df = pd.DataFrame(data)
    result = sentiment_analysis.analyze_sentiment(df, text_col="text")
    fig = visualize_sentiments(result)
    st.pyplot(fig)
    st.write("Tweets Data")
    st.dataframe(result[["text", "sentiment"]])

if st.button("Fetch Tweets"):
    st.success(f"Showing results for: {query}")
    data = get_data(query, posts, config.user_id_twitter)
    show_data(data)