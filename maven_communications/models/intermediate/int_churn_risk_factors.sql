-- models/intermediate/int_churn_risk_factors.sql
SELECT
    "CustomerID",
    CASE
        WHEN "Tenure_in_Months" < 12 THEN 'High'
        WHEN "Tenure_in_Months" BETWEEN 12 AND 24 THEN 'Medium'
        ELSE 'Low'
    END as Tenure_Risk,
    CASE
        WHEN "Contract" = 'Month-to-Month' THEN 'High'
        WHEN "Contract" = 'One Year' THEN 'Medium'
        ELSE 'Low'
    END as Contract_Risk,
    CASE
        WHEN "Total_Refunds" > 0 THEN 'High'
        ELSE 'Low'
    END as Refund_Risk
FROM {{ ref('stg_telecom_customer_churn') }}