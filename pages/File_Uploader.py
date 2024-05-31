import streamlit as st
import pandas as pd 
from datetime import datetime
from connection import get_connection

from utils.upload_volume import upload_csv

st.set_page_config(layout='wide')

def update_sheet(existing_data, data):
    for _, row in data.iterrows():
        date, bank = row['Date'], row['Bank']
        # Check if the date and bank already exist
        match = existing_data[(existing_data['Date'] == date) & (existing_data['Bank'] == bank)]
        if not match.empty:
            # Update existing row
            for col in data.columns:
                if col != 'Date' and col != 'Bank':
                    existing_data.loc[match.index, col] = row[col]
        else:
            # Append new row
            existing_data = existing_data.append(row, ignore_index=True)
    return existing_data

file_types = ["SR_Vol" , "CC_TXN"] 
banks = ["AXIS"]

sr_col_list = [
    "Date", "Bank", "P2M_Pay_Volume", "P2M_COLLECT_Volume", "P2P_Pay_Volume",
    "P2P_COLLECT_Volume", "P2M_Pay_Succvolume", "P2M_Collect_Succvolume",
    "P2P_Pay_Succvolume", "P2P_Collect_Succvolume", "CREDIT CARD Volume",
    "CREDIT CARD Succvolume", "CALLBACK Volume", "CALLBACK Succvolume",
    "UPI LITE Volume", "UPI LITE Succvolume", "Mandate Volume Execution",
    "Mandate SuccVolume Execution", "Mandate creation Vol",
    "Mandate creation succvol", "CC ONUS Vol", "CC OFFUS VOL",
    "CC ONUS sUCC-Vol", "CC OFFUS Succ-VOL"
]

cols = st.columns(4)

with cols[0]:
    selected_file_type = st.selectbox("Choose Type of File", file_types)
with cols[1]:
    selected_bank = st.selectbox("Choose Bank", banks)

uploaded_file = st.file_uploader("Upload your file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    if st.button("Upload CSV"):
        upload_csv(df , selected_bank , selected_file_type)
    
    

    