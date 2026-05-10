import streamlit as st

def metric_card(label, value):
    st.metric(label=label, value=value)
