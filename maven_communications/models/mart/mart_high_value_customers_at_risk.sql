-- models/mart/mart_high_value_customers_at_risk.sql
WITH avg_clv AS (
    SELECT AVG(Estimated_5_Year_CLV) as avg_lifetime_value
    FROM {{ ref('int_customer_lifetime_value') }}
)

SELECT
    c."CustomerID",
    c."Tenure_in_Months",
    c."Monthly_Charge",
    c."Total_Revenue",
    clv.Estimated_5_Year_CLV,
    rf.tenure_risk,
    rf.contract_risk,
    rf.refund_risk,
    CASE
        WHEN c."Customer_Status" = 'Churned' THEN 1
        ELSE 0
    END as Is_Churned
FROM {{ ref('stg_telecom_customer_churn') }} c
JOIN {{ ref('int_customer_lifetime_value') }} clv ON c."CustomerID" = clv."CustomerID"
JOIN {{ ref('int_churn_risk_factors') }} rf ON c."CustomerID" = rf."CustomerID"
CROSS JOIN avg_clv
WHERE clv.Estimated_5_Year_CLV > avg_clv.avg_lifetime_value
  AND (rf.tenure_risk = 'High' OR rf.contract_risk = 'High' OR rf.refund_risk = 'High')