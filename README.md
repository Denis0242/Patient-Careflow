# Patient CareFlow & Outcomes Dashboard

![Dashboard Preview](screenshots/careflow_dashboard.png)

## Executive Summary

This project is a healthcare product analytics dashboard that analyzes the digital patient journey from portal opening through treatment completion and outcomes. It combines funnel analysis, cohort retention, cost-to-outcome monitoring, treatment success segmentation, and decision-support recommendations into one portfolio-ready analytics system.

**Positioning:** Data Analyst (Healthcare & Tech) with Product Data Analytics skills.

## Business Problem

Healthcare teams need to understand where patients drop off in the digital care journey, how retention changes over time, and whether treatment completion is connected to better outcomes. Without a structured analytics workflow, leadership may over-invest in acquisition while missing operational barriers that reduce completion and long-term patient retention.

## KPI Goals

| KPI | Value | Why It Matters |
|---|---:|---|
| Total Patients | 900 | Measures patient population covered in the analysis |
| D1 Retention | 63.33% | Measures early follow-up engagement |
| D7 Retention | 40.11% | Measures short-term care continuity |
| D30 Retention | 23.44% | Measures long-term retention and care adherence |
| Completion Rate | 27.00% | Measures treatment journey completion |
| Outcome Success Rate | 25.11% | Measures patient outcome effectiveness |
| Avg Cost per Patient | $77.28 | Measures cost efficiency across care journeys |

## Dataset

The dataset contains patient-level journey events and healthcare engagement attributes including demographics, condition, visit type, region, risk category, retention flags, treatment completion, outcome success, engagement score, and treatment cost.

## SQL Transformations

SQL files in `/sql` cover:

- Funnel stage progression
- Retention cohort analysis
- Outcome success by condition
- Visit type performance
- Cost vs outcome analysis
- Risk and regional segmentation

## Metrics Engineering

Core metrics were engineered from event-level journey data:

- Patient count = distinct patient IDs
- Stage conversion = patients reaching each funnel stage / prior stage
- Drop-off = prior stage patients - current stage patients
- Retention = retained patients / total eligible patients
- Completion rate = patients with treatment completed / total patients
- Outcome success rate = successful outcomes / total patients
- Cost per patient = total treatment cost / patient count

## Analytics Workflow

1. Load healthcare journey dataset
2. Clean and validate patient event records
3. Build SQL-based KPI and segmentation outputs
4. Create Tableau dashboard for executive monitoring
5. Translate dashboard patterns into product insights
6. Produce recommendations and decisions for care operations
7. Package project into a reusable analytics repository

## Dashboard Preview

The dashboard includes KPI cards, patient journey funnel, stage conversion loss, retention by cohort, cost vs outcome analysis, outcome success by condition, visit type performance, and an Insight → Action → Recommendation → Decision panel.

![CareFlow Dashboard](screenshots/careflow_dashboard.png)

## Product Insights

- Patient drop-off is highest between consultation and treatment completion, showing a major barrier in the later care journey.
- D30 retention is significantly lower than D1 and D7 retention, suggesting that short-term engagement does not consistently translate into long-term care continuity.
- Hybrid and telehealth visits show different outcome patterns, making visit type an important segmentation dimension for operational decisions.
- Cost and outcome should be monitored together because high spend does not always guarantee stronger treatment success.

## Experimentation Thinking

A practical experiment could test whether targeted follow-up reminders improve treatment completion and D30 retention.

**Hypothesis:** Patients receiving automated follow-up reminders will have higher treatment completion and D30 retention than patients receiving standard communication.

**Primary metric:** Treatment completion rate  
**Secondary metric:** D30 retention  
**Guardrail metric:** Average treatment cost per patient  
**Decision rule:** Scale the intervention if completion and D30 retention improve without materially increasing cost per patient.

## Recommendations

- Prioritize follow-up interventions for high-risk patients and patients who reach consultation but do not complete treatment.
- Build operational alerts for patients who show early engagement but fail to return by D7 or D30.
- Segment outreach strategies by condition, visit type, region, and risk category.
- Track completion and retention together before increasing patient acquisition spend.

## Decision Framework

| Decision Area | Recommendation | Rationale |
|---|---|---|
| Patient Retention | Improve D30 follow-up workflow | Long-term retention is the weakest engagement signal |
| Funnel Optimization | Focus on consultation-to-treatment drop-off | This is the highest-friction part of the journey |
| Care Operations | Segment by risk and condition | High-risk patients need more targeted intervention |
| Growth Strategy | Fix completion before scaling acquisition | More acquisition will not help if patients fail to complete care |

## Business Impact

This project demonstrates how healthcare analytics can convert raw journey data into operational decisions. The dashboard can help leaders reduce care drop-off, improve follow-up strategy, identify weak retention cohorts, and prioritize interventions that improve patient outcomes.

## Streamlit App

A Streamlit version is included in `/app/streamlit_app.py` for interactive portfolio presentation.

Run locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Repo Architecture

```text
patient-careflow-outcomes-dashboard/
│
├── data/
│   └── careflow_dataset.csv
│
├── sql/
│   ├── careflow_analysis.sql
│   ├── funnel_analysis.sql
│   ├── retention_cohort_analysis.sql
│   └── outcome_cost_analysis.sql
│
├── notebooks/
│   ├── eda.ipynb
│   ├── business_insights.ipynb
│   └── kpi_analysis.ipynb
│
├── dashboard/
│   └── tableau_dashboard_preview.png
│
├── screenshots/
│   └── careflow_dashboard.png
│
├── app/
│   ├── streamlit_app.py
│   ├── components.py
│   └── utils.py
│
├── docs/
│   ├── business_case.md
│   ├── dashboard_guide.md
│   └── kpi_definitions.md
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Automation Awareness

This repo is designed so the same analysis can later be automated using scheduled SQL jobs, Python scripts, or Prefect workflows. The most practical next automation step is a Python-based refresh script that updates KPIs and exports clean data for Tableau or Streamlit.

## Future Improvements

- Add statistical testing for reminder interventions
- Add cohort-level survival analysis
- Add patient risk scoring model
- Add automated KPI refresh pipeline
- Deploy Streamlit app to Streamlit Cloud
