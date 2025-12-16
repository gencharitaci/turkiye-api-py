---
outline: deep
---

# İlçeler

Türkiye'nin idari bölümleri arasında illerden sonra gelen birimlerdir. Her il, bir veya daha fazla ilçeye ayrılmıştır. Türkiye'de toplam 973 ilçe bulunmaktadır. Varsayılan olarak API, bütün ilçeleri önce bağlı oldukları illere göre ardından da adlarına göre listeler.

İlçeler için giriş URL'si: `/v1/districts` şeklindedir.

## İlçe Özellikleri

İlçe kaynakları, aşağıdaki özelliklere sahiptir:

- `provinceId`: İlçenin bağlı olduğu il ID'si
- `id`: İlçenin ID'si
- `province`: İlçenin bağlı olduğu il adı
- `name`: İlçenin adı
- `population`: İlçenin nüfusu
- `area`: İlçenin yüzölçümü (km²)
- `neighborhoods`: İlçenin mahalleleri (yalnızca `GET /v1/districts/{id}` ile erişilebilir)
- `villages`: İlçenin köyleri (yalnızca `GET /v1/districts/{id}` ile erişilebilir)

::: info BİLGİ
Bir ilçenin mahalleleri ve köyleri, yalnızca o ilçeye ait ID ile sorgulandığında döndürülür. Örneğin, `GET /v1/districts/1757` isteği ile `Aladağ` ilçesinin mahallelerine erişebilirsiniz.
:::

::: info BİLGİ
Bir ilçeye bağlı olan köylerin olabilmesi için, o ilçenin bağlı olduğu ilin büyükşehir olmaması (`isMetropolitan: false`) gerekir. Eğer il büyükşehir ise, ilçeye bağlı köyler boş bir dizi `[]` olarak döndürülür.
:::

## Birden Fazla İlçe Verilerini Almak

Bütün ilçeleri almak için, yalnızca ilçe URL'sini kullanmanız yeterlidir. Örneğin, bütün ilçeleri almak için `/v1/districts` gibi bir URL kullanabilirsiniz.

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

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir:

::: details Örnek Yanıt {open}

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
    // Diğer ilçeler...
  ]
}
```

:::

## Belirli Bir İlçeyi Almak

Belirli bir ilçeyi almak için, ilçe ID'sini kullanarak URL'yi şu şekilde oluşturabilirsiniz:

```url
https://api.turkiyeapi.dev/v1/districts/{id}
```

Burada `{id}` kısmını almak istediğiniz ilçenin ID'si ile değiştirmelisiniz.

```bash [curl]
curl https://api.turkiyeapi.dev/v1/districts/1757
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/districts/1757')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir:

::: details Örnek Yanıt {open}

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
      // Diğer mahalleler...
    ],
    "villages": []
  }
}
```

:::

## Sorgulama

API, ilçeleri sorgulamak için çeşitli parametreler sunar. Bu parametreler, belirli alanları seçmek, sıralama yapmak ve filtreleme gibi işlemleri içerir.

::: info BİLGİ
Bununla ilgili örnekler için [Örnek API Çağrıları](./examples.md) sayfasını ziyaret edebilirsiniz.
:::

`/districts` için:

| Sorgu Parametreleri | Tip    | Açıklama                                                                                     |
| ------------------- | ------ | -------------------------------------------------------------------------------------------- |
| name                | string | Arama sorgunuzu içeren veya eşleşen tüm ilçeleri gösterir.                                   |
| minPopulation       | number | Nüfusu girdiğiniz değerden büyük veya eşit olan tüm ilçeleri gösterir.                       |
| maxPopulation       | number | Nüfusu girdiğiniz değerden küçük veya eşit olan tüm ilçeleri gösterir.                       |
| minArea             | number | Yüzölçümü girdiğiniz değerden büyük veya eşit olan tüm ilçeleri gösterir.                    |
| maxArea             | number | Yüzölçümü girdiğiniz değerden küçük veya eşit olan tüm ilçeleri gösterir.                    |
| provinceId          | number | Belirli bir ile ait ilçeleri gösterir. Bu parametre, il ID'si ile filtreleme yapar.          |
| province            | string | Belirli bir ile ait ilçeleri gösterir. Bu parametre, il adını kullanır.                      |
| offset              | number | Sonuçların başlangıç noktasını belirler. Örneğin, `offset=10` ile 11. kayıttan başlar.       |
| limit               | number | Alınacak maksimum kayıt sayısını belirler. Örneğin, `limit=10` ile en fazla 10 kayıt alır.   |
| fields              | string | Alınacak alanları belirler. Örneğin, `fields=id,name` ile sadece ID ve isim alanlarını alır. |
| sort                | string | Sıralama kriterini belirler. Örneğin, `sort=name` ile isim alanına göre sıralar.             |

`/districts/{id}` için:

| Path Değişkeni | Açıklama                       |
| -------------- | ------------------------------ |
| id             | Alınmak istenen ilçenin ID'si. |

| Sorgu Parametreleri | Tip    | Açıklama                                                                                                |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------- |
| fields              | string | Alınacak alanları belirler. Örneğin, `fields=id,name,population` ile ID, isim ve nüfus alanlarını alır. |
