-- models/churn_customers.sql

WITH Raw_Customers AS (
    SELECT
        CustomerID,
        Gender,
        Age,
        City,
        Tenure_in_Months,
        Monthly_Charge,
        Total_Revenue,
        Customer_Status,
        Churn_Category,
        Churn_Reason
    FROM public.telecom_customer_churn
)

SELECT
    *,
    CASE
        WHEN Churn_Category IS NOT NULL THEN 1
        ELSE 0
    END AS Churn_Risk
FROM Raw_Customers;
