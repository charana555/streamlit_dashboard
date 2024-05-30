import streamlit as st
import pandas as pd
import plotly.express as px

from connection import get_connection

st.set_page_config(layout="wide")

# Create a connection object.
conn = get_connection()
df = conn.read(worksheet="ErrorCodes" )
df = df.groupby(['error', 'DateRange', 'Type', 'Bank']).sum().reset_index()
st.subheader("Error Codes Analytics")

date_range_list = df["DateRange"].unique()
bank_list = df['Bank'].unique()
cols = st.columns(4)
with cols[0]:
    selected_date_range = st.selectbox("Select a Date range", date_range_list)

with cols[1]:
    selected_bank = st.selectbox("Select a Bank", bank_list)



npci_data = conn.read(worksheet="NPCIErrorCodes")

filtered_df = df.query('Bank == @selected_bank and DateRange == @selected_date_range')

txn_error = filtered_df.query('Type == "Transaction Failure Error codes"').sort_values(by='count' , ascending=False).head(10)
ref_error = filtered_df.query('Type == "Refund Failure Error codes"').sort_values(by='count' , ascending=False).head(10)
man_error = filtered_df.query('Type == "Mandate Txn Failure Error codes"').sort_values(by='count' , ascending=False).head(10)
cc_error = filtered_df.query('Type == "CREDIT CARD Error codes"').sort_values(by='count' , ascending=False).head(10)
lite_error = filtered_df.query('Type == "UPI LITE Failure Error codes"').sort_values(by='count' , ascending=False).head(10)
man_cre_error = filtered_df.query('Type == "MANDATE CREATION  Error codes"').sort_values(by='count' , ascending=False).head(10)

cols = st.columns(2)

with cols[0]:
    txn_fig = px.bar(txn_error , x="error" , y="count" , labels={"error" : "Error Codes" , "count" : "Count"} , text="count" , title="Top 10 TXN Error Codes")
    txn_fig.update_layout(xaxis_title='Error Code', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(txn_fig)

with cols[1]:
    ref_fig = px.bar(ref_error , x="error" , y="count" , labels={"error" : "Error Codes" , "count" : "Count"} , text="count" , title="Top 10 Refund Error Codes")
    ref_fig.update_layout(xaxis_title='Error Code', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(ref_fig)

with cols[0]:
    man_fig = px.bar(man_error , x="error" , y="count" , labels={"error" : "Error Codes" , "count" : "Count"} , text="count" , title="Top 10 Mandate Error Codes")
    man_fig.update_layout(xaxis_title='Error Code', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(man_fig)

with cols[1]:
    man_cre_fig = px.bar(man_cre_error , x="error" , y="count" , labels={"error" : "Error Codes" , "count" : "Count"} , text="count" , title="Top 10 Mandate Creation Error Codes")
    man_cre_fig.update_layout(xaxis_title='Error Code', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(man_cre_fig)

with cols[0]:
    lite_fig = px.bar(lite_error , x="error" , y="count" , labels={"error" : "Error Codes" , "count" : "Count"} , text="count" , title="Top 10 UPI LITE Error Codes")
    lite_fig.update_layout(xaxis_title='Error Code', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(lite_fig)

with cols[1]:
    cc_fig = px.bar(cc_error , x="error" , y="count" , labels={"error" : "Error Codes" , "count" : "Count"} , text="count" , title="Top 10 Credit Card Error Codes")
    cc_fig.update_layout(xaxis_title='Error Code', yaxis_title='Count', title_x=0.5)
    st.plotly_chart(cc_fig)

all_error_data = pd.concat([txn_error , ref_error , man_error , man_cre_error , lite_error , cc_error])
error_codes_df = all_error_data[['error']]
error_codes_df = error_codes_df.drop_duplicates()
error_codes_df = error_codes_df.rename(columns={'error' : 'Error Code'})

# npic_error_data = get_npci_error_data_from_excel()


error_code_description = pd.merge(error_codes_df[['Error Code']] , npci_data[['Error Code' , 'Description']] , on='Error Code' , how="left")
with st.expander("Error Codes Description"):
    st.dataframe(error_code_description)