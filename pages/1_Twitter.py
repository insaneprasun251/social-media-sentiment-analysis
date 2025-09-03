import streamlit as st
import config
from composio import Composio
import pandas as pd

composio = Composio(api_key=config.COMPOSIO_API_KEY)

st.title("Twitter")
st.write("It fetches tweets via twitter API, process the text for sentiment analysis, and visualize the result on a dashboard")

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

def show_data(data):
    df = pd.DataFrame(data)
    st.dataframe(df)

if st.button("Fetch Tweets"):
    st.success(f"Showing tweets for: {query}")
    data = get_data(query, posts, config.user_id)
    show_data(data)