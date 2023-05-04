{{ config(materialized='view') }}

with unchanged_prices as (
SELECT id,
    price ,
    date,
    postcode1,
    postcode2,
    type,
    is_new,
    duration,
    addr1,
    addr2,
    street,
    locality,
    town,
    district,
    county
FROM {{ source('uk_property', 'historical_prices') }}
WHERE {{ source('uk_property', 'historical_prices') }}.id not in (
    SELECT {{ source('uk_property', 'update') }}.id
    FROM {{ source('uk_property', 'update') }}
    )
)

select *
from unchanged_prices