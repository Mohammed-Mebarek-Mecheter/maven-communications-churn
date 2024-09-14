-- tests/assert_total_revenue_matches_components.sql
WITH Calculated_Revenue AS (
    SELECT
        "CustomerID",
        "Total_Revenue",
        ("Total_Charges" - "Total_Refunds" + "Total_Extra_Data_Charges" + "Total_Long_Distance_Charges") AS Calculated_Total_Revenue
    FROM {{ ref('stg_telecom_customer_churn') }}
)
SELECT *
FROM Calculated_Revenue
WHERE ABS("Total_Revenue" - Calculated_Total_Revenue) > 0.01
