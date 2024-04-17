{{ 
    config(
        materialized='incremental'
    )     
}}


SELECT DATE_TRUNC(created_at, DAY) AS day,
    type, 
    COUNT(1) AS nb_of_events
FROM {{ ref('stg_april_github_archive') }}
GROUP BY 1, 2