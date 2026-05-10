-- Core Patient CareFlow KPI Analysis
SELECT
  COUNT(DISTINCT "Patient ID") AS total_patients,
  AVG("D1 Retained") * 100 AS d1_retention_rate,
  AVG("D7 Retained") * 100 AS d7_retention_rate,
  AVG("D30 Retained") * 100 AS d30_retention_rate,
  AVG("Treatment Completed") * 100 AS completion_rate,
  AVG("Outcome Success") * 100 AS outcome_success_rate,
  AVG("Treatment Cost") AS avg_event_cost
FROM careflow_dataset;
