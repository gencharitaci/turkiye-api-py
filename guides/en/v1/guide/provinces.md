---
outline: deep
---

# Provinces

Provinces are the highest-level administrative divisions of Turkey. Turkey has a total of 81 provinces, and each province is divided into a total of 973 districts along with a provincial center. By default, the API lists all provinces according to their IDs, which are also the **license plate codes** of the provinces.

The entry URL for provinces is: `/v1/provinces`.

## Province Properties

Province resources have the following properties:

- `id`: Province ID (and corresponding license plate code)
- `name`: Province name
- `population`: Province population
- `area`: Province area (km²)
- `altitude`: Altitude (m)
- `areaCode`: Province area codes
- `isCoastal`: Whether it is a coastal province
- `isMetropolitan`: Whether it is a metropolitan province
- `nuts`: NUTS classifications
- `coordinates`: Geographic coordinates
- `maps`: Map links
- `region`: Province region
- `districts`: Province districts

## Getting Multiple Province Data

To get all provinces, you only need to use the province URL. For example, you can use a URL like `/v1/provinces` to get all provinces.

```url
https://api.turkiyeapi.dev/v1/provinces
```

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/provinces
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/provinces')
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
      "id": 1,
      "name": "Adana",
      "population": 2270298,
      "area": 13844,
      "altitude": 25,
      "areaCode": [322],
      "isCoastal": true,
      "isMetropolitan": true,
      "nuts": {
        "nuts1": {
          "code": "TR6",
          "name": {
            "en": "Mediterranean",
            "tr": "Akdeniz"
          }
        },
        "nuts2": {
          "code": "TR62",
          "name": "Adana"
        },
        "nuts3": "TR621"
      },
      "coordinates": {
        "latitude": 37.001667,
        "longitude": 35.328889
      },
      "maps": {
        "googleMaps": "https://goo.gl/maps/4yHUNdZuhcBn7rqX8",
        "openStreetMap": "https://www.openstreetmap.org/relation/167216"
      },
      "region": {
        "en": "Mediterranean",
        "tr": "Akdeniz"
      },
      "districts": [
        {
          "id": 1757,
          "name": "Aladağ",
          "population": 16954,
          "area": 1340
        },
        {
          "id": 1219,
          "name": "Ceyhan",
          "population": 156610,
          "area": 1426
        },
        {
          "id": 2033,
          "name": "Çukurova",
          "population": 374205,
          "area": 250
        }
        // 12 more districts...
      ]
    },
    {
      "id": 2,
      "name": "Adıyaman",
      "population": 604978,
      "area": 7337,
      "altitude": 701,
      "areaCode": [416],
      "isCoastal": false,
      "isMetropolitan": false,
      "nuts": {
        "nuts1": {
          "code": "TRC",
          "name": {
            "en": "Southeast Anatolia",
            "tr": "Güneydoğu Anadolu"
          }
        },
        "nuts2": {
          "code": "TRC1",
          "name": "Gaziantep"
        },
        "nuts3": "TRC12"
      },
      "coordinates": {
        "latitude": 37.764722,
        "longitude": 38.278611
      },
      "maps": {
        "googleMaps": "https://goo.gl/maps/UqRzeK1ApyPjbhpp6",
        "openStreetMap": "https://www.openstreetmap.org/relation/223141"
      },
      "region": {
        "en": "Southeastern Anatolia",
        "tr": "Güneydoğu Anadolu"
      },
      "districts": [
        {
          "id": 1182,
          "name": "Besni",
          "population": 76415,
          "area": 1235
        },
        {
          "id": 1246,
          "name": "Çelikhan",
          "population": 14856,
          "area": 444
        },
        {
          "id": 1347,
          "name": "Gerger",
          "population": 15679,
          "area": 668
        }
        // 6 more districts...
      ]
    }
    // 79 more provinces...
  ]
}
```

:::

## Getting Single Province Data

To get data for a single province, you just need to add the province ID to the URL. For example, you can use a URL like `/v1/provinces/1` to get data for Adana province.

```url
https://api.turkiyeapi.dev/v1/provinces/1
```

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/provinces/1
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/provinces/1')
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
    "id": 1,
    "name": "Adana",
    "population": 2270298,
    "area": 13844,
    "altitude": 25,
    "areaCode": [322],
    "isCoastal": true,
    "isMetropolitan": true,
    "nuts": {
      "nuts1": {
        "code": "TR6",
        "name": {
          "en": "Mediterranean",
          "tr": "Akdeniz"
        }
      },
      "nuts2": {
        "code": "TR62",
        "name": "Adana"
      },
      "nuts3": "TR621"
    },
    "coordinates": {
      "latitude": 37.001667,
      "longitude": 35.328889
    },
    "maps": {
      "googleMaps": "https://goo.gl/maps/4yHUNdZuhcBn7rqX8",
      "openStreetMap": "https://www.openstreetmap.org/relation/167216"
    },
    "region": {
      "en": "Mediterranean",
      "tr": "Akdeniz"
    },
    "districts": [
      {
        "id": 1757,
        "name": "Aladağ",
        "population": 16954,
        "area": 1340
      },
      {
        "id": 1219,
        "name": "Ceyhan",
        "population": 156610,
        "area": 1426
      },
      {
        "id": 2033,
        "name": "Çukurova",
        "population": 374205,
        "area": 250
      },
      {
        "id": 1329,
        "name": "Feke",
        "population": 17304,
        "area": 1218
      },
      {
        "id": 1806,
        "name": "İmamoğlu",
        "population": 27341,
        "area": 445
      },
      {
        "id": 1437,
        "name": "Karaisalı",
        "population": 23105,
        "area": 1165
      },
      {
        "id": 1443,
        "name": "Karataş",
        "population": 25245,
        "area": 862
      },
      {
        "id": 1486,
        "name": "Kozan",
        "population": 132642,
        "area": 1903
      },
      {
        "id": 1580,
        "name": "Pozantı",
        "population": 20733,
        "area": 899
      },
      {
        "id": 1588,
        "name": "Saimbeyli",
        "population": 13857,
        "area": 989
      },
      {
        "id": 2032,
        "name": "Sarıçam",
        "population": 236298,
        "area": 770
      },
      {
        "id": 1104,
        "name": "Seyhan",
        "population": 787771,
        "area": 444
      },
      {
        "id": 1687,
        "name": "Tufanbeyli",
        "population": 17258,
        "area": 851
      },
      {
        "id": 1734,
        "name": "Yumurtalık",
        "population": 18630,
        "area": 447
      },
      {
        "id": 1748,
        "name": "Yüreğir",
        "population": 402345,
        "area": 835
      }
    ]
  }
}
```

