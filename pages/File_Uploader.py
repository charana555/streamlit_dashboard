import streamlit as st
import pandas as pd 
from datetime import datetime

from utils.upload_volume import upload_csv
from utils.upload_errorcodes import upload_error_csv
from utils.upload_refunds import upload_refund_csv
from utils.upload_vmn import upload_vmn_csv
from utils.upload_bind_device import upload_bind_csv

st.set_page_config(layout='wide')

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
    ],
    "VMN" :["VMN"],
    "BindDevice" : ["BindDevice"]
    } 
banks = ["AXIS"]
category = ["Volume" , "ErrorCodes" , "Refunds" , "VMN" , "BindDevice"]
cols = st.columns(3)

with cols[0]:
    selected_category = st.selectbox("Choose Category", category)    
with cols[1]:
    selected_file_type = st.selectbox("Choose Type of File", file_types[selected_category])
with cols[2]:
    selected_bank = st.selectbox("Choose Bank", banks)
    
if selected_category != "Volume":
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
        elif selected_category == "VMN":
            upload_vmn_csv(df , selected_bank , start_date , end_date)
        elif selected_category == "BindDevice":
            upload_bind_csv(df , selected_bank)
            

        st.success(f"{uploaded_file.name} file processed successfully!")
        st.cache_data.clear()