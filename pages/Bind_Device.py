import streamlit as st
import pandas as pd
from connection import get_connection
import plotly.express as px

from sidebar import create_sidebar

st.set_page_config(layout="wide")

create_sidebar()

# Create a connection object.
conn = get_connection()
df = conn.read(worksheet="BindDevice")
df.dropna(how='all' , inplace=True)

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y' , errors='coerce')
cols_to_convert = [col for col in df.columns if col not in ['Bank', 'Date']]

st.title("Bind Device Analytics")

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
filtered_df['InboundSr'] = round((filtered_df['verifiedBeforeExpiry'] * 100 ) / filtered_df['Total'] , 2)
filtered_df['BoundSr']  = round(( filtered_df['BoundCount'] * 100 ) / filtered_df['Total'],2)
filtered_df['ActivatedSr'] = round((filtered_df['activatedCount'] * 100) / filtered_df['Total'],2)

filtered_df = filtered_df.sort_values(by='Date')

st.markdown("######")

cols = st.columns(4)
    # KPI Boxes 
with cols[0]:
    st.metric(label="Avg Inbound SR" , value=f"{round(filtered_df['InboundSr'].mean() , 1)} %")

with cols[1]:
    st.metric(label="Avg Bound SR" , value=f"{round(filtered_df['BoundSr'].mean() , 1)} %")

with cols[2]:
    st.metric(label="Avg Activated SR" , value=f"{round(filtered_df['ActivatedSr'].mean() , 1)} %")

st.markdown("---")

sr_melted = filtered_df.melt(id_vars=["Date"], value_vars=["InboundSr" , "BoundSr" , "ActivatedSr"],
                            var_name="SR", value_name="Percentage")
    
sr_fig = px.line(sr_melted, x="Date", y="Percentage", color="SR",
        labels={"Percentage": "Percentage (%)", "Date": "Date"} ,text=["{:.1f}".format(value) for value in sr_melted["Percentage"]] , markers=True , title=f"{selected_bank} Bind Device SR" )

# Customize the y-axis to have intervals of 5
sr_fig.update_yaxes(tick0=0, dtick=5)


# Add data labels to the points
sr_fig.update_traces(textposition="bottom center")

sr_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))

st.plotly_chart(sr_fig)

# verses_df = df.query('Date >= @start_date and Date <= @end_date')
# verses_df['InboundSr'] = round((verses_df['verifiedBeforeExpiry'] * 100 ) / verses_df['Total'] , 2)
# verses_df['BoundSr']  = round(( verses_df['BoundCount'] * 100 ) / verses_df['Total'],2)
# verses_df['ActivatedSr'] = round((verses_df['activatedCount'] * 100) / verses_df['Total'],2)

# color_palet = ["#115f9a", "#1984c5", "#22a7f0", "#48b5c4", "#76c68f", "#a6d75b", "#b3d4ff", "#8bd3c7", "#00b7c7"]

# isr_fig = px.bar(verses_df, x="Date", y="InboundSr", color="Bank", barmode="group",
#              title="APL VS YAPL VS RAPL ( InBound SR %)",
#              labels={"Date": "Date", "InboundSr": "InboundSr", "Bank": "Bank Type"},
#              text='InboundSr',
#              color_discrete_sequence=color_palet
#              )
# isr_fig.update_layout(
#     xaxis_title="Date",
#     yaxis_title="InboundSr",
#     legend_title="Bank",
#     title={
#         'text': "APL VS YAPL VS RAPL ( InBound SR %)",
#         'y':0.9,
#         'x':0.5,
#         'xanchor': 'center',
#         'yanchor': 'top'}
# )

# st.plotly_chart(isr_fig)

# # bsr_fig = px.bar(verses_df, x="Date", y="BoundSr", color="Bank", barmode="group",
# #              title="APL VS YAPL VS RAPL ( BoundSr SR %)",
# #              labels={"Date": "Date", "BoundSr": "BoundSr", "Bank": "Bank Type"},
# #              text='BoundSr',
# #              color_discrete_sequence=color_palet[3:]
# #              )
# # bsr_fig.update_layout(
# #     xaxis_title="Date",
# #     yaxis_title="BoundSr",
# #     legend_title="Bank",
# #     title={
# #         'text': "APL VS YAPL VS RAPL ( BoundSr SR %)",
# #         'y':0.9,
# #         'x':0.5,
# #         'xanchor': 'center',
# #         'yanchor': 'top'}
# # )

# # st.plotly_chart(bsr_fig)

# asr_fig = px.bar(verses_df, x="Date", y="ActivatedSr", color="Bank", barmode="group",
#              title="APL VS YAPL VS RAPL ( ActivatedSr SR %)",
#              labels={"Date": "Date", "ActivatedSr": "ActivatedSr", "Bank": "Bank Type"},
#              text='ActivatedSr',
#              color_discrete_sequence=color_palet[6:]
#              )
# asr_fig.update_layout(
#     xaxis_title="Date",
#     yaxis_title="ActivatedSr",
#     legend_title="Bank",
#     title={
#         'text': "APL VS YAPL VS RAPL ( ActivatedSr SR %)",
#         'y':0.9,
#         'x':0.5,
#         'xanchor': 'center',
#         'yanchor': 'top'}
# )

# st.plotly_chart(asr_fig)