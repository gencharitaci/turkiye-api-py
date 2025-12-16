---
outline: deep
---

# Key Concepts

This section explains the core concepts and terminology of TurkiyeAPI. These terms frequently appear throughout the API, and understanding them will help you use it more effectively.

## Path Variables

The following path variables are used in the API:

- `:provinceId`: Province ID
- `:districtId`: District ID
- `:neighborhoodId`: Neighborhood ID
- `:villageId`: Village ID

```plaintext
/v1/
├─/provinces
│   └─/:provinceId
├─/districts
│   └─/:districtId
├─/neighborhoods
│   └─/:neighborhoodId
├─/villages
│   └─/:villageId
```

::: warning WARNING
The values you provide for path variables must be numbers. Otherwise, the API will return a 404 error.
:::

::: danger SAMPLE ERROR

```plaintext
GET /v1/provinces/istanbul
```

In the example above, the value `istanbul` is **not a valid number** for `:provinceId` _(even though it is a real province)_, so the API will return a `404` error:

```json {3}
{
  "status": "ERROR",
  "message": "Invalid province ID. The id parameter must be a number."
}
```

:::

## Query Parameters

The following query parameters are supported by the API:

- For filtering by fields (most common):
  - `name`: Name
  - `minPopulation`: Minimum population
  - `maxPopulation`: Maximum population
  - `minArea`: Minimum area
  - `maxArea`: Maximum area
  - `isMetropolitan`: Whether it is a metropolitan municipality
  - _and more..._
- `offset`: Determines where the result set should start
- `limit`: Specifies how many records to return
- `fields`: Specifies which fields to include in the response
- `sort`: Specifies the field by which to sort the results

::: details EXAMPLE {open}

To retrieve the first 10 provinces that contain the letter `a` in their name, sorted alphabetically by name, and return only `id` and `name` fields:

```plaintext
GET /v1/provinces?name=a&offset=0&limit=10&fields=id,name&sort=name
```

Response:

```json
{
  "status": "OK",
  "data": [
    {
      "id": 1,
      "name": "Adana"
    },
    {
      "id": 2,
      "name": "Adıyaman"
    },
    {
      "id": 3,
      "name": "Afyonkarahisar"
    },
    {
      "id": 4,
      "name": "Ağrı"
    },
    {
      "id": 68,
      "name": "Aksaray"
    },
    {
      "id": 5,
      "name": "Amasya"
    },
    {
      "id": 6,
      "name": "Ankara"
    },
    {
      "id": 7,
      "name": "Antalya"
    },
    {
      "id": 75,
      "name": "Ardahan"
    },
    {
      "id": 8,
      "name": "Artvin"
    }
  ]
}
```

:::

::: tip TIP

To sort in descending order, prefix the field name in the `sort` parameter with a `-` sign:

:::

::: details EXAMPLE {open}

To sort provinces by name in descending order:

```plaintext
GET /v1/provinces?fields=id,name&sort=-name
```

Response:

```json
{
  "status": "OK",
  "data": [
    {
      "id": 67,
      "name": "Zonguldak"
    },
    {
      "id": 66,
      "name": "Yozgat"
    },
    {
      "id": 77,
      "name": "Yalova"
    },
    {
      "id": 65,
      "name": "Van"
    },
    {
      "id": 64,
      "name": "Uşak"
    },
    {
      "id": 62,
      "name": "Tunceli"
    },
    {
      "id": 61,
      "name": "Trabzon"
    },
    {
      "id": 60,
      "name": "Tokat"
    },
    {
      "id": 59,
      "name": "Tekirdağ"
    },
    {
      "id": 73,
      "name": "Şırnak"
    },
    {
      "id": 63,
      "name": "Şanlıurfa"
    },
    {
      "id": 58,
      "name": "Sivas"
    },
    // 56 more provinces...
    {
      "id": 74,
      "name": "Bartın"
    },
    {
      "id": 10,
      "name": "Balıkesir"
    },
    {
      "id": 9,
      "name": "Aydın"
    },
    {
      "id": 8,
      "name": "Artvin"
    },
    {
      "id": 75,
      "name": "Ardahan"
    },
    {
      "id": 7,
      "name": "Antalya"
    },
    {
      "id": 6,
      "name": "Ankara"
    },
    {
      "id": 5,
      "name": "Amasya"
    },
    {
      "id": 68,
      "name": "Aksaray"
    },
    {
      "id": 4,
      "name": "Ağrı"
    },
    {
      "id": 3,
      "name": "Afyonkarahisar"
    },
    {
      "id": 2,
      "name": "Adıyaman"
    },
    {
      "id": 1,
      "name": "Adana"
    }
  ]
}
```

:::

::: tip TIP

You can sort by multiple fields by separating them with commas.

:::

::: details EXAMPLE {open}

To sort districts first by their province names (`province`), then by population (`population`):

```plaintext
GET /v1/districts?fields=name,province,population&sort=province,population
```

Response:

```json
{
  "status": "OK",
  "data": [
    {
      "name": "Seyhan",
      "province": "Adana",
      "population": 787771
    },
    {
      "name": "Yüreğir",
      "province": "Adana",
      "population": 402345
    },
    {
      "name": "Çukurova",
      "province": "Adana",
      "population": 374205
    },
    {
      "name": "Sarıçam",
      "province": "Adana",
      "population": 236298
    },
    {
      "name": "Ceyhan",
      "province": "Adana",
      "population": 156610
    },
    {
      "name": "Kozan",
      "province": "Adana",
      "population": 132642
    },
    {
      "name": "İmamoğlu",
      "province": "Adana",
      "population": 27341
    },
    {
      "name": "Karataş",
      "province": "Adana",
      "population": 25245
    },
    {
      "name": "Karaisalı",
      "province": "Adana",
      "population": 23105
    },
    {
      "name": "Pozantı",
      "province": "Adana",
      "population": 20733
    },
    {
      "name": "Yumurtalık",
      "province": "Adana",
      "population": 18630
    },
    {
      "name": "Feke",
      "province": "Adana",
      "population": 17304
    },
    {
      "name": "Tufanbeyli",
      "province": "Adana",
      "population": 17258
    },
    {
      "name": "Aladağ",
      "province": "Adana",
      "population": 16954
    },
    {
      "name": "Saimbeyli",
      "province": "Adana",
      "population": 13857
    },
    {
      "name": "Merkez",
      "province": "Adıyaman",
      "population": 284839
    },
    {
      "name": "Kahta",
      "province": "Adıyaman",
      "population": 132303
    },
    {
      "name": "Besni",
      "province": "Adıyaman",
      "population": 76415
    },
    {
      "name": "Gölbaşı",
      "province": "Adıyaman",
      "population": 47876
    },
    {
      "name": "Sincik",
      "province": "Adıyaman",
      "population": 16477
    }
  ]
}
```

:::
