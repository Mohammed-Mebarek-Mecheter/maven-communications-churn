-- models/mart/mart_churn_reasons_analysis.sql
SELECT
    "Churn_Category",
    "Churn_Reason",
    COUNT(*) as Churn_Count,
    AVG("Total_Revenue") as Avg_Revenue_Lost
FROM {{ ref('stg_telecom_customer_churn') }}
WHERE "Customer_Status" = 'Churned'
GROUP BY "Churn_Category", "Churn_Reason"
ORDER BY Churn_Count DESC