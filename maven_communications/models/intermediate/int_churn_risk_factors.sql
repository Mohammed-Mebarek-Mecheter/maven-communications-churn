-- models/intermediate/int_churn_risk_factors.sql
SELECT
    "customerid",
    CASE
        WHEN "tenure_in_months" < 12 THEN 'High'
        WHEN "tenure_in_months" BETWEEN 12 AND 24 THEN 'Medium'
        ELSE 'Low'
    END as Tenure_Risk,
    CASE
        WHEN "contract" = 'Month-to-Month' THEN 'High'
        WHEN "contract" = 'One Year' THEN 'Medium'
        ELSE 'Low'
    END as Contract_Risk,
    CASE
        WHEN "total_revenue" > 0 THEN 'High'
        ELSE 'Low'
    END as Refund_Risk
FROM {{ ref('stg_telecom_customer_churn') }}