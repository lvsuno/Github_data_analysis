{{ 
    config(
        materialized='incremental'
    )     
}}


SELECT DATE_TRUNC(created_at, DAY) AS day,
    type, 
    COUNT(1) AS nb_of_events
FROM {{ ref('stg_april_github_archive') }} 
    {% if is_incremental() %}
    WHERE DATE_TRUNC(created_at, DAY) > 
      (
        SELECT MAX(day)
        FROM {{ this }}
      )
    {% endif %}    
GROUP BY 1, 2