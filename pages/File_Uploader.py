import streamlit as st
import pandas as pd 
from datetime import datetime
from connection import get_connection

from utils.upload_volume import upload_csv
from utils.upload_errorcodes import upload_error_csv
from utils.upload_refunds import upload_refund_csv

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

file_types = {
    "Volume" : ["SR_Vol" , "CC_TXN" ,"CALLBACK_SR" , "LITE_SR" , "MAN_EXE" , "MAN_CRE" , "ON_OFF_US"] ,
    "ErrorCodes" :[
        "Transaction Failure Error codes",
        "Refund Failure Error codes",
        "Mandate Txn Failure Error codes",
        "CREDIT CARD Error codes",
        "UPI LITE Failure Error codes",
        "MANDATE CREATION  Error codes"
    ],
    "Refunds" : [
        "Online",
        "Offline"
    ]
    } 
banks = ["AXIS"]
category = ["Volume" , "ErrorCodes" , "Refunds"]
cols = st.columns(3)

with cols[0]:
    selected_category = st.selectbox("Choose Category", category)    
with cols[1]:
    selected_file_type = st.selectbox("Choose Type of File", file_types[selected_category])
with cols[2]:
    selected_bank = st.selectbox("Choose Bank", banks)
    
if selected_category == "ErrorCodes" or selected_category == "Refunds":
    with cols[0]:
        start_date = st.date_input("Start Date")    
    with cols[1]:
        end_date = st.date_input("End Date")    

uploaded_file = st.file_uploader("Upload your file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    if st.button("Upload CSV"):
        if selected_category == "Volume":
            upload_csv(df , selected_bank , selected_file_type)
        elif selected_category == "ErrorCodes":
            upload_error_csv(df , selected_bank , selected_file_type , start_date , end_date)    
        elif selected_category == "Refunds":
            upload_refund_csv(df , selected_bank , selected_file_type , start_date , end_date)
            

    