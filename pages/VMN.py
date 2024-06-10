import streamlit as st
import pandas as pd
import plotly.express as px

from connection import get_connection

st.set_page_config(layout='wide')

conn = get_connection()
df = conn.read(worksheet='VMN')
st.subheader("VMN Analytics")

date_range_list = df["DateRange"].unique()
bank_list = df['Bank'].unique()
cols = st.columns(4)
with cols[0]:
    selected_date_range = st.selectbox("Select a Date range", date_range_list)

with cols[1]:
    selected_bank = st.selectbox("Select a Bank", bank_list)


filtered_df = df.query('Bank == @selected_bank and DateRange == @selected_date_range')

on_txn_fig = px.bar(
    filtered_df , x="aggregator" , 
    y="successRate" , 
    labels={"aggregator" : "Status" , "successRate" : "SR"} , 
    text="successRate" , 
    title=f"{selected_bank} VMN SR",
    )
on_txn_fig.update_layout(xaxis_title=f'{selected_bank} Aggregators', yaxis_title='SR', title_x=0.5)
st.plotly_chart(on_txn_fig)