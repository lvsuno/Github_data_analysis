{{ config(
    materialized = 'incremental',
) }}

WITH org_data AS (
    SELECT org.id AS org_id, 
        org.login AS org_login, 
        created_at 
    FROM {{ ref('stg_april_github_archive') }}
        
    WHERE org.id IS NOT NULL

    {% if is_incremental() %}
      AND DATE_TRUNC(created_at, DAY) > 
      (
        SELECT MAX(day)
        FROM {{ this }}
      )
    {% endif %}    

)
SELECT DATE_TRUNC(created_at, DAY) as day,
    org_id, 
    org_login, 
    COUNT(1) AS nb_of_events
FROM org_data
GROUP BY 1,2,3
ORDER BY nb_of_events DESC