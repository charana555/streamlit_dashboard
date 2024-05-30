import streamlit as st
from streamlit_gsheets import GSheetsConnection


@st.cache_resource
def get_connection():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn
