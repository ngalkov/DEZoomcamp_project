{{ config(materialized='table') }}


select * from {{ ref('unchanged_prices') }}
union all
select * from {{ ref('new_prices') }}