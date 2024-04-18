{{ config(
    materialized = 'incremental',
) }}

WITH repos_activity AS (
    SELECT 
        repo.id AS repo_id,
        repo.name AS repo_name,
        created_at
    FROM {{ ref('stg_april_github_archive') }}
    WHERE type = 'ForkEvent'
    
    {% if is_incremental() %}
    AND DATE_TRUNC(created_at, DAY) > 
      (
        SELECT MAX(day)
        FROM {{ this }}
      )
    {% endif %}    
)
SELECT DATE_TRUNC(created_at, DAY) AS day,
    repo_id, 
    repo_name, 
    COUNT(1) AS nb_of_events
FROM repos_activity
GROUP BY 1, 2, 3
ORDER BY nb_of_events DESC