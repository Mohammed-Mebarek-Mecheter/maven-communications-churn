-- models/staging/stg_telecom_zipcode_population.sql
SELECT
    "zip_code",
    "population"
FROM {{ source('maven_communications', 'telecom_zipcode_population') }}
