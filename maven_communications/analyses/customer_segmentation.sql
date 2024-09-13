-- analyses/customer_segmentation.sql
WITH customer_segments AS (
    SELECT
        CustomerID,
        CASE
            WHEN Estimated_5_Year_CLV >= 5000 THEN 'High Value'
            WHEN Estimated_5_Year_CLV >= 2500 THEN 'Medium Value'
            ELSE 'Low Value'
        END as Customer_Segment
    FROM {{ ref('int_customer_lifetime_value') }}
)
SELECT
    Customer_Segment,
    COUNT(*) as Segment_Count,
    AVG(Estimated_5_Year_CLV) as Avg_CLV
FROM customer_segments
GROUP BY Customer_Segment