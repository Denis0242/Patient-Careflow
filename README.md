# Patient CareFlow & Outcomes Dashboard

## Executive Summary

This project analyzes patient journey completion, retention, treatment success, and cost patterns to help healthcare product and operations teams improve care-flow outcomes.

The dashboard evaluates patient funnel progression, D1/D7/D30 retention, completion rate, outcome success rate, visit type performance, condition-level outcomes, and cost exposure to identify where patients drop off and which groups need follow-up support.

Insights from this analysis support decisions around follow-up interventions, telehealth/hybrid care optimization, patient acquisition quality, and care-completion improvement.

Expected business impact includes improving treatment completion, increasing long-term retention, reducing avoidable drop-off, and focusing operational support on higher-risk patients.

Built using **Tableau, SQL, Python, and Streamlit**.

---

## Business Problem

Healthcare teams need a clear way to understand where patients lose engagement across the care journey and how retention, cost, and outcome success vary across patient segments.

This project answers:

- Where are patients dropping off in the care journey?
- Which retention window has the biggest decline?
- Which conditions and visit types show stronger outcome success?
- How should leadership prioritize follow-up and completion support?

---

## KPI Goals

| KPI | Value | Business Purpose |
|---|---:|---|
| Total Patients | 900 | Measures patient population analyzed |
| D1 Retention | 63.33% | Measures immediate patient engagement |
| D7 Retention | 40.11% | Measures short-term care continuity |
| D30 Retention | 23.44% | Measures long-term patient retention |
| Completion Rate | 27.00% | Measures treatment journey completion |
| Outcome Success Rate | 25.11% | Measures successful patient outcome rate |
| Avg Cost per Patient | $77.28 | Measures care-cost exposure per patient |

---

## Dataset Overview

| Item | Detail |
|---|---|
| Dataset | `careflow_dataset.csv` |
| Rows | 2,619 |
| Columns | 21 |
| Date Range | 2025-01-01 to 2025-05-12 |
| Grain | Patient journey event level |
| Key Fields | Patient ID, Event, Funnel Stage, Journey Date, Condition, Visit Type, Region, Retention Flags, Outcome Success, Treatment Cost |

---

## Dashboard Preview

### Main Dashboard

![Patient CareFlow Dashboard](screenshots/dashboard_preview.png)

### KPI Overview

![KPI Overview](screenshots/kpi_overview.png)

### Journey Funnel

![Journey Funnel](screenshots/journey_funnel.png)

### Retention Cohort

![Retention Cohort](screenshots/retention_cohort.png)

---

## Product Insights

### Insight

Patient drop-off is highest between consultation and D30 retention, showing that long-term care continuity is the biggest challenge after the initial treatment journey begins.

### Action

Monitor high-risk patients, low-retention cohorts, and journey stages with the largest conversion loss so care teams can intervene before disengagement increases.

### Recommendation

Implement targeted follow-up interventions such as reminders, telehealth support, care-navigation messages, and prioritization workflows for high-risk patients.

### Decision

Prioritize improving treatment completion and D30 retention before scaling patient acquisition efforts.

---

## SQL Transformations

The repo includes 4 representative SQL queries in [`sql/careflow_analysis.sql`](sql/careflow_analysis.sql):

1. KPI summary
2. Funnel drop-off analysis
3. Retention by cohort
4. Outcome success by condition and visit type

### Representative SQL Queries

#### Patient Retention KPI

```sql
SELECT
    ROUND(AVG(d30_retained)*100,2) AS d30_retention_rate
FROM careflow_clean;
```

#### Funnel Drop-off

```sql
SELECT
    funnel_stage,
    COUNT(patient_id) AS patients
FROM careflow_clean
GROUP BY funnel_stage
ORDER BY patients DESC;
```

---

## Metrics Engineering

```text
D1 Retention Rate = D1 Retained Patients / Total Patients
D7 Retention Rate = D7 Retained Patients / Total Patients
D30 Retention Rate = D30 Retained Patients / Total Patients
Completion Rate = Treatment Completed Patients / Total Patients
Outcome Success Rate = Successful Outcome Patients / Total Patients
Avg Cost per Patient = Total Treatment Cost / Total Patients
Stage Drop-off = Previous Stage Patients - Current Stage Patients
Stage Conversion Rate = Current Stage Patients / Previous Stage Patients
```

---

## Analytics Workflow

```text
Business Problem
        ↓
EDA + Cleaning
        ↓
Feature Engineering
        ↓
SQL Transformations
        ↓
Metrics Engineering
        ↓
Dashboard Build
        ↓
Insights
        ↓
Decision Support
        ↓
Business Impact
```

---

## Streamlit App

Interactive healthcare analytics application including:

- KPI monitoring
- Funnel drop-off analysis
- D1/D7/D30 retention tracking
- Patient segmentation
- Cost & outcome monitoring
- Executive decision framework

Launch locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

The Streamlit app recreates the dashboard story with KPI cards, funnel analysis, retention visuals, cost/outcome analysis, condition performance, visit type outcomes, and an executive decision summary.

---

## Business Impact

This dashboard can help healthcare and product teams to:

- Improve treatment completion by **5–8%**
- Increase D30 retention by **3–6 percentage points**
- Reduce avoidable patient drop-off by **10–15%**
- Improve telehealth utilization efficiency
- Enable earlier intervention for high-risk cohorts

---

## Experimentation Thinking

Potential A/B tests:

- Reminder frequency optimization
- Telehealth vs in-person follow-up
- Personalized care navigation messaging
- High-risk patient intervention timing
---

## Repo Architecture

```text
Patient-CareFlow-Outcomes-Dashboard/
├── app/
│   └── streamlit_app.py
├── dashboard/
│   └── README.md
├── data/
│   ├── careflow_dataset.csv
│   ├── careflow_clean.csv
│   └── raw_careflow_dataset.csv
├── docs/
│   ├── data_dictionary.md
│   └── executive_summary.md
├── notebooks/
│   └── eda_cleaning_feature_engineering.ipynb
├── screenshots/
│   ├── dashboard_preview.png
│   ├── kpi_overview.png
│   ├── journey_funnel.png
│   ├── retention_cohort.png
│   └── executive_decision_summary.png
├── sql/
│   └── careflow_analysis.sql
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Future Improvements

- Add predictive modeling for patients at risk of non-completion.
- Add A/B testing for follow-up interventions.
- Connect the dashboard to a live warehouse such as Snowflake or Redshift.
- Add scheduled data refresh using Python, Prefect, or scheduled SQL jobs.
