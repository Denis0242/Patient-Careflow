-- Patient Journey Funnel Analysis
SELECT
  "Funnel Stage",
  "Funnel Stage Order",
  COUNT(DISTINCT "Patient ID") AS patients_at_stage
FROM careflow_dataset
GROUP BY "Funnel Stage", "Funnel Stage Order"
ORDER BY "Funnel Stage Order";
