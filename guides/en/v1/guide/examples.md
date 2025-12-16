---
outline: deep
---

# Examples

If you're confused or want examples for clarification, you can review this page.

This API emphasizes query parameters more than path variables.

In this section, we'll use queries that are more likely to be used in real life.

## Searching Provinces

One of the first things an end user will probably do when they enter your website, application, etc. is to search for any province (or district, neighborhood, etc.). In this case, it would make the most sense to use this query.

::: warning WARNING
Remember that this method only deals with the names of provinces (or other units). If you want to search by ID, use `/v1/provinces/34` instead of `/v1/provinces?name=34`.
:::

Example usage:
::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/provinces?name=istanbul
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/provinces?name=istanbul')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

This query returns the province with the name `istanbul`. The result will be in JSON format.

::: details Example Response

```json
{
  "status": "OK",
  "data": [
    {
      "id": 34,
      "name": "İstanbul",
      "area": 5461,
      "population": 15840900,
      "altitude": 25,
      "areaCode": [212, 216],
      "isCoastal": true,
      "isMetropolitan": true,
      "nuts": {
        "nuts1": {
          "code": "TR1",
          "name": {
            "en": "İstanbul",
            "tr": "İstanbul"
          }
        },
        "nuts2": {
          "code": "TR10",
          "name": "İstanbul"
        },
        "nuts3": "TR100"
      },
      "coordinates": {
        "latitude": 41.01384,
        "longitude": 28.94966
      },
      "maps": {
        "googleMaps": "https://goo.gl/maps/wKdwRFM4NW8Wm6ZZ8",
        "openStreetMap": "https://www.openstreetmap.org/relation/223474"
      },
      "region": {
        "en": "Marmara",
        "tr": "Marmara"
      },
      "districts": [
        // Districts of İstanbul
      ]
    }
  ]
}
```

:::

## List regions within a specific population range

Users may want to list districts within a specific population range. In this example, let's assume the end user entered a minimum population of 100000 and a maximum population of 300000.

Example usage:
::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/districts?minPopulation=100000&maxPopulation=300000
```

```javascript [fetch]
fetch(
  'https://api.turkiyeapi.dev/v1/districts?minPopulation=100000&maxPopulation=300000',
)
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

This query returns all districts with a population between 100,000 and 300,000 in JSON format. The response comes with the name, population, province it belongs to, and other relevant information for each district.

::: details Example Response

```json
{
  "status": "OK",
  "data": [
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
      "id": 1486,
      "province": "Adana",
      "name": "Kozan",
      "population": 132642,
      "area": 1903
    },
    {
      "provinceId": 1,
      "id": 2032,
      "province": "Adana",
      "name": "Sarıçam",
      "population": 236298,
      "area": 770
    }
    // ... other districts
  ]
}
```

:::

## Pagination

Displaying 81 cities (with their districts) or 972 districts at once can be annoying for end users with slow connections, and your website, application, etc. can be filled with too much content at once. To prevent this, you can use the pagination method.

Example usage:
::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/provinces?offset=30&limit=10
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/provinces?offset=30&limit=10')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

This query returns provinces by paginating them according to the specified `offset` and `limit` values. For example, with the parameters `offset=30&limit=10`, it lists 10 provinces starting from the 31st position. This method is ideal for retrieving large datasets in chunks and providing users with a faster, more manageable experience.

::: details Example Response

```json
{
  "status": "OK",
  "data": [
    {
      "id": 31,
      "name": "Hatay",
      "area": 5524,
      "population": 1670712,
      "altitude": 89,
      "areaCode": [326],
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
          "code": "TR63",
          "name": "Hatay"
        },
        "nuts3": "TR631"
      },
      "coordinates": {
        "latitude": 36.2,
        "longitude": 36.16667
      },
      "maps": {
        "googleMaps": "https://goo.gl/maps/2VkFg1AM9B4Xv9W89",
        "openStreetMap": "https://www.openstreetmap.org/relation/223122"
      },
      "region": {
        "en": "Mediterranean",
        "tr": "Akdeniz"
      },
      "districts": [
        // Districts of Hatay
      ]
    },
    {
      "id": 32,
      "name": "Isparta",
      "area": 8946,
      "population": 445678,
      "altitude": 1058,
      "areaCode": [246],
      "isCoastal": false,
      "isMetropolitan": false,
      "nuts": {
        "nuts1": {
          "code": "TR6",
          "name": {
            "en": "Mediterranean",
            "tr": "Akdeniz"
          }
        },
        "nuts2": {
          "code": "TR61",
          "name": "Antalya"
        },
        "nuts3": "TR612"
      },
      "coordinates": {
        "latitude": 37.76667,
        "longitude": 30.55
      },
      "maps": {
        "googleMaps": "https://goo.gl/maps/v8tcHjuuCKyNMn687",
        "openStreetMap": "https://www.openstreetmap.org/relation/223134"
      },
      "region": {
        "en": "Mediterranean",
        "tr": "Akdeniz"
      },
      "districts": [
        // Districts of Isparta
      ]
    }
    // Other 8 provinces
  ]
}
```

