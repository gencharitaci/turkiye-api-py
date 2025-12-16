---
outline: deep
---

# Beldeler

Varsayılan olarak API, bütün beldeleri önce bağlı oldukları illere göre, sonra bağlı oldukları ilçelere göre, ardından da adlarına göre listeler.

::: info BİLGİ
TurkiyeAPI'nin v1 versiyonunun kapsamı (belediye birimleri olmadan) illeri, ilçeleri, mahalleleri ve köyleri içerecek şekildedir. Ancak beldeler (bir belediye türü) ülkede önemli bir yere sahip olduğu için onlara da tıpkı mahalle ve köyler gibi iki rota ayrılmıştır. Kısacası bu v1 için hazırlanmış bir yamadır. Ancak mahalle ve köylerden farklı olarak `/districts/:id` rotasında gösterilmezler, yani kendi içlerinde izole edilmişlerdir. Yine de `/districts` ile başlayan bu rotalarda ilçelerin bağlı olduğu il-ilçe isimleri ve ID'leri belirtilmiştir, yani dilerseniz bunları kullanarak bağlantı kurabilirsiniz.
:::

::: warning UYARI
v2 versiyonunda bu rotalar muhtemelen kaldırılacak, yerine belediye odaklı rotalar gelecek.
:::

Beldeler için giriş URL'si: `/v1/towns` şeklindedir.

## Belde Özellikleri

Belde kaynakları, aşağıdaki özelliklere sahiptir:

- `provinceId`: Beldenin bağlı olduğu il ID'si
- `districtId`: Beldenin bağlı olduğu ilçe ID'si
- `id`: Beldenin ID'si
- `province`: Beldenin bağlı olduğu il adı
- `district`: Beldenin bağlı olduğu ilçe adı
- `name`: Beldenin adı
- `population`: Beldenin nüfusu

## Birden Fazla Belde Verilerini Almak

Bütün beldeleri almak için, yalnızca belde URL'sini kullanmanız yeterlidir. Örneğin, bütün beldeleri almak için `/v1/towns` gibi bir URL kullanabilirsiniz.

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

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir:

::: details Örnek Yanıt {open}

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
    // Diğer beldeler...
  ]
}
```

:::

## Tek Bir Belde Verisini Almak

Tek bir belde verisini almak için, belde ID'sini kullanarak aşağıdaki gibi bir istek yapabilirsiniz:

```url
https://api.turkiyeapi.dev/v1/towns/:id
```

Burada `:id` kısmını almak istediğiniz beldenin ID'si ile değiştirmelisiniz.

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

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir:

::: details Örnek Yanıt {open}

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

## Sorgulama

API'de sorgulama yapmak için, URL'ye sorgu parametreleri ekleyebilirsiniz. Örneğin, belirli bir ildeki beldeleri almak için `provinceId` parametresini kullanabilirsiniz.

::: info BİLGİ
Bununla ilgili örnekler için [Örnek API Çağrıları](./examples.md) sayfasını ziyaret edebilirsiniz.
:::

`/towns` için:

| Sorgu Parametreleri | Tip    | Açıklama                                                                                                |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------- |
| name                | string | Arama sorgunuzu içeren veya eşleşen tüm beldeleri gösterir.                                             |
| minPopulation       | number | Nüfusu girdiğiniz değerden büyük veya eşit olan tüm beldeleri gösterir.                                 |
| maxPopulation       | number | Nüfusu girdiğiniz değerden küçük veya eşit olan tüm beldeleri gösterir.                                 |
| provinceId          | number | Belirli bir ile ait beldeleri gösterir. Bu parametre, il ID'si ile filtreleme yapar.                    |
| province            | string | Belirli bir ile ait beldeleri gösterir. Bu parametre, il adını kullanır.                                |
| districtId          | number | Belirli bir ilçeye ait beldeleri gösterir. Bu parametre, ilçe ID'si ile filtreleme yapar.               |
| district            | string | Belirli bir ilçeye ait beldeleri gösterir. Bu parametre, ilçe adını kullanır.                           |
| offset              | number | Kaçıncı kayıttan başlayacağını belirler. Varsayılan değer 0'dır.                                        |
| limit               | number | Kaç kayıt alınacağını belirler. Varsayılan değer 10'dur.                                                |
| fields              | string | Alınacak alanları belirler. Örneğin, `fields=id,name,population` ile ID, isim ve nüfus alanlarını alır. |
| sort                | string | Hangi alana göre sıralanacağını belirler. Örneğin, `sort=name` ile isim alanına göre sıralar.           |

`/towns/{id}` için:

| Path Değişkeni | Açıklama                        |
| -------------- | ------------------------------- |
| id             | Alınmak istenen beldenin ID'si. |

| Sorgu Parametreleri | Tip    | Açıklama                                                                                                |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------- |
| fields              | string | Alınacak alanları belirler. Örneğin, `fields=id,name,population` ile ID, isim ve nüfus alanlarını alır. |
