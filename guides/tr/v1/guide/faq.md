---
outline: deep
---

# Sıkça Sorulan Sorular (SSS)

Bu bölümde, kullanıcıların sıkça sorduğu soruları yanıtlayacağız.

## TurkiyeAPI Nedir?

**TurkiyeAPI**, Türkiye'nin idari bölümleri (il, ilçe, mahalle ve köyler) hakkında demografik ve coğrafi veriler sağlayan kapsamlı bir **REST API**'dir. Bu API, Türkiye'nin idari yapısını anlamak ve bu yapıya ilişkin verilere erişmek isteyen geliştiriciler ve araştırmacılar için tasarlanmıştır.

## TurkiyeAPI Nasıl Kullanılır?

TurkiyeAPI, RESTful bir API olarak tasarlanmıştır. API'yi kullanmak için HTTP istekleri göndermeniz yeterlidir. API, JSON formatında veri döndürür ve kimlik doğrulama gerektirmez. API'yi kullanmak için aşağıdaki adımları izleyebilirsiniz:

1. API URL'sini kullanarak istek gönderin. Örneğin, bütün illeri almak için `/v1/provinces` URL'sini kullanabilirsiniz.
2. İstek başarılı olduğunda, API size JSON formatında veri döndürecektir.
3. Dönen veriyi işleyerek istediğiniz bilgilere erişebilirsiniz.

## TurkiyeAPI Hangi Verileri Sağlar?

TurkiyeAPI, Türkiye'nin idari bölümleri hakkında çeşitli veriler sağlar. Bu veriler arasında şunlar bulunmaktadır:

İllerin, ilçelerin, mahallelerin ve köylerin adları, ID'leri, nüfusları, yüzölçümleri gibi demografik ve coğrafi veriler. Ayrıca, illerin bağlı olduğu bölgeler, ilçelerin bağlı olduğu iller gibi ilişkisel veriler de sağlanır.

## TurkiyeAPI'yi Nerede Bulabilirim?

TurkiyeAPI'nin kaynak kodu [GitHub](https://github.com/ubeydeozdmr/turkiye-api) adresinde bulunmaktadır. Ayrıca, API dokümantasyonu da bu repoda yer almaktadır.

## TurkiyeAPI'yi Kullanmak Ücretli mi?

Hayır, TurkiyeAPI tamamen ücretsiz ve açık kaynak kodludur. Herkes tarafından kullanılabilir. API'yi kullanmak için herhangi bir kimlik doğrulama veya abonelik gerektirmez. Bununla birlikte, API'nin geliştirilmesine destek olmak isteyen kullanıcılar [Buy Me a Coffee](https://www.buymeacoffee.com/ubeydeozdmr) üzerinden bağış yapabilirler.

## TurkiyeAPI'yi Geliştirmek İstiyorum, Nasıl Katkıda Bulunabilirim?

TurkiyeAPI'ye katkıda bulunmak isteyenler, GitHub üzerindeki [repo](https://github.com/ubeydeozdmr/turkiye-api) sayfasını ziyaret edebilirler. Burada, hata bildiriminde bulunabilir, yeni özellikler önerebilir veya doğrudan kod katkısında bulunabilirler.

## TurkiyeAPI'yi Kendi Sunucumda Çalıştırabilir Miyim?

Evet, TurkiyeAPI'yi kendi sunucunuzda çalıştırabilirsiniz. API'nin kaynak kodu açık kaynaklıdır ve istediğiniz gibi özelleştirebilir veya geliştirebilirsiniz. Kendi sunucunuzda çalıştırmak için gerekli adımları izleyerek API'yi kurabilirsiniz.

## TurkiyeAPI'nin Dokümantasyonu Neden Değişti?

TurkiyeAPI'nin dokümantasyonu, kullanıcı deneyimini iyileştirmek ve API'nin kullanımını daha anlaşılır hale getirmek amacıyla yeniden tasarlandı. Yeni dokümantasyon, hem başarılı hem de başarısız API çağrılarını detaylandırır, zengin örnek istekler sunar ve kullanıcı deneyimini iyileştirir. Bununla birlikte v2 sürümü daha detaylı ve sistemli olacağından buna uygun olarak dokümantasyon da yeniden yapılandırıldı.

## Eski Dokümantasyona Erişebilir Miyim?

Evet, eski dokümantasyona [buradan](https://api.turkiyeapi.dev/docs) erişebilirsiniz.
