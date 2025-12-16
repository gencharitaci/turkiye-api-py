---
outline: deep
---

# İdari Yapı

Aşağıdaki idari verilerin sayıları ile ilgili bilgiler [biruni.tuik.gov.tr/medas](https://biruni.tuik.gov.tr/medas/) adresinden 2023 yılı verileri baz alınarak verilmiştir. Bu projede kullanılan verilerin kaynağı için [tıklayınız](./sources.md).

## İller

Türkiye'nin idari bölümleri arasında en üst seviyede yer alan birimlerdir. Türkiye'de toplam 81 il bulunmaktadır ve her il, bir il merkezi ile birlikte toplamda 973 ilçeye ayrılmıştır.

## İlçeler

İllerin alt birimleridir ve Türkiye'de toplam 973 ilçe bulunmaktadır. İlçeler, bir il merkezine bağlı olarak yönetilir ve her ilçe, bir veya daha fazla mahalleye ayrılmıştır. Eğer ilçenin bağlı olduğu il için `isMetropolitan` alanı `true` ise, bu ilçe büyükşehir ilçesi olarak kabul edilir ve bu ilçeye bağlı olan `villages` alanı boş bir dizidir (array). Eğer `false` ise bu ilçeye bağlı köyler olabilir.

::: info BİLGİ
Büyükşehir olmayan illerin merkezleri de ilçe olarak kabul edilir ve bu sayıya dahildir.
:::

## Mahalleler

İlçelerin alt birimleridir ve Türkiye'de toplam 32.186 mahalle bulunmaktadır. Mahalleler, bir ilçe merkezine bağlı olarak yönetilir.

## Köyler

İlçelerin alt birimleridir ve Türkiye'de toplam 18.171 köy bulunmaktadır. Köyler, bir ilçe merkezine bağlı olarak yönetilir.
