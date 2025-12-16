---
outline: deep
---

# Anahtar Kavramlar

Bu bölümde, TurkiyeAPI'nin temel kavramlarını ve terminolojisini açıklamaktayız. Bu kavramlar, API'yi kullanırken karşılaşacağınız terimlerdir ve bu terimlerin anlamını anlamanız, API'yi daha iyi kullanmanıza yardımcı olacaktır.

## Path Değişkenleri

API'de kullanılan path değişkenleri aşağıdaki gibidir:

- `:provinceId`: İl kimlik numarası (ID'si)
- `:districtId`: İlçe kimlik numarası (ID'si)
- `:neighborhoodId`: Mahalle kimlik numarası (ID'si)
- `:villageId`: Köy kimlik numarası (ID'si)

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

::: warning UYARI
Path değişkenleri için girmeniz gereken değerler sayı cinsinden olmalıdır. Aksi takdirde, API size `404` kodlu bir hata mesajı döndürecektir.
:::

::: danger ÖRNEK HATA

```plaintext
GET /v1/provinces/istanbul
```

Yukarıdaki örnekte, `:provinceId` için `istanbul` değeri bir **sayı olmadığı** için **geçersiz** bir değerdir _(böyle bir il olsa bile)_ ve API size `404` kodlu bir hata mesajı döndürecektir.

```json {3}
{
  "status": "ERROR",
  "message": "Invalid province ID. The id parameter must be a number."
}
```

:::

## Sorgu Parametreleri

API'de kullanılan sorgu parametreleri aşağıdaki gibidir:

- Hangi alanlara göre filtreleme yapılacağını belirlemek için (en yaygın kullanılanlar):
  - `name`: İsim
  - `minPopulation`: Minimum nüfus
  - `maxPopulation`: Maksimum nüfus
  - `minArea`: Minimum yüzölçümü
  - `maxArea`: Maksimum yüzölçümü
  - `isMetropolitan`: Büyükşehir olup olmadığı
  - _ve daha fazlası..._
- `offset`: Kaçıncı kayıttan başlayacağını belirler
- `limit`: Kaç kayıt alınacağını belirler
- `fields`: Hangi alanların alınacağını belirler
- `sort`: Hangi alana göre sıralanacağını belirler

::: details ÖRNEK {open}

İçerisinde `a` harfi geçen illeri isimlerine göre sıralayarak, sadece `id` ve `name` (isim) alanlarını almak ve ilk 10 il için aşağıdaki gibi bir sorgu yapabilirsiniz:

```plaintext
GET /v1/provinces?name=a&offset=0&limit=10&fields=id,name&sort=name
```

Çıkış:

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

::: tip İPUCU

Azalan sıralama yapmak için `sort` (sıralama) alanının başına `-` işareti ekleyebilirsiniz:

:::

::: details ÖRNEK {open}

İsimlerine göre azalan sıralama yapmak için aşağıdaki gibi bir sorgu yapabilirsiniz:

```plaintext
GET /v1/provinces?fields=id,name&sort=-name
```

Çıkış:

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
    // ... 56 il daha
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

::: tip İPUCU

Birden fazla alana göre sıralama yapmak için sıralama alanlarını virgülle ayırabilirsiniz.

:::

::: details ÖRNEK {open}

Bağlı oldukları illerin isimlerine göre ve nüfuslarına göre sıralama yapmak için aşağıdaki gibi bir sorgu yapabilirsiniz (önce `province` (il) değerine göre, sonra `population` (nüfus) değerine göre sıralama yapar):

```plaintext
GET /v1/districts?fields=name,province,population&sort=province,population
```

Çıkış:

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
