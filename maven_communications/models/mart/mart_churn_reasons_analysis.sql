-- models/mart/mart_churn_reasons_analysis.sql
SELECT
    "churn_category",
    "churn_reason",
    COUNT(*) as churn_count,
    AVG("total_revenue") as Avg_Revenue_Lost
FROM {{ ref('stg_telecom_customer_churn') }}
WHERE "customer_status" = 'Churned'
GROUP BY "churn_category", "churn_reason"
ORDER BY churn_count DESC