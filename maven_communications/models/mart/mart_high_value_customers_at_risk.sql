-- models/mart/mart_high_value_customers_at_risk.sql
WITH avg_clv AS (
    -- Calculate the average 5-year Customer Lifetime Value (CLV)
    SELECT AVG(estimated_5_year_clv) AS avg_lifetime_value
    FROM {{ ref('int_customer_lifetime_value') }}
),

     high_value_customers AS (
         -- Select customers whose 5-year CLV is above the average
         SELECT
             c."customerid",
             c."tenure_in_months",
             c."monthly_charge",
             c."total_revenue",
             clv.estimated_5_year_clv,
             rf.tenure_risk,
             rf.contract_risk,
             rf.refund_risk,
             CASE
                 WHEN c."customer_status" = 'Churned' THEN 1
                 ELSE 0
                 END AS is_churned
         FROM {{ ref('stg_telecom_customer_churn') }} c
                  JOIN {{ ref('int_customer_lifetime_value') }} clv
                       ON c."customerid" = clv."customerid"
                  JOIN {{ ref('int_churn_risk_factors') }} rf
                       ON c."customerid" = rf."customerid"
         WHERE clv.estimated_5_year_clv > (SELECT avg_lifetime_value FROM avg_clv)
     )

-- Final query to get high-value customers at churn risk
SELECT *
FROM high_value_customers
WHERE tenure_risk = 'High'
   OR contract_risk = 'High'
   OR refund_risk = 'High';
