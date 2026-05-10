-- Outcome and Cost Segmentation
SELECT
  "Condition",
  "Visit Type",
  "Patient Risk Category",
  COUNT(DISTINCT "Patient ID") AS patients,
  AVG("Outcome Success") * 100 AS outcome_success_rate,
  AVG("Treatment Completed") * 100 AS completion_rate,
  AVG("Treatment Cost") AS avg_treatment_cost
FROM careflow_dataset
GROUP BY "Condition", "Visit Type", "Patient Risk Category"
ORDER BY outcome_success_rate DESC;