:::

## Querying

You can query on provinces. For example, you can use query parameters to get only coastal provinces or metropolitan provinces.

::: info INFO
For examples of this, you can visit the [Sample API Calls](./examples.md) page.
:::

For `/provinces`:

| Query Parameters | Type    | Description                                                              |
| ---------------- | ------- | ------------------------------------------------------------------------ |
| name             | string  | Shows all provinces containing or matching your search query.            |
| minPopulation    | number  | Shows all provinces with population greater than or equal to your value. |
| maxPopulation    | number  | Shows all provinces with population less than or equal to your value.    |
| minArea          | number  | Shows all provinces with area greater than or equal to your value.       |
| maxArea          | number  | Shows all provinces with area less than or equal to your value.          |
| minAltitude      | number  | Shows all provinces with altitude greater than or equal to your value.   |
| maxAltitude      | number  | Shows all provinces with altitude less than or equal to your value.      |
| isCoastal        | boolean | `true` for coastal provinces, `false` for others                         |
| isMetropolitan   | boolean | `true` for metropolitan provinces, `false` for others                    |
| offset           | number  | Determines which record to start from (default: 0)                       |
| limit            | number  | Determines how many records to retrieve (default: 81)                    |
| fields           | string  | Determines which fields to retrieve (e.g., `id,name`)                    |
| sort             | string  | Determines which field to sort by (e.g., `-name`)                        |

For `/provinces/{id}`:

| Path Variable | Description                     |
| ------------- | ------------------------------- |
| id            | ID of the province to retrieve. |

| Query Parameters | Type    | Description                                                       |
| ---------------- | ------- | ----------------------------------------------------------------- |
| fields           | string  | Determines which fields to retrieve (e.g., `id,name`)             |
| extend           | boolean | Shows extended data of the province (neighborhoods and villages). |
