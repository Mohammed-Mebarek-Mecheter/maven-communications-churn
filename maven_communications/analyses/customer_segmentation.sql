-- analyses/customer_segmentation.sql
WITH customer_segments AS (
    SELECT
        customerid,
        CASE
            WHEN estimated_5_year_clv >= 5000 THEN 'High Value'
            WHEN estimated_5_year_clv >= 2500 THEN 'Medium Value'
            ELSE 'Low Value'
        END as segment_count
    FROM {{ ref('int_customer_lifetime_value') }}
)
SELECT
    segment_count,
    COUNT(*) as segment_count,
    AVG(estimated_5_year_clv) as avg_clv
FROM customer_segments
GROUP BY segment_count