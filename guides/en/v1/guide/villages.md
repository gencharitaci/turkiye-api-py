---
outline: deep
---

# Villages

Villages are the administrative units that come after districts among Turkiye's administrative divisions. Each district is divided into one or more villages. There are more than 18,000 villages in Turkiye. By default, the API lists all villages first by the provinces they belong to, then by the districts they belong to, and then by their names.

::: info INFO
The provinces that villages belong to are not metropolitan municipalities. (`isMetropolitan: false`)
:::

The entry URL for villages is: `/v1/villages`.

## Village Properties

Village resources have the following properties:

- `provinceId`: Province ID that the village belongs to
- `districtId`: District ID that the village belongs to
- `id`: Village ID
- `province`: Name of the province that the village belongs to
- `district`: Name of the district that the village belongs to
- `name`: Village name
- `population`: Village population

## Getting Multiple Village Data

To get all villages, you only need to use the village URL. For example, you can use a URL like `/v1/villages` to get all villages.

```url
https://api.turkiyeapi.dev/v1/villages
```

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/villages
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/villages')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

If your request is successful, the API will return a response like this:

::: details Sample Response {open}

```json
{
  "status": "OK",
  "data": [
    {
      "provinceId": 2,
      "districtId": 1105,
      "id": 37777,
      "province": "Adıyaman",
      "district": "Merkez",
      "name": "100.yıl",
      "population": 60
    },
    {
      "provinceId": 2,
      "districtId": 1105,
      "id": 631,
      "province": "Adıyaman",
      "district": "Merkez",
      "name": "Ağaçkonak",
      "population": 170
    }
    // Other villages...
  ]
}
```

:::

## Getting Single Village Data

To get data for a single village, you can create a URL like `/v1/villages/{id}` using the village ID. For example, you can use the URL `/v1/villages/37777` to get the village with ID `37777`.

```url
https://api.turkiyeapi.dev/v1/villages/37777
```

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/villages/37777
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/villages/37777')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

If your request is successful, the API will return a response like this:

::: details Sample Response {open}

```json
{
  "status": "OK",
  "data": {
    "provinceId": 2,
    "districtId": 1105,
    "id": 37777,
    "province": "Adıyaman",
    "district": "Merkez",
    "name": "100.yıl",
    "population": 60
  }
}
```

:::

## Querying

To query the API, you can add query parameters to the URL. For example, you can use the `provinceId` parameter to get villages in a specific province.

::: info INFO
For examples of this, you can visit the [Sample API Calls](./examples.md) page.
:::

For `/villages`:

| Query Parameters | Type   | Description                                                                                                             |
| ---------------- | ------ | ----------------------------------------------------------------------------------------------------------------------- |
| name             | string | Shows all villages containing or matching your search query.                                                            |
| minPopulation    | number | Shows all villages with population greater than or equal to your value.                                                 |
| maxPopulation    | number | Shows all villages with population less than or equal to your value.                                                    |
| provinceId       | number | Shows villages belonging to a specific province. This parameter filters by province ID.                                 |
| province         | string | Shows villages belonging to a specific province. This parameter uses the province name.                                 |
| districtId       | number | Shows villages belonging to a specific district. This parameter filters by district ID.                                 |
| district         | string | Shows villages belonging to a specific district. This parameter uses the district name.                                 |
| offset           | number | Determines which record to start from. Default value is 0.                                                              |
| limit            | number | Determines how many records to retrieve. Default value is 10.                                                           |
| fields           | string | Determines which fields to retrieve. For example, `fields=id,name,population` retrieves ID, name and population fields. |
| sort             | string | Determines which field to sort by. For example, `sort=name` sorts by the name field.                                    |

For `/villages/{id}`:

| Path Variable | Description                    |
| ------------- | ------------------------------ |
| id            | ID of the village to retrieve. |

| Query Parameters | Type   | Description                                                                                                             |
| ---------------- | ------ | ----------------------------------------------------------------------------------------------------------------------- |
| fields           | string | Determines which fields to retrieve. For example, `fields=id,name,population` retrieves ID, name and population fields. |
