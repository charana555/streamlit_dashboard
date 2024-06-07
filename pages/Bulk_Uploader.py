import streamlit as st
import re
import pandas as pd
from utils.upload_volume import upload_csv
from utils.upload_errorcodes import upload_error_csv
from utils.upload_refunds import upload_refund_csv
from utils.upload_vmn import upload_vmn_csv

st.set_page_config(layout='wide')

file_name_keywords = [
    'srvol',
    'CCTXN' ,
    'CallbackSR' ,
    'LITESR' ,
    'LITEEC' ,
    'mandtxnvol' ,
    'txnerror' ,
    'referror' ,
    'CCTXNerrorcode' ,
    'mandateerror' ,
    'Offrefund' ,
    'Onlrefund' ,
    'VMN'
]

file_name_category_mapper = {
    'srvol': 'Volume',
    'CCTXN' : 'Volume',
    'CallbackSR' : 'Volume',
    'LITESR' : 'Volume',
    'mandtxnvol' : 'Volume',
    'txnerror' : 'ErrorCodes',
    'referror' : 'ErrorCodes',
    'CCTXNerrorcode' : 'ErrorCodes',
    'mandateerror' : 'ErrorCodes',
    'LITEEC' : 'ErrorCodes',
    'Offrefund' : 'Refunds',
    'Onlrefund' : 'Refunds',
    'VMN' : 'VMN'
}

file_name_type_mapper = {
    'srvol': 'SR_Vol',
    'CCTXN' : 'CC_TXN',
    'CallbackSR' : 'CALLBACK_SR',
    'LITESR' : 'LITE_SR',
    'mandtxnvol' : 'MAN_EXE',
    'txnerror' : 'Transaction Failure Error codes',
    'referror' : 'Refund Failure Error codes',
    'CCTXNerrorcode' : 'CREDIT CARD Error codes',
    'mandateerror' : 'Mandate Txn Failure Error codes',
    'LITEEC' : 'UPI LITE Failure Error codes',
    'Offrefund' : 'Offline',
    'Onlrefund' : 'Online',
    'VMN' :'VMN'
}

banks = ["AXIS" , "YAPL" , "RAPL"]

# Function to find matching keywords in file name
def find_matching_keyword(uploaded_file_name, keywords):
    for keyword in keywords:
        # Use case-insensitive regex to match keyword in file name
        pattern = re.compile(r'\b{}\b'.format(re.escape(keyword)), re.IGNORECASE)
        if pattern.search(uploaded_file_name.replace('_', ' ')):
            return keyword
    return None

cols = st.columns(3)
with cols[0]:
        start_date = st.date_input("Start Date")    
with cols[1]:
        end_date = st.date_input("End Date")  
with cols[2]:
    selected_bank = st.selectbox("Choose Bank", banks)
    
      

uploaded_files = st.file_uploader("Upload your files" , accept_multiple_files=True)
if st.button("Upload CSV"):
    if uploaded_files:
        for file in uploaded_files:
            with st.spinner(f"Processing {file.name}..."):
                keyword = find_matching_keyword(file.name, file_name_keywords)
                if keyword:
                    selected_category = file_name_category_mapper[keyword]
                    selected_file_type = file_name_type_mapper[keyword]
                    df = pd.read_csv(file)
                    if selected_category == "Volume":
                        upload_csv(df , selected_bank , selected_file_type)
                    elif selected_category == "ErrorCodes":
                        upload_error_csv(df , selected_bank , selected_file_type , start_date , end_date)    
                    elif selected_category == "Refunds":
                        upload_refund_csv(df , selected_bank , selected_file_type , start_date , end_date)
                    elif selected_category == "VMN":
                        upload_vmn_csv(df , selected_bank , start_date , end_date)

                    st.success(f"{file.name} file processed successfully!")
                    st.cache_data.clear()