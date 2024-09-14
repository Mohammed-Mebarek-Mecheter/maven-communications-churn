-- models/intermediate/int_customer_lifetime_value.sql
WITH "customer_revenue" AS (
    SELECT
        "customerid",
        "tenure_in_months",
        "monthly_charge",
        "total_revenue",
        "total_revenue" / NULLIF("tenure_in_months", 0) AS average_monthly_revenue
    FROM {{ ref('stg_telecom_customer_churn') }}
)

SELECT
    "customerid",
    "tenure_in_months",
    "monthly_charge",
    "total_revenue",
    average_monthly_revenue,
    average_monthly_revenue * 12 * 5 AS estimated_5_year_clv
FROM "customer_revenue"