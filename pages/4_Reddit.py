import streamlit as st
import config
import sentiment_analysis
from composio import Composio
import pandas as pd
import matplotlib.pyplot as plt

composio = Composio(api_key=config.COMPOSIO_API_KEY)

st.title("Reddit")
st.write("It fetches commenrs from Reddit posts via Composio API, process the text for sentiment analysis, and visualize the result on a dashboard")

query = st.text_input("Enter the URL of the post...", value="")

def get_data(id, uid):
    dict = {
        "user": [],
        "data": []
    }
    result = composio.tools.execute(
                "REDDIT_RETRIEVE_POST_COMMENTS",
                arguments={
                    "article": id
                },
                user_id = uid
            )
    for i in range(len(result["data"]["comments"])):
        dict["user"].append(result["data"]["comments"][i]["author"])
        dict["data"].append(result["data"]["comments"][i]["body"])

    return dict

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
    result = sentiment_analysis.analyze_sentiment(df, text_col="data")
    fig = visualize_sentiments(result)
    st.pyplot(fig)
    st.write("Post Comments")
    st.dataframe(result[["data", "sentiment"]])

if st.button("Fetch Comments"):
    REDDIT_POST_URL = query
    REDDIT_POST_ID = REDDIT_POST_URL.split("/comments/")[1].split("/")[0]
    st.success("Showing results for the Post...")
    data = get_data(REDDIT_POST_ID, config.user_id_reddit)
    show_data(data)