-- models/customer_revenue_analysis.sql

WITH Customer_Revenue AS (
    SELECT
        CustomerID,
        Tenure_in_Months,
        Monthly_Charge,
        Total_Revenue,
        CASE
            WHEN Churn_Category IS NOT NULL THEN 'Churned'
            ELSE 'Active'
        END AS Customer_Status
    FROM public.telecom_customer_churn
)

SELECT
    Customer_Status,
    COUNT(CustomerID) AS num_customers,
    AVG(Total_Revenue) AS avg_revenue_per_customer,
    SUM(Total_Revenue) AS total_revenue_generated
FROM Customer_Revenue
GROUP BY Customer_Status;
