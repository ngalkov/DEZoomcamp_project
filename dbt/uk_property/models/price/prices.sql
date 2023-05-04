{{ config(materialized='table') }}


with unchanged_data as (
    select *
    from {{ ref('unchanged_prices') }}
), 

new_data as (
    select *
    from {{ ref('new_prices') }}
)

select * from unchanged_data
union all
select * from new_data
