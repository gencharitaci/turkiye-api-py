---
outline: deep
---

# Köyler

Türkiye'nin idari bölümleri arasında ilçelerden sonra gelen birimlerdir. Her ilçe, bir veya daha fazla köye ayrılmıştır. Türkiye'de toplam 18 000'den fazla köy bulunmaktadır. Varsayılan olarak API, bütün köyleri önce bağlı oldukları illere göre, sonra bağlı oldukları ilçelere göre, ardından da adlarına göre listeler.

::: info BİLGİ
Köylerin bağlı olduğu iller büyükşehir belediyesi değildir. (`isMetropolitan: false`)
:::

Köyler için giriş URL'si: `/v1/villages` şeklindedir.

## Köy Özellikleri

Köy kaynakları, aşağıdaki özelliklere sahiptir:

- `provinceId`: Köyün bağlı olduğu il ID'si
- `districtId`: Köyün bağlı olduğu ilçe ID'si
- `id`: Köyün ID'si
- `province`: Köyün bağlı olduğu il adı
- `district`: Köyün bağlı olduğu ilçe adı
- `name`: Köyün adı
- `population`: Köyün nüfusu

## Birden Fazla Köy Verilerini Almak

Bütün köyleri almak için, yalnızca köy URL'sini kullanmanız yeterlidir. Örneğin, bütün köyleri almak için `/v1/villages` gibi bir URL kullanabilirsiniz.

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

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir:

::: details Örnek Yanıt {open}

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
    // Diğer köyler...
  ]
}
```

:::

## Tek Bir Köy Verisini Almak

Tek bir köy verisini almak için, köyün ID'sini kullanarak `/v1/villages/{id}` şeklinde bir URL oluşturabilirsiniz. Örneğin, ID'si `37777` olan köyü almak için `/v1/villages/37777` URL'sini kullanabilirsiniz.

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

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir:

::: details Örnek Yanıt {open}

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

## Sorgulama

API'de sorgulama yapmak için, URL'ye sorgu parametreleri ekleyebilirsiniz. Örneğin, belirli bir ildeki köyleri almak için `provinceId` parametresini kullanabilirsiniz.

::: info BİLGİ
Bununla ilgili örnekler için [Örnek API Çağrıları](./examples.md) sayfasını ziyaret edebilirsiniz.
:::

`/villages` için:

| Sorgu Parametreleri | Tip    | Açıklama                                                                                                |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------- |
| name                | string | Arama sorgunuzu içeren veya eşleşen tüm köyleri gösterir.                                               |
| minPopulation       | number | Nüfusu girdiğiniz değerden büyük veya eşit olan tüm köyleri gösterir.                                   |
| maxPopulation       | number | Nüfusu girdiğiniz değerden küçük veya eşit olan tüm köyleri gösterir.                                   |
| provinceId          | number | Belirli bir ile ait köyleri gösterir. Bu parametre, il ID'si ile filtreleme yapar.                      |
| province            | string | Belirli bir ile ait köyleri gösterir. Bu parametre, il adını kullanır.                                  |
| districtId          | number | Belirli bir ilçeye ait köyleri gösterir. Bu parametre, ilçe ID'si ile filtreleme yapar.                 |
| district            | string | Belirli bir ilçeye ait köyleri gösterir. Bu parametre, ilçe adını kullanır.                             |
| offset              | number | Kaçıncı kayıttan başlayacağını belirler. Varsayılan değer 0'dır.                                        |
| limit               | number | Kaç kayıt alınacağını belirler. Varsayılan değer 10'dur.                                                |
| fields              | string | Alınacak alanları belirler. Örneğin, `fields=id,name,population` ile ID, isim ve nüfus alanlarını alır. |
| sort                | string | Hangi alana göre sıralanacağını belirler. Örneğin, `sort=name` ile isim alanına göre sıralar.           |

`/villages/{id}` için:

| Path Değişkeni | Açıklama                     |
| -------------- | ---------------------------- |
| id             | Alınmak istenen köyün ID'si. |

| Sorgu Parametreleri | Tip    | Açıklama                                                                                                |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------- |
| fields              | string | Alınacak alanları belirler. Örneğin, `fields=id,name,population` ile ID, isim ve nüfus alanlarını alır. |
