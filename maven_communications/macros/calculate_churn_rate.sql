-- macros/calculate_churn_rate.sql
{% macro calculate_churn_rate(churned_customers, total_customers) %}
    CAST({{ churned_customers }} AS FLOAT) / NULLIF({{ total_customers }}, 0) * 100
{% endmacro %}