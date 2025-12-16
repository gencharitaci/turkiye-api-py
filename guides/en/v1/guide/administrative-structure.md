---
outline: deep
---

# Administrative Structure

The following administrative figures are based on 2023 data retrieved from [biruni.tuik.gov.tr/medas](https://biruni.tuik.gov.tr/medas/). For the data source used in this project, [click here](./sources.md).

## Provinces

Provinces represent the highest level of administrative division in Türkiye. There are a total of 81 provinces in the country, and each province is subdivided into districts, amounting to 973 districts in total.

## Districts

Districts are the sub-units of provinces. Türkiye has 973 districts, each governed under a specific province. Every district consists of one or more neighborhoods. If the `isMetropolitan` field of the district's province is `true`, the district is considered part of a metropolitan municipality, and its `villages` field will be an empty array. If `false`, the district may contain villages.

::: info NOTE
Provincial centers of non-metropolitan provinces are also counted as districts and are included in this total.
:::

## Neighborhoods

Neighborhoods are sub-units of districts. There are 32,186 neighborhoods in Türkiye. Each neighborhood is administratively connected to a district center.

## Villages

Villages are also sub-units of districts. There are 18,171 villages in Türkiye, and they are governed under district centers.
