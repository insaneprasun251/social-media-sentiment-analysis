import streamlit as st
import config
from composio import Composio
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

composio = Composio(api_key=config.COMPOSIO_API_KEY)

def get_response(q):
    response = composio.tools.execute(
        "COMPOSIO_SEARCH_TRENDS_SEARCH",
        arguments={
            "query": query,
            "data_type": "TIMESERIES"
        }
    )
    if response.get("successful"):
        raw_data = response.get("data")
        return raw_data
    else:
        print("Error:", response.get("error"))
        return {}

def get_df():
    raw_data = get_response(query)
    interest_over_time_df = pd.DataFrame(raw_data["results"]["interest_over_time"]["timeline_data"], columns = raw_data["results"]["interest_over_time"]["timeline_data"][0].keys())
    values = []
    for i in range(len(interest_over_time_df["values"])):
        values.append(int(interest_over_time_df["values"][i][0]["value"]))
    interest_over_time_df["values"] = values
    interest_over_time_df['date'] = pd.to_datetime(interest_over_time_df['timestamp'], unit='s')
    return interest_over_time_df

def show_graph():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['date'], df['values'], label='Interest Over Time', color='blue')
    ax.set_title(f'Google Trends: {query} (Last 12 Months)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Interest')
    ax.grid(alpha=0.3)
    ax.legend()
    return fig

st.title("Google Trend Search")
st.write("Here you can search for any keyword which trends on social media and can get the analytics of it.")

query = st.text_input("Enter a keyword....")

if st.button("Fetch Trends"):
    st.success(f"Showing trends for: {query}")
    df = get_df()
    fig = show_graph()
    st.pyplot(fig)