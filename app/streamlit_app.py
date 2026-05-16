import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Patient CareFlow & Outcomes", layout="wide")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "careflow_dataset.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    df["journey_date"] = pd.to_datetime(df["journey_date"], errors="coerce")
    return df

df = load_data()

st.markdown("""
<style>
.block-container {padding-top: 1rem;}
.metric-card {
    background:#f7f2f7;
    border:1px solid #ead6e8;
    border-radius:16px;
    padding:18px;
    text-align:center;
    box-shadow:0 1px 4px rgba(0,0,0,.06);
}
.metric-label {font-size:15px; color:#3b6fb6; font-weight:600;}
.metric-value {font-size:28px; color:#222; font-weight:800; margin-top:8px;}
.summary-card {
    border-radius:16px;
    padding:18px;
    min-height:180px;
    box-shadow:0 1px 5px rgba(0,0,0,.08);
}
.insight {background:#e8f2ff; border-left:7px solid #3b82f6;}
.action {background:#fff7db; border-left:7px solid #f59e0b;}
.recommendation {background:#eaf8ee; border-left:7px solid #22c55e;}
.decision {background:#ffe9ef; border-left:7px solid #e11d48;}
</style>
""", unsafe_allow_html=True)

st.title("Patient CareFlow & Outcomes Dashboard")
st.caption("Healthcare journey analytics | Funnel, retention, outcome success, and cost decision support")

with st.sidebar:
    st.header("Filters")
    age = st.multiselect("Age Group", sorted(df["age_group"].dropna().unique()))
    condition = st.multiselect("Condition", sorted(df["condition"].dropna().unique()))
    risk = st.multiselect("Patient Risk", sorted(df["patient_risk_category"].dropna().unique()))
    region = st.multiselect("Region", sorted(df["region"].dropna().unique()))
    visit_type = st.multiselect("Visit Type", sorted(df["visit_type"].dropna().unique()))

filtered = df.copy()

for col, values in {
    "age_group": age,
    "condition": condition,
    "patient_risk_category": risk,
    "region": region,
    "visit_type": visit_type,
}.items():
    if values:
        filtered = filtered[filtered[col].isin(values)]

patient_level = filtered.groupby("patient_id", as_index=False).agg(
    d1_retained=("d1_retained", "max"),
    d7_retained=("d7_retained", "max"),
    d30_retained=("d30_retained", "max"),
    treatment_completed=("treatment_completed", "max"),
    outcome_success=("outcome_success", "max"),
    treatment_cost=("treatment_cost", "sum"),
    engagement_score=("engagement_score", "mean"),
)

def pct(x):
    return f"{x * 100:.1f}%" if len(patient_level) else "0.0%"

def money(x):
    return f"${x:,.0f}"

def clean_fig(fig, height=380, showlegend=False):
    fig.update_layout(
        height=height,
        showlegend=showlegend,
        margin=dict(l=10, r=10, t=15, b=25),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend_title_text="",
        font=dict(size=12)
    )
    fig.update_xaxes(showgrid=False, zeroline=False, title=None)
    fig.update_yaxes(showgrid=False, zeroline=False, title=None)
    return fig

metrics = [
    ("Total Patients", f"{patient_level['patient_id'].nunique():,.0f}"),
    ("D1 Retention", pct(patient_level["d1_retained"].mean())),
    ("D7 Retention", pct(patient_level["d7_retained"].mean())),
    ("D30 Retention", pct(patient_level["d30_retained"].mean())),
    ("Completion Rate", pct(patient_level["treatment_completed"].mean())),
    ("Outcome Success Rate", pct(patient_level["outcome_success"].mean())),
    ("Avg Cost per Patient", money(patient_level["treatment_cost"].mean() if len(patient_level) else 0)),
]

cols = st.columns(7)

