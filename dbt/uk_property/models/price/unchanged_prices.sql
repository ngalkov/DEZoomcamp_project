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
FROM uk_property.historical_prices
WHERE uk_property.historical_prices.id not in (
    SELECT uk_property.update.id
    FROM uk_property.update
    )
)

select *
from unchanged_prices