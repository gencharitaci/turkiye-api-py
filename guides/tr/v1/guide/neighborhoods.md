---
outline: deep
---

# Mahalleler

Türkiye'nin idari bölümleri arasında ilçelerden sonra gelen birimlerdir. Her ilçe, bir veya daha fazla mahalleye ayrılmıştır. Türkiye'de toplam 32 186 mahalle bulunmaktadır. Varsayılan olarak API, bütün mahalleleri önce bağlı oldukları illere göre, sonra bağlı oldukları ilçelere göre, ardından da adlarına göre listeler.

Mahalleler için giriş URL'si: `/v1/neighborhoods` şeklindedir.

## Mahalle Özellikleri

Mahalle kaynakları, aşağıdaki özelliklere sahiptir:

- `provinceId`: Mahallenin bağlı olduğu il ID'si
- `districtId`: Mahallenin bağlı olduğu ilçe ID'si
- `id`: Mahallenin ID'si
- `province`: Mahallenin bağlı olduğu il adı
- `district`: Mahallenin bağlı olduğu ilçe adı
- `name`: Mahallenin adı
- `population`: Mahallenin nüfusu

## Birden Fazla Mahalle Verilerini Almak

Bütün mahalleleri almak için, yalnızca mahalle URL'sini kullanmanız yeterlidir. Örneğin, bütün mahalleleri almak için `/v1/neighborhoods` gibi bir URL kullanabilirsiniz.

```url
https://api.turkiyeapi.dev/v1/neighborhoods
```

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/neighborhoods
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/neighborhoods')
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
      "districtId": 1757,
      "id": 176887,
      "province": "Adana",
      "district": "Aladağ",
      "name": "Akören",
      "population": 980
    },
    {
      "provinceId": 1,
      "districtId": 1757,
      "id": 248,
      "province": "Adana",
      "district": "Aladağ",
      "name": "Akpınar",
      "population": 654
    }
    // Diğer mahalleler...
  ]
}
```

:::

## Tek Bir Mahalle Verisini Almak

Tek bir mahalle verisini almak için, mahalle ID'sini kullanarak URL'yi şu şekilde oluşturabilirsiniz:

```url
https://api.turkiyeapi.dev/v1/neighborhoods/{id}
```

Burada `{id}` kısmını almak istediğiniz mahallenin ID'si ile değiştirmelisiniz.

```bash [curl]
curl https://api.turkiyeapi.dev/v1/neighborhoods/176887
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/neighborhoods/176887')
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
    "districtId": 1757,
    "id": 176887,
    "province": "Adana",
    "district": "Aladağ",
    "name": "Akören",
    "population": 980
  }
}
```

:::

## Sorgulama

API, mahalleleri sorgulamak için çeşitli parametreler sunar. Bu parametreler, belirli kriterlere göre mahalleleri filtrelemenizi sağlar. Örneğin, belirli bir il veya ilçeye ait mahalleleri alabilir, nüfus aralığına göre filtreleme yapabilir veya mahalle adlarına göre arama yapabilirsiniz.

::: info BİLGİ
Bununla ilgili örnekler için [Örnek API Çağrıları](./examples.md) sayfasını ziyaret edebilirsiniz.
:::

`/neighborhoods` için:

| Sorgu Parametreleri | Tip    | Açıklama                                                                                                |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------- |
| name                | string | Arama sorgunuzu içeren veya eşleşen tüm mahalleleri gösterir.                                           |
| minPopulation       | number | Nüfusu girdiğiniz değerden büyük veya eşit olan tüm mahalleleri gösterir.                               |
| maxPopulation       | number | Nüfusu girdiğiniz değerden küçük veya eşit olan tüm mahalleleri gösterir.                               |
| provinceId          | number | Belirli bir ile ait mahalleleri gösterir. Bu parametre, il ID'si ile filtreleme yapar.                  |
| province            | string | Belirli bir ile ait mahalleleri gösterir. Bu parametre, il adını kullanır.                              |
| districtId          | number | Belirli bir ilçeye ait mahalleleri gösterir. Bu parametre, ilçe ID'si ile filtreleme yapar.             |
| district            | string | Belirli bir ilçeye ait mahalleleri gösterir. Bu parametre, ilçe adını kullanır.                         |
| offset              | number | Kaçıncı kayıttan başlayacağını belirler. Varsayılan değer 0'dır.                                        |
| limit               | number | Kaç kayıt alınacağını belirler. Varsayılan değer 10'dur.                                                |
| fields              | string | Alınacak alanları belirler. Örneğin, `fields=id,name,population` ile ID, isim ve nüfus alanlarını alır. |
| sort                | string | Hangi alana göre sıralanacağını belirler. Örneğin, `sort=name` ile isim alanına göre sıralar.           |

`/neighborhoods/{id}` için:

| Path Değişkeni | Açıklama                          |
| -------------- | --------------------------------- |
| id             | Alınmak istenen mahallenin ID'si. |

| Sorgu Parametreleri | Tip    | Açıklama                                                                                                |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------- |
| fields              | string | Alınacak alanları belirler. Örneğin, `fields=id,name,population` ile ID, isim ve nüfus alanlarını alır. |
