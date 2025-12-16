---
outline: deep
---

# İller

Türkiye'nin idari bölümleri arasında en üst seviyede yer alan birimlerdir. Türkiye'de toplam 81 il bulunmaktadır ve her il, bir il merkezi ile birlikte toplamda 973 ilçeye ayrılmıştır. Varsayılan olarak API, bütün illeri ID'lerine göre listeler, bu ID'ler aynı zamanda illerin **plaka kodlarıdır**.

İller için giriş URL'si: `/v1/provinces` şeklindedir.

## İl Özellikleri

İl kaynakları, aşağıdaki özelliklere sahiptir:

- `id`: İlin ID'si (ve karşılık gelen plaka kodu)
- `name`: İlin adı
- `population`: İlin nüfusu
- `area`: İlin yüzölçümü (km²)
- `altitude`: Yükseklik (m)
- `areaCode`: İlin alan kodları
- `isCoastal`: Kıyı ili olup olmadığı
- `isMetropolitan`: Büyükşehir olup olmadığı
- `nuts`: İBBS sınıflandırmaları
- `coordinates`: Coğrafi koordinatlar
- `maps`: Harita bağlantıları
- `region`: İlin bölgesi
- `districts`: İlin ilçeleri

## Birden Fazla İl Verilerini Almak

Bütün illeri almak için, yalnızca il URL'sini kullanmanız yeterlidir. Örneğin, bütün illeri almak için `/v1/provinces` gibi bir URL kullanabilirsiniz.

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

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir:

::: details Örnek Yanıt {open}

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
        // 12 ilçe daha...
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
        // 6 ilçe daha...
      ]
    }
    // 79 il daha...
  ]
}
```

:::

## Tek İl Verilerini Almak

Tek bir ilin verilerini almak için, il ID'sini URL'ye eklemeniz yeterlidir. Örneğin, Adana ilinin verilerini almak için `/v1/provinces/1` gibi bir URL kullanabilirsiniz.

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

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir:

::: details Örnek Yanıt {open}

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

## Sorgulama

İller üzerinde sorgulama yapabilirsiniz. Örneğin, yalnızca kıyı illerini veya büyükşehir olan illeri almak için sorgu parametreleri kullanabilirsiniz.

::: info BİLGİ
Bununla ilgili örnekler için [Örnek API Çağrıları](./examples.md) sayfasını ziyaret edebilirsiniz.
:::

`/provinces` için:

| Sorgu Parametreleri | Tip     | Açıklama                                                                |
| ------------------- | ------- | ----------------------------------------------------------------------- |
| name                | string  | Arama sorgunuzu içeren veya eşleşen tüm illeri gösterir.                |
| minPopulation       | number  | Nüfusu girdiğiniz değerden büyük veya eşit olan tüm illeri gösterir.    |
| maxPopulation       | number  | Nüfusu girdiğiniz değerden küçük veya eşit olan tüm illeri gösterir.    |
| minArea             | number  | Yüzölçümü girdiğiniz değerden büyük veya eşit olan tüm illeri gösterir. |
| maxArea             | number  | Yüzölçümü girdiğiniz değerden küçük veya eşit olan tüm illeri gösterir. |
| minAltitude         | number  | Rakımı girdiğiniz değerden büyük veya eşit olan tüm illeri gösterir.    |
| maxAltitude         | number  | Rakımı girdiğiniz değerden küçük veya eşit olan tüm illeri gösterir.    |
| isCoastal           | boolean | Kıyı illeri için `true`, diğerleri için `false`                         |
| isMetropolitan      | boolean | Büyükşehir olan iller için `true`, diğerleri için `false`               |
| offset              | number  | Kaçıncı kayıttan başlayacağını belirler (varsayılan: 0)                 |
| limit               | number  | Kaç kayıt alınacağını belirler (varsayılan: 81)                         |
| fields              | string  | Hangi alanların alınacağını belirler (örneğin: `id,name`)               |
| sort                | string  | Hangi alana göre sıralanacağını belirler (örneğin: `-name`)             |

`/provinces/{id}` için:

| Path Değişkeni | Açıklama                    |
| -------------- | --------------------------- |
| id             | Alınmak istenen ilin ID'si. |

| Sorgu Parametreleri | Tip     | Açıklama                                                     |
| ------------------- | ------- | ------------------------------------------------------------ |
| fields              | string  | Hangi alanların alınacağını belirler (örneğin: `id,name`)    |
| extend              | boolean | İlin genişletilmiş verilerini (mahalle ve köyleri) gösterir. |
