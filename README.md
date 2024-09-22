# Maven Communications: Customer Retention Dashboard & Data Pipeline

## Overview

The **Maven Communications Customer Retention Project** is a data-driven solution designed to help **Maven Communications**, a California-based telecommunications company, reduce customer churn and improve retention strategies. By leveraging **modern data tools**, the project transforms raw customer data into valuable insights presented in an intuitive **Streamlit dashboard**.

Key components of this solution include:
- A **real-time Streamlit dashboard** to visualize customer metrics, churn risks, high-value customers at risk, and actionable retention strategies.
- A powerful **dbt (Data Build Tool)** pipeline that processes, cleans, and transforms raw data into analytical outputs.
- Plans for **Dagster** orchestration to automate the data pipeline, ensuring data freshness for the dashboard.

---

## Project Components

### 1. **Streamlit Dashboard**

The **Streamlit dashboard** offers a user-friendly, interactive interface that provides actionable insights into customer behavior, churn risks, and segmentation. This dashboard is built for **Maven Communications' marketing, sales, and support teams** to monitor critical metrics and make informed decisions.

#### Key Pages:
- **Overview Page**: Offers a high-level summary of customer churn, segmentation trends, and KPIs.
- **Churn Analysis**: Analyzes customer churn reasons, including the financial impact of churn on the company.
- **High-Value Customers at Risk**: Identifies customers with the highest revenue potential who are at risk of leaving.
- **Customer Segmentation**: Segments customers by risk level, contract type, internet service, and geographical location.
- **Retention Strategies**: Provides actionable recommendations to retain customers who are at risk of churning.

You can find the dashboard on [huggingface space](https://huggingface.co/spaces/Mebarek/maven-communications-churn).
![maven-communications-churn.png](customer_retention_dashboard%2Fmaven-communications-churn.png)
### 2. **dbt (Data Build Tool)**

**dbt** powers the data transformation pipeline, turning raw data from **Supabase** into clean, reliable datasets that feed into the Streamlit dashboard. The dbt pipeline processes key metrics such as **Customer Lifetime Value (CLV)**, **churn risk factors**, and **revenue at risk** to help the business understand customer behavior better.

#### Key dbt Models:
- **Staging Models (`stg_`)**: Standardize and clean raw data.
- **Intermediate Models (`int_`)**: Perform advanced calculations like churn risk and CLV.
- **Mart Models (`mart_`)**: Provide business-facing data models used in the dashboard, such as high-value customers at risk and churn reasons.

### 3. **Dagster (Data Orchestration)**

**Dagster** is integrated to automate and monitor the data pipeline. By orchestrating the dbt models, it ensures data is consistently refreshed and available for real-time analysis in the Streamlit dashboard.

#### Key Features:
- **Automated dbt Runs**: Dagster schedules and triggers dbt runs at set intervals (e.g., daily at 2 AM), ensuring fresh data.
- **Asset Materialization**: Dagster treats dbt models as assets and provides visibility into when each model was last materialized.
- **Pipeline Monitoring**: With built-in error handling and logging, Dagster ensures the data pipeline runs smoothly, and team members are alerted in case of issues.

### 4. **Supabase Integration**

**Supabase** acts as the primary database, storing customer information and demographic data, including key tables like `telecom_customer_churn` and `telecom_zipcode_population`. The **dbt models** retrieve data from Supabase, process it, and load the transformed data back for the **Streamlit dashboard**.

---

## Project Structure

The project structure is split into the **Streamlit dashboard**, the **dbt pipeline**, and the **Dagster orchestration** system. The following is the directory layout:

```
maven-communications-churn/
├── customer_retention_dashboard/
│   ├── app/                        # Streamlit app components
│   │   ├── overview.py              # Overview dashboard script
│   │   ├── churn_reasons.py         # Churn analysis page script
│   │   ├── high_value_risk.py       # High-value customer risk analysis
│   │   ├── retention_strategies.py  # Retention strategies page
│   │   ├── segmentation.py          # Customer segmentation page
│   ├── utils/                      # Utility scripts for data manipulation
│   │   ├── load_data.py            # Loads data from Supabase
│   │   ├── clean_data.py           # Cleans and preprocesses data
│   │   ├── transform_data.py       # Applies data transformations for analysis
├── dagster_ci/
│   ├── assets.py                   # Defines dbt models as Dagster assets
│   ├── definitions.py              # Entry point for Dagster jobs and schedules
│   ├── schedules.py                # Schedule configuration for dbt model execution
├── maven_communications/           # dbt project for data transformations
│   ├── models/                     # dbt models
│   │   ├── intermediate/           # Intermediate models (e.g., churn risk, CLV)
│   │   ├── mart/                   # Final models used in dashboards
│   │   ├── staging/                # Staging models for raw data
│   │   └── schema.yml              # Documentation for dbt models
├── requirements.txt                # Python dependencies
├── setup.sh                        # Setup script for initializing the environment
└── README.md                       # Project documentation
```

---

## How Everything Works Together

1. **Supabase**: Stores raw customer and demographic data.
2. **dbt Models**: Transforms raw data into actionable insights (e.g., churn risk, CLV) and loads the results back into Supabase.
3. **Dagster**: Automates and monitors the dbt pipeline, ensuring that the models are regularly updated based on the predefined schedule.
4. **Streamlit Dashboard**: Pulls the latest data from Supabase and presents it in an interactive, real-time dashboard that helps teams monitor churn, identify high-risk customers, and implement retention strategies.

---

## Conclusion

The **Maven Communications Customer Retention Dashboard** integrates **dbt**, **Dagster**, and **Streamlit** to deliver a real-time, data-driven solution for managing customer churn. By automating data processing and providing actionable insights, the project helps **Maven Communications** proactively identify and retain high-value customers, ultimately driving revenue growth.

This setup ensures seamless data flow, automated transformations, and a user-friendly dashboard to monitor and act on customer retention efforts.

--- 
