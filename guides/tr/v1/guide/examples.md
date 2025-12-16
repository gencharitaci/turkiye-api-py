---
outline: deep
---

# Örnekler

Kafanız karıştıysa veya örneklerle açıklama istiyorsanız bu sayfayı inceleyebilirsiniz.

Bu API, sorgu parametrelerini yol değişkenlerinden daha fazla vurgular.

Bu bölümde gerçek hayatta kullanılma olasılığı daha yüksek olan sorguları kullanacağız.

## İlleri Arama

Son kullanıcının sitenize, uygulamanıza vb. girdiğinde yapacağı ilk şeylerden biri muhtemelen herhangi bir ili (veya ilçeyi, mahalleyi vb.) aramak olacaktır. Bu durumda bu sorguyu kullanmak en mantıklısı olacaktır.

::: warning UYARI
Bu yöntemin yalnızca illerin (veya diğer birimlerin) adlarıyla ilgilendiğini unutmayın. Eğer ID ile arama yapmak istiyorsanız, bunun için `/v1/provinces?name=34` yerine `/v1/provinces/34` kullanın.
:::

Örnek kullanım:
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

Bu sorgu, adı `istanbul` olan ili döndürür. Sonuç JSON formatında olacaktır.

::: details Örnek Yanıt

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

## Belirli bir nüfus aralığındaki bölgeleri listeleyin

Kullanıcılar belirli bir nüfus aralığındaki ilçeleri listelemek isteyebilir. Bu örnekte, son kullanıcının minimum nüfus olarak 100000 ve maksimum nüfus olarak 300000 girdiğini varsayalım.

Örnek kullanım:
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

Bu sorgu, nüfusu 100.000 ile 300.000 arasında olan tüm ilçeleri JSON formatında döndürür. Yanıt, her bir ilçenin adı, nüfusu, bağlı olduğu il ve diğer ilgili bilgilerle birlikte gelir.

::: details Örnek Yanıt

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
    // ... diğer ilçeler
  ]
}
```

:::

## Sayfalandırma

81 şehri (ilçeleriyle birlikte) veya 972 ilçeyi aynı anda görüntülemek, yavaş bağlantıları olan son kullanıcılar için can sıkıcı olabileceği gibi siteniz, uygulamanız vb. bir anda çok fazla içerikle dolabilir. Bunu önlemek için sayfalandırma yöntemini kullanabilirsiniz.

Örnek kullanım:
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

Bu sorgu, belirtilen `offset` ve `limit` değerlerine göre illeri sayfalandırarak döndürür. Örneğin, `offset=30&limit=10` parametreleri ile 31. sıradan başlayarak 10 ili listeler. Bu yöntem, büyük veri kümelerini parça parça almak ve kullanıcıya daha hızlı, yönetilebilir bir deneyim sunmak için idealdir.

::: details Örnek Yanıt

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

## Alanlar

Sadece bir veya daha fazla il/ilçeyi elde etmek istediğinizde ID, il/ilçe adı, alan, nüfus vb. tüm verileri elde edersiniz. Ama tüm bu verilere gerçekten ihtiyacınız var mı?

Tüm illeri listelemek istediğinizi düşünün. Bu durumda bu illerin verilerini almanız gerekiyor ama öte yandan her ilin kendi ilçeleri var. Ancak bu ilçelerin bilgisine ihtiyacınız yok, sadece şehirlerin bilgisine ihtiyacınız var. Bu durumda alan sorgusu kullanmanız gerekecektir.

Örnek kullanım:
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

Bu örnekte NUTS (İBBS) ve ilçeler hariç tüm alanları almak istiyoruz. Bu durumda, ilçeler hariç tüm alanları yazmalıyız. Her alan arasında virgül olduğuna dikkat edin.

::: details Örnek Yanıt

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

## Sıralama

Varsayılan olarak ilçeler önce bağlı oldukları illere göre, eğer ilçeler aynı illere bağlı ise isimlerine göre sınıflandırılır. Bu sıralamayı değiştirmek için sort sorgusu kullanmalıyız.

Örnek kullanım:
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

Bu örnekte, tüm bölgeleri en kalabalıktan en az nüfusa doğru sıralayalım.

::: info NOT
Dikkat ettiyseniz, `?sort=-population` sorgusunda `population`'dan önce bir eksi `-` işareti vardır. Bu sembol, artan sıralamayı azalan olarak değiştirmek için kullanılır. Bu örnekte, en kalabalık ilçeden en az nüfusa sahip ilçeye doğru sıralama yapmak için bu işareti kullanacağız.
:::

::: details Örnek Yanıt

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

## Karmaşık Sorgular

Örnek kullanım:
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

Elbette, tek bir URL için birden fazla sorgu kullanabilirsiniz. Bu isteği gönderdiğinizde, nüfusu en az `100000` olan ve adında `i` harfi bulunan şehirleri `artan` şekilde **_sıralar_** ve size `11`'den `30`'a kadar olan ilçeleri verir.

::: details Örnek Yanıt

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
    // 16 ilçe daha...
  ]
}
```

:::

Bol şanslar!
