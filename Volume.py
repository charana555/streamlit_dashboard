import streamlit as st
import pandas as pd
from connection import get_connection
from sr_stats import stats_component

st.set_page_config(layout="wide")

# Create a connection object.
conn = get_connection()
df = conn.read(worksheet="Volume")
df.dropna(how='all' , inplace=True)

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y' , errors='coerce')
cols_to_convert = [col for col in df.columns if col not in ['Bank', 'Date']]

st.title("Amazon Metric Dashboard")

bank_list = df['Bank'].unique()
cols = st.columns(4)
with cols[0]:
    selected_bank = st.selectbox("Select a Bank", bank_list)

available_dates = df["Date"].unique()

max_date = pd.to_datetime(available_dates , format='%d/%m/%Y').max()
acc_min_date = pd.to_datetime(available_dates , format='%d/%m/%Y').min()
min_date = max_date - pd.Timedelta(days=13)

with cols[1]:
    start_date = st.date_input("Start Date", min_value=acc_min_date, max_value=max_date, value=min_date)
with cols[2]:    
    end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)


filtered_df = df.query('Bank == @selected_bank and Date >= @start_date and Date <= @end_date')
stats_component(filtered_df , selected_bank)