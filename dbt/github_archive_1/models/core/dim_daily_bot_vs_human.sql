{{ 
    config(
        materialized='incremental'
    )     
}}


WITH human_bot AS(
    SELECT event_id, 
        type, 
        actor, 
        repo,
        payload,
        public, 
        created_at, 
        org,
-- returns Bot when any row for a event has 'Bot'
       MAX(CASE WHEN (actor.login LIKE '%bot%' or 
       actor.login LIKE '%Bot%' or 
       actor.login LIKE '%BOT%') THEN 'BOT' else 'HUMAN' end)
       OVER (PARTITION BY event_id) as bot_or_human
FROM {{ ref('stg_april_github_archive') }}
    {% if is_incremental() %}
    WHERE DATE_TRUNC(created_at, DAY) > 
      (
        SELECT MAX(day)
        FROM {{ this }}
      )
    {% endif %}    
)

SELECT DATE_TRUNC(created_at, DAY) AS day,
    type, 
    bot_or_human,
    COUNT(1) AS nb_of_events
FROM human_bot
GROUP BY 1, 2, 3