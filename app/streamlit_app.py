import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, patient_level

st.set_page_config(page_title="Patient CareFlow Dashboard", layout="wide")
st.title("Patient CareFlow & Outcomes Dashboard")
st.caption("Healthcare + Product Analytics portfolio project")

df = load_data()
pl = patient_level(df)

cols = st.columns(6)
cols[0].metric("Total Patients", f"{pl['Patient ID'].nunique():,}")
cols[1].metric("D1 Retention", f"{pl['D1 Retained'].mean()*100:.2f}%")
cols[2].metric("D7 Retention", f"{pl['D7 Retained'].mean()*100:.2f}%")
cols[3].metric("D30 Retention", f"{pl['D30 Retained'].mean()*100:.2f}%")
cols[4].metric("Completion Rate", f"{pl['Treatment Completed'].mean()*100:.2f}%")
cols[5].metric("Outcome Success", f"{pl['Outcome Success'].mean()*100:.2f}%")

st.divider()

funnel = df.groupby(["Funnel Stage", "Funnel Stage Order"])["Patient ID"].nunique().reset_index().sort_values("Funnel Stage Order")
fig = px.funnel(funnel, x="Patient ID", y="Funnel Stage", title="Patient Journey Funnel")
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    cond = df.groupby("Condition")["Outcome Success"].mean().reset_index()
    cond["Outcome Success"] *= 100
    st.plotly_chart(px.bar(cond, x="Condition", y="Outcome Success", title="Outcome Success by Condition"), use_container_width=True)
with right:
    visit = df.groupby("Visit Type")["Outcome Success"].mean().reset_index()
    visit["Outcome Success"] *= 100
    st.plotly_chart(px.pie(visit, names="Visit Type", values="Outcome Success", title="Outcome by Visit Type"), use_container_width=True)

st.subheader("Insight → Action → Recommendation → Decision")
st.markdown("""
**Insight:** Completion and long-term retention are the biggest performance gaps.  
**Action:** Investigate barriers after consultation and before treatment completion.  
**Recommendation:** Test targeted follow-up reminders for high-risk patients.  
**Decision:** Improve completion and D30 retention before scaling patient acquisition.
""")
