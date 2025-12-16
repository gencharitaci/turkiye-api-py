---
outline: deep
---

# Districts

Districts are the second-level administrative divisions in Türkiye, following provinces. Each province is divided into one or more districts. There are 973 districts in total across the country. By default, the API lists districts first by their parent province and then alphabetically by name.

The entry point for districts is: `/v1/districts`

## District Properties

Each district resource contains the following fields:

- `provinceId`: The ID of the province to which the district belongs
- `id`: The district's unique ID
- `province`: The name of the province the district belongs to
- `name`: The name of the district
- `population`: The population of the district
- `area`: The surface area of the district (in km²)
- `neighborhoods`: The neighborhoods within the district (available only via `GET /v1/districts/{id}`)
- `villages`: The villages within the district (available only via `GET /v1/districts/{id}`)

::: info NOTE
Neighborhoods and villages of a district are only returned when querying that district by its specific ID. For example, `GET /v1/districts/1757` returns the neighborhoods of the Aladağ district.
:::

::: info NOTE
For a district to have villages, its parent province must **not** be a metropolitan municipality (`isMetropolitan: false`). If the province is metropolitan, the `villages` field will be returned as an empty array `[]`.
:::

## Fetching Multiple Districts

To fetch all districts, simply use the root district endpoint:

```url
https://api.turkiyeapi.dev/v1/districts
```

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/districts
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/districts')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

If the request is successful, the API will return a response like this:

::: details Sample Response {open}

```json
{
  "status": "OK",
  "data": [
    {
      "provinceId": 1,
      "id": 1757,
      "province": "Adana",
      "name": "Aladağ",
      "population": 16954,
      "area": 1340
    },
    {
      "provinceId": 1,
      "id": 1219,
      "province": "Adana",
      "name": "Ceyhan",
      "population": 156610,
      "area": 1426
    },
    {
      "provinceId": 1,
      "id": 2033,
      "province": "Adana",
      "name": "Çukurova",
      "population": 374205,
      "area": 250
    },
    {
      "provinceId": 1,
      "id": 1329,
      "province": "Adana",
      "name": "Feke",
      "population": 17304,
      "area": 1218
    },
    {
      "provinceId": 1,
      "id": 1806,
      "province": "Adana",
      "name": "İmamoğlu",
      "population": 27341,
      "area": 445
    }
    // Other districts...
  ]
}
```

:::

## Fetching a Specific District

To fetch a single district, use the district ID in the endpoint:

```url
https://api.turkiyeapi.dev/v1/districts/{id}
```

Replace `{id}` with the ID of the district you want to retrieve.

```bash [curl]
curl https://api.turkiyeapi.dev/v1/districts/1757
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/districts/1757')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

If the request is successful, the API will return a response like the following:

::: details Sample Response {open}

```json
{
  "status": "OK",
  "data": {
    "provinceId": 1,
    "id": 1757,
    "province": "Adana",
    "name": "Aladağ",
    "population": 16954,
    "area": 1340,
    "neighborhoods": [
      {
        "id": 176887,
        "name": "Akören",
        "population": 980
      },
      {
        "id": 248,
        "name": "Akpınar",
        "population": 654
      },
      {
        "id": 249,
        "name": "Başpınar",
        "population": 848
      },
      {
        "id": 176889,
        "name": "Boztahta",
        "population": 258
      }
      // Other neighborhoods...
    ],
    "villages": []
  }
}
```

:::

## Query Parameters

The API offers several parameters to query district data. These parameters allow filtering, sorting, and selecting specific fields.

::: info NOTE
For more examples, see the Example API Calls page.
:::

For `/districts`:

| Query Parameter | Type   | Description                                                                             |
| --------------- | ------ | --------------------------------------------------------------------------------------- |
| name            | string | Returns all districts that contain or match the provided name string.                   |
| minPopulation   | number | Returns districts with a population greater than or equal to the given value.           |
| maxPopulation   | number | Returns districts with a population less than or equal to the given value.              |
| minArea         | number | Returns districts with an area greater than or equal to the given value.                |
| maxArea         | number | Returns districts with an area less than or equal to the given value.                   |
| provinceId      | number | Filters districts belonging to a specific province using the province's ID.             |
| province        | string | Filters districts belonging to a specific province using the province's name.           |
| offset          | number | Skips a number of records; e.g., `offset=10` starts from the 11th result.               |
| limit           | number | Limits the number of results returned; e.g., `limit=10` returns up to 10 records.       |
| fields          | string | Selects which fields to return; e.g., `fields=id,name` returns only ID and name fields. |
| sort            | string | Specifies the sorting criteria; e.g., `sort=name` sorts by district name.               |

For `/districts/{id}`:

| Path Variable | Description                     |
| ------------- | ------------------------------- |
| id            | The ID of the district to fetch |

| Query Parameter | Type   | Description                                                                                         |
| --------------- | ------ | --------------------------------------------------------------------------------------------------- |
| fields          | string | Selects which fields to return; e.g., `fields=id,name,population` returns ID, name, and population. |
