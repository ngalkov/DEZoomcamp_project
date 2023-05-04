{{ config(materialized='view') }}

with new_prices as (
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
FROM uk_property.update
WHERE uk_property.update.id not in (
    SELECT uk_property.historical_prices.id
    FROM uk_property.historical_prices
    )
)

select *
from new_prices