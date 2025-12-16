---
outline: deep
---

# Towns

By default, the API lists all towns first by the provinces they belong to, then by the districts they belong to, and then by their names.

::: info INFO
The scope of TurkiyeAPI's v1 version (without municipal units) includes provinces, districts, neighborhoods, and villages. However, since towns (a type of municipality) have an important place in the country, two routes have been allocated to them just like neighborhoods and villages. In short, this is a patch prepared for v1. However, unlike neighborhoods and villages, they are not shown in the `/districts/:id` route, meaning they are isolated within themselves. Still, the province-district names and IDs that districts belong to are specified in these routes starting with `/districts`, so you can use them to establish connections if you wish.
:::

::: warning WARNING
In v2 version, these routes will probably be removed and replaced with municipality-focused routes.
:::

The entry URL for towns is: `/v1/towns`.

## Town Properties

Town resources have the following properties:

- `provinceId`: Province ID that the town belongs to
- `districtId`: District ID that the town belongs to
- `id`: Town ID
- `province`: Name of the province that the town belongs to
- `district`: Name of the district that the town belongs to
- `name`: Town name
- `population`: Town population

## Getting Multiple Town Data

To get all towns, you only need to use the town URL. For example, you can use a URL like `/v1/towns` to get all towns.

```url
https://api.turkiyeapi.dev/v1/towns
```

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/towns
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/towns')
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
      "id": 1002,
      "province": "Adıyaman",
      "district": "Merkez",
      "name": "Kömür",
      "population": 3058
    },
    {
      "provinceId": 2,
      "districtId": 1105,
      "id": 1004,
      "province": "Adıyaman",
      "district": "Merkez",
      "name": "Yaylakonak",
      "population": 1906
    }
    // Other towns...
  ]
}
```

:::

## Getting Single Town Data

To get data for a single town, you can make a request using the town ID as follows:

```url
https://api.turkiyeapi.dev/v1/towns/:id
```

Here you should replace the `:id` part with the ID of the town you want to retrieve.

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/towns/1002
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/towns/1002')
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
    "id": 1002,
    "province": "Adıyaman",
    "district": "Merkez",
    "name": "Kömür",
    "population": 3058
  }
}
```

:::

## Querying

To query the API, you can add query parameters to the URL. For example, you can use the `provinceId` parameter to get towns in a specific province.

::: info INFO
For examples of this, you can visit the [Sample API Calls](./examples.md) page.
:::

For `/towns`:

| Query Parameters | Type   | Description                                                                                                             |
| ---------------- | ------ | ----------------------------------------------------------------------------------------------------------------------- |
| name             | string | Shows all towns containing or matching your search query.                                                               |
| minPopulation    | number | Shows all towns with population greater than or equal to your value.                                                    |
| maxPopulation    | number | Shows all towns with population less than or equal to your value.                                                       |
| provinceId       | number | Shows towns belonging to a specific province. This parameter filters by province ID.                                    |
| province         | string | Shows towns belonging to a specific province. This parameter uses the province name.                                    |
| districtId       | number | Shows towns belonging to a specific district. This parameter filters by district ID.                                    |
| district         | string | Shows towns belonging to a specific district. This parameter uses the district name.                                    |
| offset           | number | Determines which record to start from. Default value is 0.                                                              |
| limit            | number | Determines how many records to retrieve. Default value is 10.                                                           |
| fields           | string | Determines which fields to retrieve. For example, `fields=id,name,population` retrieves ID, name and population fields. |
| sort             | string | Determines which field to sort by. For example, `sort=name` sorts by the name field.                                    |

For `/towns/{id}`:

| Path Variable | Description                 |
| ------------- | --------------------------- |
| id            | ID of the town to retrieve. |

| Query Parameters | Type   | Description                                                                                                             |
| ---------------- | ------ | ----------------------------------------------------------------------------------------------------------------------- |
| fields           | string | Determines which fields to retrieve. For example, `fields=id,name,population` retrieves ID, name and population fields. |
