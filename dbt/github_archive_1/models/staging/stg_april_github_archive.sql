{{ 
    config(
        materialized='incremental',
        partition_by={
            "field": "created_at",
            "data_type":"timestamp",
            "granularity": "day"
        },
        cluster_by=["created_at", "type"]  
    )     
}}


with 

source as (

    select
        {{ dbt_utils.generate_surrogate_key(['id', 'created_at']) }} as event_id,
        id,
        type,
        actor,
        repo,
        payload,
        public,
        created_at,
        org,
        Row_number() over(partition by id, created_at) as rn

    from {{ source('staging', 'april_github_archive') }}
  
    {% if is_incremental() %}
    WHERE created_at > 
      (
        SELECT MAX(created_at)
        FROM {{ this }}
      )
    {% endif %}    

)

select         
    event_id,
    id,
    type,
    actor,
    repo,
    payload,
    public,
    created_at,
    org 
from source WHERE rn=1