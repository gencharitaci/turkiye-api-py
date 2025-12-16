---
outline: deep
---

# Başlarken

Gereksinimlerinize ve yapmak istediklerinize bağlı olarak TurkiyeAPI'yi farklı şekillerde kullanabilirsiniz. Bu rehber, API'yi nasıl kullanacağınızı ve nasıl başlayacağınızı adım adım açıklamaktadır.

Kendi projeleriniz için hobi amaçlı veya kritik olmayan bir işte kullanmayı düşünüyorsanız, API'yi doğrudan `api.turkiyeapi.dev` üzerinden kullanabilirsiniz. Ancak, API'yi kendi sunucunuzda çalıştırarak daha fazla kontrol ve özelleştirme seçeneğine sahip olabilirsiniz. Özellikle ticari bir proje geliştiriyorsanız, API'yi kendi sunucunuzda çalıştırmanızı öneririz. Bu, projenizin güvenliğini ve ölçeklenebilirliğini artıracaktır.

<!-- [Detaylı okuma](./sss.md) -->

## Adil Kullanım

TurkiyeAPI, herkes tarafından kullanılabilir ve kimlik doğrulama gerektirmez. Ancak, API'yi adil ve sorumlu bir şekilde kullanmanızı rica ederiz. API'yi kötüye kullanmak, aşırı kullanmak veya hizmeti engellemek, diğer kullanıcıların erişimini engelleyebilir ve hizmetin kalitesini düşürebilir.

### API'nin rate limiting politikası

- Aynı IP adresi için **15 dakika içinde 150 istek** sınırı vardır.
- Bu sınırı aşarsanız, `429 - Too Many Requests` hatası alırsınız.
- Bekleme süresi tamamlandıktan sonra tekrar erişebilirsiniz.

```plaintext
Too many requests from this IP, please try again in 15 minutes!
```

Bu sınırı aşmamak ve API'yi adil bir şekilde kullanmak, diğer kullanıcıların da hizmetten yararlanmasına olanak tanır.

## API'yi Kullanma

```url
https://api.turkiyeapi.dev/v1/
```

Yukarıda belirtilen URL, API'nin ana giriş noktasıdır. Bu URL'yi kullanarak API'ye erişebilir ve veri alışverişi yapabilirsiniz.

Örnek olarak aşağıdaki kod parçacıklarını kullanarak API'ye bir `GET` isteği gönderebilirsiniz:

::: code-group

```bash [curl]
curl https://api.turkiyeapi.dev/v1/
```

```javascript [fetch]
fetch('https://api.turkiyeapi.dev/v1/')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error('Error fetching data:', error));
```

:::

::: warning UYARI
Windows PowerShell'da `curl` komutu çalışmayabilir. Bu durumda, `Invoke-WebRequest` komutunu kullanabilirsiniz.

```powershell
Invoke-WebRequest -Uri 'https://api.turkiyeapi.dev/v1/' -Method GET
```

:::

İsteğinizin başarılı olması durumunda, API size şu şekilde bir yanıt döndürecektir, `200` durum kodu ile:

```json
{
  "status": "OK",
  "message": "Welcome to the TurkiyeAPI"
}
```

## API'yi Kendi Sunucunuzda Çalıştırma

API'yi çalıştırmak için [Node.js](https://nodejs.org/) ve [npm](https://www.npmjs.com/) yüklü olmalıdır.

API'yi kendi sunucunuzda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

0. Hangi dizinde çalıştıracağınıza karar verin ve bu dizine geçin.

```bash
cd /path/to/your/directory
```

1. API'nin kaynak kodunu GitHub'dan indirin:

```bash
git clone https://github.com/ubeydeozdmr/turkiye-api.git
```

2. API'nin bağımlılıklarını yükleyin:

```bash
cd turkiye-api
npm install
```

3. TurkiyeAPI, varsayılan olarak `8181` numaralı bir port üzerinde çalışır. API'yi çalıştırmak için aşağıdaki komutu çalıştırabilirsiniz:

```bash
npm start
```

4. API başarıyla başlatıldığında, konsolda aşağıdaki gibi bir çıktı göreceksiniz:

```bash
TurkiyeAPI is running at http://localhost:8181
```

5. API'ye tarayıcınızdan veya bir API test aracından erişebilirsiniz:

```url
http://localhost:8181/v1/
```

## Ortam Değişkenleri

API'nin bazı özelliklerini yapılandırmak için çeşitli ortam değişkenleri kullanabilirsiniz. Bu değişkenler, API'nin çalışma şeklini ve davranışını değiştirmenize olanak tanır.

Örneğin, API'nin hangi port üzerinde çalışacağını belirlemek için `PORT` ortam değişkenini kullanabilirsiniz. Aşağıdaki örnek, API'nin `8181` numaralı port üzerinde ve `development` ortamında çalışmasını sağlar:

```env
PORT=8181
NODE_ENV=development
```

Bunun için aşağıdaki komutu kullanabilirsiniz:

::: code-group

```bash [Windows CMD]
# API'yi başlatmak için ortam değişkenlerini ayarlayın ve başlatın
set PORT=8181 && set NODE_ENV=development && npm start
```

```bash [MacOS/Linux]
# API'yi başlatmak için ortam değişkenlerini ayarlayın ve başlatın
export PORT=8181 && export NODE_ENV=development && npm start
```

:::

Veya projenizin kök dizinine `.env` dosyası oluşturabilir ve bu dosyaya ortam değişkenlerini ekleyebilirsiniz.