for col, (label, value) in zip(cols, metrics):
    col.markdown(
        f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

left, mid, right = st.columns([1.1, 1.05, 1.25])

with left:
    st.subheader("Patient Journey Funnel")

    funnel = (
        filtered
        .groupby(["funnel_stage_order", "funnel_stage"], as_index=False)["patient_id"]
        .nunique()
        .sort_values("funnel_stage_order")
        .rename(columns={"patient_id": "patients"})
    )

    fig = px.funnel(
        funnel,
        y="funnel_stage",
        x="patients",
        text="patients"
    )

    fig.update_traces(
        textinfo="value",
        textposition="inside"
    )

    fig.update_yaxes(title=None)
    fig = clean_fig(fig, height=420, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

with mid:
    st.subheader("Stage Conversion Loss")

    stage = funnel.copy()
    stage["previous"] = stage["patients"].shift(1)
    stage["dropoff"] = stage["previous"] - stage["patients"]
    stage = stage.dropna()

    fig = px.bar(
        stage,
        y="funnel_stage",
        x="dropoff",
        orientation="h",
        text=stage["dropoff"].astype(int)
    )

    fig.update_traces(textposition="inside")
    fig = clean_fig(fig, height=420, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Retention by Cohort")

    cohort = filtered.copy()
    cohort["month"] = cohort["journey_date"].dt.strftime("%B")

    heat = cohort.groupby("month", as_index=False).agg(
        d1_retention=("d1_retained", "mean"),
        d7_retention=("d7_retained", "mean"),
        d30_retention=("d30_retained", "mean"),
    )

    heat = heat.set_index("month") * 100

    fig = px.imshow(
        heat,
        text_auto=".1f",
        aspect="auto",
        labels=dict(color="")
    )

    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=15, b=25)
    )

    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)

    st.plotly_chart(fig, use_container_width=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Cost vs Outcome")

    scatter = filtered.groupby("patient_id", as_index=False).agg(
        treatment_cost=("treatment_cost", "sum"),
        outcome_success=("outcome_success", "max"),
        engagement_score=("engagement_score", "mean"),
        patient_risk_category=("patient_risk_category", "first"),
    )

    scatter["outcome_label"] = scatter["outcome_success"].map({
        1: "Successful Outcome",
        0: "Unsuccessful Outcome"
    })

    fig = px.scatter(
        scatter,
        x="treatment_cost",
        y="engagement_score",
        color="outcome_label",
        size="engagement_score",
        hover_data=["patient_risk_category", "outcome_label"],
        size_max=24
    )

    fig.update_traces(
        marker=dict(
            opacity=0.65,
            line=dict(width=0.5, color="white")
        )
    )

    fig.update_xaxes(title="Cost")
    fig.update_yaxes(title="Engagement")
    fig = clean_fig(fig, height=410, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Outcome Success by Condition")

    cond = (
        filtered
        .groupby("condition", as_index=False)["outcome_success"]
        .mean()
        .sort_values("outcome_success", ascending=True)
    )

    cond["outcome_success"] *= 100

    fig = px.bar(
        cond,
        x="outcome_success",
        y="condition",
        orientation="h",
        text=cond["outcome_success"].map(lambda x: f"{x:.1f}%")
    )

    fig.update_traces(textposition="inside")
    fig.update_xaxes(ticksuffix="%")
    fig = clean_fig(fig, height=410, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

with c3:
    st.subheader("Outcome by Visit Type")

    visit = (
        filtered
        .groupby("visit_type", as_index=False)["outcome_success"]
        .mean()
        .sort_values("outcome_success", ascending=True)
    )

    visit["outcome_success"] *= 100

    fig = px.bar(
        visit,
        x="outcome_success",
        y="visit_type",
        orientation="h",
        text=visit["outcome_success"].map(lambda x: f"{x:.1f}%")
    )

    fig.update_traces(textposition="inside")
    fig.update_xaxes(ticksuffix="%")
    fig = clean_fig(fig, height=410, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Executive Decision Summary")

summary_cols = st.columns(4)

summary = [
    (
        "INSIGHT",
        "Patient drop-off is highest between consultation and D30 retention, making long-term retention the biggest care-flow risk.",
        "insight"
    ),
    (
        "ACTION",
        "Investigate barriers preventing patients from completing treatment and returning for follow-up care.",
        "action"
    ),
    (
        "RECOMMENDATION",
        "Implement targeted follow-up interventions such as reminders, telehealth support, and outreach for high-risk patients.",
        "recommendation"
    ),
    (
        "DECISION",
        "Prioritize improving treatment completion and D30 retention before scaling patient acquisition efforts.",
        "decision"
    ),
]

for col, (title, body, klass) in zip(summary_cols, summary):
    col.markdown(
        f"""
        <div class='summary-card {klass}'>
            <h4>{title}</h4>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True
    )