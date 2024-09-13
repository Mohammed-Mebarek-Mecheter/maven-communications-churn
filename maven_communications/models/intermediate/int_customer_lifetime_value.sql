-- models/intermediate/int_customer_lifetime_value.sql
WITH "Customer_Revenue" AS (
    SELECT
        "CustomerID",
        "Tenure_in_Months",
        "Monthly_Charge",
        "Total_Revenue",
        "Total_Revenue" / NULLIF("Tenure_in_Months", 0) AS Average_Monthly_Revenue
    FROM {{ ref('stg_telecom_customer_churn') }}
)

SELECT
    "CustomerID",
    "Tenure_in_Months",
    "Monthly_Charge",
    "Total_Revenue",
    Average_Monthly_Revenue,
    Average_Monthly_Revenue * 12 * 5 AS Estimated_5_Year_CLV
FROM "Customer_Revenue"