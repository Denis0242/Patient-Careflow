-- Patient CareFlow & Outcomes Dashboard SQL Analysis
-- Dialect: PostgreSQL / Snowflake-style SQL

-- 1. KPI Summary
SELECT
    COUNT(DISTINCT patient_id) AS total_patients,
    AVG(d1_retained) * 100 AS d1_retention_rate,
    AVG(d7_retained) * 100 AS d7_retention_rate,
    AVG(d30_retained) * 100 AS d30_retention_rate,
    AVG(treatment_completed) * 100 AS completion_rate,
    AVG(outcome_success) * 100 AS outcome_success_rate,
    SUM(treatment_cost) / COUNT(DISTINCT patient_id) AS avg_cost_per_patient
FROM careflow_clean;

-- 2. Funnel Drop-off Analysis
WITH stage_counts AS (
    SELECT
        funnel_stage_order,
        funnel_stage,
        COUNT(DISTINCT patient_id) AS patients
    FROM careflow_clean
    GROUP BY 1, 2
), funnel AS (
    SELECT
        funnel_stage_order,
        funnel_stage,
        patients,
        LAG(patients) OVER (ORDER BY funnel_stage_order) AS previous_stage_patients
    FROM stage_counts
)
SELECT
    funnel_stage,
    patients,
    previous_stage_patients,
    previous_stage_patients - patients AS stage_dropoff,
    ROUND(patients * 100.0 / NULLIF(previous_stage_patients, 0), 2) AS stage_conversion_rate
FROM funnel
ORDER BY funnel_stage_order;

-- 3. Monthly Retention by Cohort
SELECT
    DATE_TRUNC('month', journey_date) AS cohort_month,
    AVG(d1_retained) * 100 AS d1_retention_rate,
    AVG(d7_retained) * 100 AS d7_retention_rate,
    AVG(d30_retained) * 100 AS d30_retention_rate
FROM careflow_clean
GROUP BY 1
ORDER BY 1;

-- 4. Outcome Success by Condition and Visit Type
SELECT
    condition,
    visit_type,
    COUNT(DISTINCT patient_id) AS total_patients,
    AVG(outcome_success) * 100 AS outcome_success_rate,
    AVG(treatment_completed) * 100 AS completion_rate,
    SUM(treatment_cost) / COUNT(DISTINCT patient_id) AS avg_cost_per_patient
FROM careflow_clean
GROUP BY 1, 2
ORDER BY outcome_success_rate DESC;
