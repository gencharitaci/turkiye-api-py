---
outline: deep
---

# Neighborhoods

Neighborhoods are administrative units that come after districts in Turkey's administrative divisions. Each district is divided into one or more neighborhoods. There are a total of 32,186 neighborhoods in Turkey. By default, the API lists all neighborhoods first by the provinces they belong to, then by the districts they belong to, and finally by their names.

The entry URL for neighborhoods is: `/v1/neighborhoods`.

## Neighborhood Properties

Neighborhood resources have the following properties:

- `provinceId`: The ID of the province the neighborhood belongs to
- `districtId`: The ID of the district the neighborhood belongs to
- `id`: The neighborhood's ID
- `province`: The name of the province the neighborhood belongs to
- `district`: The name of the district the neighborhood belongs to
- `name`: The neighborhood's name
- `population`: The neighborhood's population

## Getting Multiple Neighborhood Data

To get all neighborhoods, you only need to use the neighborhood URL. For example, you can use a URL like `/v1/neighborhoods` to get all neighborhoods.

```url
https://api.turkiyeapi.dev/v1/neighborhoods
```

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/neighborhoods
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/neighborhoods')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

If your request is successful, the API will return a response like this:

::: details Example Response {open}

```json
{
  "status": "OK",
  "data": [
    {
      "provinceId": 1,
      "districtId": 1757,
      "id": 176887,
      "province": "Adana",
      "district": "Aladağ",
      "name": "Akören",
      "population": 980
    },
    {
      "provinceId": 1,
      "districtId": 1757,
      "id": 248,
      "province": "Adana",
      "district": "Aladağ",
      "name": "Akpınar",
      "population": 654
    }
    // Other neighborhoods...
  ]
}
```

:::

## Getting Single Neighborhood Data

To get a single neighborhood's data, you can create the URL using the neighborhood ID as follows:

```url
https://api.turkiyeapi.dev/v1/neighborhoods/{id}
```

Here you should replace the `{id}` part with the ID of the neighborhood you want to get.

```bash [curl]
curl https://api.turkiyeapi.dev/v1/neighborhoods/176887
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/neighborhoods/176887')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

If your request is successful, the API will return a response like this:

::: details Example Response {open}

```json
{
  "status": "OK",
  "data": {
    "provinceId": 1,
    "districtId": 1757,
    "id": 176887,
    "province": "Adana",
    "district": "Aladağ",
    "name": "Akören",
    "population": 980
  }
}
```

:::

## Querying

The API provides various parameters for querying neighborhoods. These parameters allow you to filter neighborhoods according to specific criteria. For example, you can get neighborhoods belonging to a specific province or district, filter by population range, or search by neighborhood names.

::: info INFO
For examples related to this, you can visit the [API Examples](./examples.md) page.
:::

For `/neighborhoods`:

| Query Parameters | Type   | Description                                                                                                        |
| ---------------- | ------ | ------------------------------------------------------------------------------------------------------------------ |
| name             | string | Shows all neighborhoods that contain or match your search query.                                                   |
| minPopulation    | number | Shows all neighborhoods with a population greater than or equal to the value you entered.                          |
| maxPopulation    | number | Shows all neighborhoods with a population less than or equal to the value you entered.                             |
| provinceId       | number | Shows neighborhoods belonging to a specific province. This parameter filters by province ID.                       |
| province         | string | Shows neighborhoods belonging to a specific province. This parameter uses the province name.                       |
| districtId       | number | Shows neighborhoods belonging to a specific district. This parameter filters by district ID.                       |
| district         | string | Shows neighborhoods belonging to a specific district. This parameter uses the district name.                       |
| offset           | number | Determines which record to start from. The default value is 0.                                                     |
| limit            | number | Determines how many records to retrieve. The default value is 10.                                                  |
| fields           | string | Determines which fields to retrieve. For example, `fields=id,name,population` gets ID, name and population fields. |
| sort             | string | Determines which field to sort by. For example, `sort=name` sorts by the name field.                               |

For `/neighborhoods/{id}`:

| Path Variable | Description                                 |
| ------------- | ------------------------------------------- |
| id            | The ID of the neighborhood to be retrieved. |

| Query Parameters | Type   | Description                                                                                                        |
| ---------------- | ------ | ------------------------------------------------------------------------------------------------------------------ |
| fields           | string | Determines which fields to retrieve. For example, `fields=id,name,population` gets ID, name and population fields. |