:::

## Fields

When you want to get just one or more provinces/districts, you get all the data like ID, province/district name, area, population, etc. But do you really need all this data?

Imagine you want to list all provinces. In this case, you need to get the data of these provinces, but on the other hand, each province has its own districts. However, you don't need information about these districts, you only need information about the cities. In this case, you will need to use a field query.

Example usage:
::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/provinces?fields=id,name,area,population,altitude,areaCode,isCoastal,isMetropolitan,maps,region
```

```javascript [fetch]
fetch(
  'https://api.turkiyeapi.dev/v1/provinces?fields=id,name,area,population,altitude,areaCode,isCoastal,isMetropolitan,maps,region',
)
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

In this example, we want to get all fields except NUTS and districts. In this case, we need to write all fields except districts. Note that there is a comma between each field.

::: details Example Response

```json
{
  "status": "OK",
  "data": [
    {
      "id": 1,
      "name": "Adana",
      "area": 13844,
      "population": 2263373,
      "altitude": 25,
      "areaCode": [322],
      "isCoastal": true,
      "isMetropolitan": true,
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
      }
    },
    {
      "id": 2,
      "name": "Adıyaman",
      "area": 7337,
      "population": 632148,
      "altitude": 701,
      "areaCode": [416],
      "isCoastal": false,
      "isMetropolitan": false,
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
      }
    }
    // Other 79 provinces
  ]
}
```

:::

## Sorting

By default, districts are classified first by the provinces they belong to, and if the districts belong to the same provinces, by their names. To change this sorting, we need to use a sort query.

Example usage:
::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/districts?sort=-population
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/districts?sort=-population')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

In this example, let's sort all regions from most populated to least populated.

::: info NOTE
As you noticed, there is a minus `-` sign before `population` in the `?sort=-population` query. This symbol is used to change ascending sorting to descending. In this example, we will use this sign to sort from the most populated district to the least populated district.
:::

::: details Example Response

```json
{
  "status": "OK",
  "data": [
    // First two districts
    {
      "id": 2053,
      "name": "Esenyurt",
      "area": 43,
      "population": 977489,
      "province": "İstanbul"
    },
    {
      "id": 1231,
      "name": "Çankaya",
      "area": 483,
      "population": 949265,
      "province": "Ankara"
    },
    // Other 968 districts
    {
      "id": 1379,
      "name": "Hamur",
      "area": 873,
      "population": 1710,
      "province": "Ağrı"
    },
    {
      "id": 1994,
      "name": "Yalıhüyük",
      "area": 94,
      "population": 1532,
      "province": "Konya"
    }
    // Last two districts
  ]
}
```

:::

## Complex Queries

Example usage:
::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/districts?name=i&minPopulation=100000&sort=name&offset=10&limit=20
```

```javascript [fetch]
fetch(
  'https://api.turkiyeapi.dev/v1/districts?name=i&minPopulation=100000&sort=name&offset=10&limit=20',
)
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

Of course, you can use multiple queries for a single URL. When you send this request, it **_sorts_** cities with a population of at least `100000` and containing the letter `i` in their name in `ascending` order and gives you districts from `11th` to `30th`.

::: details Example Response

```json
{
  "status": "OK",
  "data": [
    {
      "id": 2051,
      "name": "Beylikdüzü",
      "area": 39,
      "population": 398122,
      "province": "İstanbul"
    },
    {
      "id": 1195,
      "name": "Bismil",
      "area": 1679,
      "population": 118592,
      "province": "Diyarbakır"
    },
    {
      "id": 1223,
      "name": "Cizre",
      "area": 444,
      "population": 155182,
      "province": "Şırnak"
    },
    {
      "id": 2007,
      "name": "Çiğli",
      "area": 139,
      "population": 209951,
      "province": "İzmir"
    }
    // 16 more districts...
  ]
}
```

:::

Good luck!
