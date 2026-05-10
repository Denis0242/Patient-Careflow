-- Monthly Retention Cohort Analysis
SELECT
  DATE_TRUNC('month', CAST("Journey Date" AS DATE)) AS cohort_month,
  AVG("D1 Retained") * 100 AS d1_retention,
  AVG("D7 Retained") * 100 AS d7_retention,
  AVG("D30 Retained") * 100 AS d30_retention
FROM careflow_dataset
GROUP BY 1
ORDER BY 1;
