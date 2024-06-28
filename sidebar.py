import streamlit as st

def create_sidebar():
    st.sidebar.page_link('Volume.py')
    st.sidebar.page_link('pages/Refunds.py')
    st.sidebar.page_link('pages/Mandate.py')
    st.sidebar.page_link('pages/Credit_Card.py')
    st.sidebar.page_link('pages/UPI_Lite.py')
    st.sidebar.page_link('pages/CallBack.py')
    st.sidebar.page_link('pages/Bind_Device.py')
    st.sidebar.page_link('pages/VMN.py')
    st.sidebar.markdown('---')
    st.sidebar.page_link('pages/File_Uploader.py')
    st.sidebar.page_link('pages/Bulk_Uploader.py')    
