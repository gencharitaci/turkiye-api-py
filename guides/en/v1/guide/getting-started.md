---
outline: deep
---

# Getting Started

Depending on your needs and what you want to build, you can use TurkiyeAPI in different ways. This guide explains how to start using the API step-by-step.

If you're working on a personal or non-critical project, you can use the API directly via `api.turkiyeapi.dev`. However, if you want more control and customization—especially for commercial use—we recommend running the API on your own server. This approach offers better security and scalability for your project.

<!-- [Read more](./faq.md) -->

## Fair Use Policy

TurkiyeAPI is available for everyone and does not require authentication. That said, we kindly ask you to use the API fairly and responsibly. Abusing the service, making excessive requests, or intentionally disrupting access can negatively affect other users and degrade the overall quality of service.

### API Rate Limiting Policy

- Each IP address is limited to **150 requests per 15 minutes**.
- If you exceed this limit, you’ll receive a `429 - Too Many Requests` error.
- You can resume making requests once the cooldown period has passed.

```plaintext
Too many requests from this IP, please try again in 15 minutes!
```

Staying within these limits helps ensure that everyone can benefit from the service.

## Using the API

```url
https://api.turkiyeapi.dev/v1/
```

The URL above is the main entry point to the API. You can use it to interact with the service and retrieve data.

Here are a few code examples that demonstrate how to make a `GET` request:

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

::: warning WARNING
The `curl` command may not work in Windows PowerShell. In that case, use `Invoke-WebRequest` instead:

```powershell
Invoke-WebRequest -Uri 'https://api.turkiyeapi.dev/v1/' -Method GET
```

:::

If your request is successful, the API will return a response like this, with status code `200`:

```json
{
  "status": "OK",
  "message": "Welcome to the TurkiyeAPI"
}
```

## Running the API Locally

To run the API locally, you need to have [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) installed.

Follow these steps to set up the API on your own server:

0. Choose a directory and navigate into it:

```bash
cd /path/to/your/directory
```

1. Clone the source code from GitHub:

```bash
git clone https://github.com/ubeydeozdmr/turkiye-api.git
```

2. Install the project dependencies:

```bash
cd turkiye-api
npm install
```

3. By default, TurkiyeAPI runs on port `8181`. To start the API:

```bash
npm start
```

4. Once the API is running, you’ll see an output like this in your terminal:

```bash
TurkiyeAPI is running at http://localhost:8181
```

5. You can now access the API via your browser or an API testing tool:

```url
http://localhost:8181/v1/
```

## Environment Variables

You can customize certain aspects of the API using environment variables. These variables allow you to modify the behavior and configuration of the API.

For example, to change the port number or the environment mode, set the following:

```env
PORT=8181
NODE_ENV=development
```

You can set environment variables in the terminal like this:

::: code-group

```bash [Windows CMD]
# Set environment variables and start the API
set PORT=8181 && set NODE_ENV=development && npm start
```

```bash [MacOS/Linux]
# Set environment variables and start the API
export PORT=8181 && export NODE_ENV=development && npm start
```

:::

Alternatively, you can create a `.env` file in the project root and add the variables there.
