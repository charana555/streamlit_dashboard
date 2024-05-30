import streamlit as st
import pandas as pd
import plotly.express as px

def stats_component(data , bank):
    total_p2p_pay_volume = data["P2P_Pay_Volume"]
    total_p2m_pay_volume = data["P2M_Pay_Volume"]
    total_p2p_collect_volume = data["P2P_COLLECT_Volume"]
    total_p2m_collect_volume = data["P2M_COLLECT_Volume"]
    total_p2p_pay_succvolume = data["P2P_Pay_Succvolume"]
    total_p2m_pay_succvolume = data["P2M_Pay_Succvolume"]
    total_p2p_collect_succvolume = data["P2P_Collect_Succvolume"]
    total_p2m_collect_succvolume = data["P2M_Collect_Succvolume"]
    filtered_date = data["Date"]

    

    st.markdown("######")
    cols = st.columns(5)
    # KPI Boxes 

    with cols[0]:
        total_volume = (total_p2p_pay_volume.sum() + total_p2p_collect_volume.sum() + total_p2m_pay_volume.sum() + total_p2m_collect_volume.sum()) if total_p2p_pay_volume.sum() + total_p2p_collect_volume.sum() + total_p2m_pay_volume.sum() + total_p2m_collect_volume.sum() != 0 else 0

        st.metric(label="Total Volume" , value=f"{round(total_volume /1000000 , 1)} M")

    with cols[1]:
        pay_sr = ((total_p2m_pay_succvolume.sum() + total_p2p_pay_succvolume.sum()) * 100) / (total_p2p_pay_volume.sum() + total_p2m_pay_volume.sum()) if total_p2p_pay_volume.sum() + total_p2m_pay_volume.sum() != 0 else 0
        st.metric(label="Pay SR %" , value=f"{round(pay_sr , 1)} %")
    with cols[2]:
        collect_sr = ((total_p2m_collect_succvolume.sum() + total_p2p_collect_succvolume.sum()) * 100) / (total_p2p_collect_volume.sum() + total_p2m_collect_volume.sum()) if total_p2p_collect_volume.sum() + total_p2m_collect_volume.sum() != 0 else 0
        st.metric(label="Collect SR %" , value=f"{round(collect_sr , 1)} %")

    st.markdown("---")

    # sr graph 
    sr_data = pd.DataFrame(
        {
            "Date": filtered_date,
            "P2P_Pay_SR": (total_p2p_pay_succvolume * 100) / total_p2p_pay_volume.where(total_p2p_pay_volume != 0, other=1),
            "P2M_Pay_SR": (total_p2m_pay_succvolume * 100) / total_p2m_pay_volume.where(total_p2m_pay_volume != 0, other=1),
            "P2P_Collect_SR": (total_p2p_collect_succvolume * 100) / total_p2p_collect_volume.where(total_p2p_collect_volume != 0, other=1),
            "P2M_Collect_SR": (total_p2m_collect_succvolume * 100) / total_p2m_collect_volume.where(total_p2m_collect_volume != 0, other=1),
        }
    )



    sr_melted = sr_data.melt(id_vars=["Date"], value_vars=["P2P_Pay_SR" , "P2M_Pay_SR" , "P2P_Collect_SR" , "P2M_Collect_SR"],
                            var_name="SR", value_name="Percentage")
    
    sr_fig = px.line(sr_melted, x="Date", y="Percentage", color="SR",
            labels={"Percentage": "Percentage (%)", "Date": "Date"} ,text=["{:.1f}".format(value) for value in sr_melted["Percentage"]] , markers=True , title=f"{bank} Success Rate" )

    # Customize the y-axis to have intervals of 5
    sr_fig.update_yaxes(tick0=0, dtick=5)


    # Add data labels to the points
    sr_fig.update_traces(textposition="bottom center")

    sr_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))

    st.plotly_chart(sr_fig)
    st.markdown("---")

    # volume graph 
    volume_data = pd.DataFrame(
        {
            "Date" : filtered_date,
            "P2P_Pay_Volume" : total_p2p_pay_volume,
            "P2M_Pay_Volume" : total_p2m_pay_volume,
            "P2P_Collect_Volume" : total_p2p_collect_volume,
            "P2M_Collect_Volume" : total_p2m_collect_volume,
        }
    )

    volume_melted = volume_data.melt(
        id_vars=["Date"],
        value_vars=["P2P_Pay_Volume" , "P2M_Pay_Volume" , "P2P_Collect_Volume" , "P2M_Collect_Volume"],
        var_name="Vol",
        value_name="Volume"

    )

    volume_fig = px.line(
        volume_melted,
        x="Date",
        y="Volume",
        color="Vol",
        labels={"Volume ": "Volume (M)" , "Date" : "Date"},
        text=["{:.1f} M".format(value/1000000) for value in volume_melted["Volume"]],
        markers=True,
        title=f"{bank} Volume"
    )

    volume_fig.update_yaxes(tick0=0, dtick=500000)

    volume_fig.update_traces(textposition="bottom center")

    volume_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))

    st.plotly_chart(volume_fig)
    st.markdown("---")

    # Succces volume graph 
    success_volume_data = pd.DataFrame(
        {
            "Date" : filtered_date,
            "P2P_Pay_Succvolume" : total_p2p_pay_succvolume,
            "P2M_Pay_Succvolume" : total_p2m_pay_succvolume,
            "P2P_Collect_Succvolume" : total_p2p_collect_succvolume,
            "P2M_Collect_Succvolume" : total_p2m_collect_succvolume,
        }
    )

    success_volume_melted = success_volume_data.melt(
        id_vars=["Date"],
        value_vars=["P2P_Pay_Succvolume" , "P2M_Pay_Succvolume" , "P2P_Collect_Succvolume" , "P2M_Collect_Succvolume"],
        var_name="SuccVol",
        value_name="SuccVolume"

    )

    success_volume_fig = px.line(
        success_volume_melted,
        x="Date",
        y="SuccVolume",
        color="SuccVol",
        labels={"SuccVolume ": "Volume (M)" , "Date" : "Date"},
        text=["{:.1f} M".format(value/1000000) for value in success_volume_melted["SuccVolume"]],
        markers=True,
        title=f"{bank} Success Volume"
    )

    success_volume_fig.update_yaxes(tick0=0, dtick=500000)

    success_volume_fig.update_traces(textposition="bottom center")

    success_volume_fig.update_layout(title_x=0.5 , legend=dict(orientation="h", yanchor="top", y=1.2, xanchor="right", x=1))

    st.plotly_chart(success_volume_fig)
