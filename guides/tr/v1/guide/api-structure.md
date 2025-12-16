---
outline: deep
---

# API Yapısı

TurkiyeAPI, v1 versiyonu için aşağıdaki API yapısına sahiptir:

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

Özetlemek gerekecek olursa, dört ana kaynak bulunmaktadır:

- **İller** (`/provinces`)
- **İlçeler** (`/districts`)
- **Mahalleler** (`/neighborhoods`)
- **Köyler** (`/villages`)

Her bir kaynak, ayrıntılı bilgi almak için bir `GET` isteği gönderildiğinde, ilgili kaynağın kimlik numarasıyla birlikte bir URL parametresi bekler. Örneğin, bir ilçenin ayrıntılarını almak için `/districts/1832` gibi bir URL kullanabilirsiniz.

Ancak bir kaynaktaki bütün verileri almak için, yalnızca kaynağın kök URL'sini kullanmanız yeterlidir. Örneğin, bütün illeri almak için `/provinces` gibi bir URL kullanabilirsiniz.

::: info BİLGİ
TurkiyeAPI'yi kullanırken yalnızca `GET` istekleri gönderebilirsiniz. Diğer türdeki istekler desteklenmemektedir. Aksi durumda, API size `405` kodlu bir hata mesajı döndürecektir:

```json {3}
{
  "status": "ERROR",
  "message": "Method not allowed."
}
```

:::

::: info BİLGİ
`/v1` altında API dokümantasyonunda belirtilmemiş bir URL'ye istek gönderirseniz, API size `404` kodlu bir hata mesajı döndürecektir:

```json {3}
{
  "status": "ERROR",
  "message": "Wrong endpoint."
}
```

:::
