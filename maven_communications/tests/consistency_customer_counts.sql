-- tests/consistency_customer_counts.sql
WITH stg_count AS (
    SELECT COUNT(DISTINCT "CustomerID") AS count
FROM {{ ref('stg_telecom_customer_churn') }}
    ),
    mart_count AS (
SELECT COUNT(DISTINCT "CustomerID") AS count
FROM {{ ref('mart_high_value_customers_at_risk') }}
    )
SELECT *
FROM stg_count, mart_count
WHERE stg_count.count != mart_count.count
