{{ config(
    materialized = 'incremental',
) }}

WITH actor_data AS (
    SELECT actor.id AS actor_id, 
        actor.login AS actor_login, 
        created_at 
    FROM {{ ref('stg_april_github_archive') }}

    {% if is_incremental() %}
    WHERE DATE_TRUNC(created_at, DAY) > 
      (
        SELECT MAX(day)
        FROM {{ this }}
      )
    {% endif %}    

)
SELECT DATE_TRUNC(created_at, DAY) as day,
    actor_id, 
    actor_login, 
    COUNT(1) AS nb_of_events
FROM actor_data
GROUP BY 1,2,3
ORDER BY nb_of_events DESC