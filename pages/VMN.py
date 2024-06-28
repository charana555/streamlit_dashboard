import streamlit as st
import pandas as pd
import plotly.express as px

from sidebar import create_sidebar

from connection import get_connection


st.set_page_config(layout='wide')
create_sidebar()

conn = get_connection()
df = conn.read(worksheet='VMN')
st.subheader("VMN Analytics")

date_range_list = df["DateRange"].unique()
bank_list = df['Bank'].unique()
cols = st.columns(4)
with cols[0]:
    selected_date_range = st.selectbox("Select a Date range", date_range_list)

# with cols[1]:
#     selected_bank = st.selectbox("Select a Bank", bank_list)


# filtered_df = df.query('Bank == @selected_bank and DateRange == @selected_date_range')

axis_df = df.query('Bank == "AXIS" and DateRange == @selected_date_range')
yapl_df = df.query('Bank == "YAPL" and DateRange == @selected_date_range')
rapl_df = df.query('Bank == "RAPL" and DateRange == @selected_date_range')

axis_txn_fig = px.bar(
    axis_df , x="aggregator" , 
    y="successRate" , 
    labels={"aggregator" : "Status" , "successRate" : "SR"} , 
    text="successRate" , 
    title=f"AXIS VMN SR",
    )
axis_txn_fig.update_layout(xaxis_title=f'AXIS Aggregators', yaxis_title='SR', title_x=0.5)
st.plotly_chart(axis_txn_fig)

yapl_txn_fig = px.bar(
    yapl_df , x="aggregator" , 
    y="successRate" , 
    labels={"aggregator" : "Status" , "successRate" : "SR"} , 
    text="successRate" , 
    title=f"YAPL VMN SR",
    )
yapl_txn_fig.update_layout(xaxis_title=f'YAPL Aggregators', yaxis_title='SR', title_x=0.5)
st.plotly_chart(yapl_txn_fig)

rapl_txn_fig = px.bar(
    rapl_df , x="aggregator" , 
    y="successRate" , 
    labels={"aggregator" : "Status" , "successRate" : "SR"} , 
    text="successRate" , 
    title=f"RAPL VMN SR",
    )
rapl_txn_fig.update_layout(xaxis_title=f'RAPL Aggregators', yaxis_title='SR', title_x=0.5)
st.plotly_chart(rapl_txn_fig)