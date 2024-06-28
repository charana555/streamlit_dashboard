import streamlit as st
import pandas as pd
import plotly.express as px

from connection import get_connection
from sidebar import create_sidebar

st.set_page_config(layout="wide")

create_sidebar()
# Create a connection object.
conn = get_connection()
df = conn.read(worksheet="Refunds" )
st.subheader("Refunds Analytics")

date_range_list = df["DateRange"].unique()
bank_list = df['Bank'].unique()
cols = st.columns(4)
with cols[0]:
    selected_date_range = st.selectbox("Select a Date range", date_range_list)

with cols[1]:
    selected_bank = st.selectbox("Select a Bank", bank_list)


online_df = df.query('Bank == @selected_bank and DateRange == @selected_date_range and Type == "Online"')
offline_df = df.query('Bank == @selected_bank and DateRange == @selected_date_range and Type == "Offline"')


cols = st.columns(2)

with cols[0]:
    on_txn_fig = px.bar(online_df , x="status" , y="count" , labels={"status" : "Status" , "count" : "Count"} , text="count" , title=f"{selected_bank} Online Refunds")
    on_txn_fig.update_layout(xaxis_title=f'{selected_bank} Online Refunds', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(on_txn_fig)

with cols[1]:
    on_sr_fig = px.bar(online_df, x="status", y="sr", labels={"sr": "Percentage (%)", "status": "Status"} ,text=["{:.1f} %".format(value) for value in online_df["sr"]] , title=f"{selected_bank} Refunds SR" )
    on_sr_fig.update_layout(xaxis_title='Online Refunds SR', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(on_sr_fig)

with cols[0]:
    off_txn_fig = px.bar(offline_df , x="status" , y="count" , labels={"status" : "Status" , "count" : "Count"} , text="count" , title=f"{selected_bank} Offline Refunds")
    off_txn_fig.update_layout(xaxis_title=f'{selected_bank} Offline Refunds', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(off_txn_fig)

with cols[1]:
    off_sr_fig = px.bar(offline_df, x="status", y="sr", labels={"sr": "Percentage (%)", "status": "Status"} ,text=["{:.1f} %".format(value) for value in offline_df["sr"]] , title=f"{selected_bank} Refunds SR" )
    off_sr_fig.update_layout(xaxis_title='Offline Refunds SR', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(off_sr_fig)