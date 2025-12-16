---
outline: deep
---

# API Structure

TurkiyeAPI has the following API structure for version v1:

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

In summary, there are four main resources:

- **Provinces** (`/provinces`)
- **Districts** (`/districts`)
- **Neighborhoods** (`/neighborhoods`)
- **Villages** (`/villages`)

Each resource accepts a URL parameter with its unique ID to retrieve detailed information via a `GET` request. For example, to fetch the details of a specific district, you can use a URL like `/districts/1832`.

To retrieve all entries of a given resource, you only need to use the root path of that resource. For example, to get a list of all provinces, you can use the endpoint `/provinces`.

::: info INFO
TurkiyeAPI only supports `GET` requests. Other HTTP methods are not allowed. If a different request method is used, the API will respond with a `405` error code:

```json {3}
{
  "status": "ERROR",
  "message": "Method not allowed."
}
```

:::

::: info INFO
If you send a request to an undefined endpoint under `/v1`, the API will respond with a `404` error code:

```json {3}
{
  "status": "ERROR",
  "message": "Wrong endpoint."
}
```

:::
