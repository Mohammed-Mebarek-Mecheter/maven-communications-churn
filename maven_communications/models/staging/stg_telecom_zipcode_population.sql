-- models/staging/stg_telecom_zipcode_population.sql
SELECT
    "Zip_Code",
    "Population"
FROM {{ source('maven_communications', 'telecom_zipcode_population') }}
