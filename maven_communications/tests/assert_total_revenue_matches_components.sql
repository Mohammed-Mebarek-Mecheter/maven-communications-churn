-- tests/assert_total_revenue_matches_components.sql
WITH calculated_revenue AS (
    SELECT
        CustomerID,
        Total_Revenue,
        (Total_Charges - Total_Refunds + Total_Extra_Data_Charges + Total_Long_Distance_Charges) AS calculated_total_revenue
    FROM {{ ref('stg_telecom_customer_churn') }}
)
SELECT *
FROM calculated_revenue
WHERE ABS(Total_Revenue - calculated_total_revenue) > 0.01;
