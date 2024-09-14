# Maven Communications Customer Retention Project

This project aims to help **Maven Communications**, a California-based telecommunications company, improve customer retention by identifying high-value customers at risk of churn. By leveraging **dbt (Data Build Tool)**, we’ve built a data pipeline that transforms raw customer and demographic data into actionable insights.

## **Project Objective**

The primary goals of this project are to:
- Identify **high-value customers** at risk of churning.
- Analyze the key **reasons for churn**.
- Provide insights that support the development of **customer retention strategies**.

To achieve this, we’ve implemented a series of dbt models that clean, transform, and analyze the data, focusing on **Customer Lifetime Value (CLV)** and **churn risk factors**.

---

## **Data Sources**

The project uses two primary data sources stored in **Supabase**:

1. **`telecom_customer_churn`**: This table contains detailed customer data, including demographics, services, and churn-related information.
2. **`telecom_zipcode_population`**: This table contains population estimates for the zip codes where customers reside.

---

## **dbt Models**

The dbt models have been structured in layers to ensure a clean, modular, and efficient data pipeline. Below is an overview of the models created:

### **1. Staging Models (`stg_`)**

Staging models are designed to clean and standardize raw data before further analysis. These views serve as a foundation for the intermediate and mart models.

#### **View: `stg_telecom_customer_churn`**
- **Description**: This staging view cleans and standardizes the raw customer data from `telecom_customer_churn`. It ensures data consistency, handles missing values, and prepares the data for deeper analysis.
- **Columns**: Matches the columns in the `telecom_customer_churn` table but with transformations applied.

#### **View: `stg_telecom_zipcode_population`**
- **Description**: This staging view cleans and standardizes zip code population data from `telecom_zipcode_population`. It ensures the population data is ready for analysis and can be easily joined with customer data.
- **Columns**: Matches the columns in the `telecom_zipcode_population` table.

### **2. Intermediate Models (`int_`)**

Intermediate models perform more complex transformations and calculations. These models serve as stepping stones for creating final business-facing models (marts).

#### **Table: `int_churn_risk_factors`**
- **Description**: This model calculates churn risk factors for each customer based on their tenure, contract type, and refund history. It assigns customers a `High`, `Medium`, or `Low` risk level for each factor.
- **Key Columns**:
    - `customerid`: Unique identifier for each customer.
    - `tenure_risk`: Churn risk based on the customer’s tenure.
    - `contract_risk`: Churn risk based on the customer’s contract type.
    - `refund_risk`: Churn risk based on refund history.

#### **Table: `int_customer_lifetime_value`**
- **Description**: This model calculates the **Customer Lifetime Value (CLV)** for each customer. The CLV is estimated over a 5-year period based on historical revenue and customer tenure.
- **Key Columns**:
    - `customerid`: Unique identifier for each customer.
    - `tenure_in_months`: The number of months the customer has been with the company.
    - `estimated_5_year_clv`: The estimated 5-year CLV for each customer.

### **3. Mart Models (`mart_`)**

Mart models are business-facing and designed to answer specific questions. They combine data from staging and intermediate models to provide actionable insights.

#### **Table: `mart_high_value_customers_at_risk`**
- **Description**: This mart identifies high-value customers who are at risk of churning. It combines the Customer Lifetime Value (CLV) with churn risk factors to highlight customers that should be prioritized for retention efforts.
- **Key Columns**:
    - `customerid`: Unique identifier for each customer.
    - `tenure_in_months`: The customer’s tenure with the company.
    - `estimated_5_year_clv`: The customer’s estimated lifetime value over 5 years.
    - `tenure_risk`: Churn risk based on tenure.
    - `contract_risk`: Churn risk based on contract type.
    - `refund_risk`: Churn risk based on refund history.
    - `is_churned`: Flag indicating if the customer has churned.

#### **Table: `mart_churn_reasons_analysis`**
- **Description**: This model provides a breakdown of customer churn reasons and their impact on revenue. It helps identify which churn reasons are most prevalent and costly.
- **Key Columns**:
    - `churn_category`: The high-level category of churn reason (e.g., Price, Competitor, Dissatisfaction).
    - `churn_reason`: The specific reason for churn provided by the customer.
    - `churn_count`: The number of customers who churned for each reason.
    - `avg_revenue_lost`: The average revenue lost for each churn reason.

---

## **Project Structure**

The dbt models are organized into the following directories to maintain clarity and modularity:

```bash
maven_communications/
├── models/
│   ├── staging/
│   │   ├── stg_telecom_customer_churn.sql
│   │   ├── stg_telecom_zipcode_population.sql
│   │   └── schema.yml
│   ├── intermediate/
│   │   ├── int_churn_risk_factors.sql
│   │   ├── int_customer_lifetime_value.sql
│   │   └── schema.yml
│   └── mart/
│       ├── mart_high_value_customers_at_risk.sql
│       ├── mart_churn_reasons_analysis.sql
│       └── schema.yml
├── tests/                 # Contains custom tests
├── macros/                # Contains custom macros (if needed)
└── dbt_project.yml        # Project configuration file
```

- **Staging models** are in the `models/staging/` directory.
- **Intermediate models** are in the `models/intermediate/` directory.
- **Mart models** (business-facing) are in the `models/mart/` directory.
- **Custom tests** and **macros** are placed in separate directories for better modularity.

---

## **dbt Testing**

We have implemented a set of **generic and custom tests** to ensure the quality of our data models. Some of the key tests include:
- **Unique and Not Null Tests**: Ensures that critical fields like `customerid` are unique and not null.
- **Accepted Values Tests**: Verifies that fields like `contract_risk` and `tenure_risk` have valid values (`High`, `Medium`, or `Low`).
- **Custom SQL Tests**: Checks if calculated values such as `Total_Revenue` match their expected components (charges minus refunds).

## **Conclusion**

This project provides a comprehensive approach to **customer retention** by identifying high-value customers at risk of churn and understanding the reasons behind churn. By using dbt, we have built a robust, scalable, and modular data pipeline that transforms raw data into actionable insights. This will allow Maven Communications to implement targeted retention strategies and ultimately reduce customer churn.

--- 
