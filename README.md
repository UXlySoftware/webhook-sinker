
[![Watch the tutorial](https://img.youtube.com/vi/UYWcTV2FwVo/maxresdefault.jpg)](https://youtu.be/UYWcTV2FwVo)

# Webhook Sinker

This tiny repo implements a docker stack for locally testing webhooks. It uses [ngrok](https://ngrok.com) to establish an introspective
tunnel from you local machine to a static public URL which you can use for testing [1Shot API](https://1shotapi.com) webhook callbacks. 

Checkout the [1Shot Docs](https://docs.1shotapi.com/transactions.html#webhooks) for more details on webhooks and also the official [1Shot Python sdk](https://pypi.org/project/uxly-1shot-client/).

> [!IMPORTANT] 
> Be sure to go to the [Escrow Wallets](https://app.1shotapi.com/escrow-wallets) tab in 1Shot API and create an escrow wallet for Sepolia Network and fund it with some testnet funds (try using Google's [Sepolia Testnet Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)).

## 1. Ngrok Setup

First, make a free account at [ngrok.com](https://ngrok.com) and grab your auth token from the [ngrok dashboard](https://dashboard.ngrok.com/endpoints) and input it in the [`docker-compose.env`](./docker-compose.env) for the `NGROK_AUTHTOKEN` variable.

Also, create a static cloud endpoint by going to the [Domains tab](https://dashboard.ngrok.com/domains) to register a free static URL address. 
Put the endpoint url (including `https://`) into the `docker-compose.env` file for the `TUNNEL_BASE_URL` variable.

## 2. Get your 1Shot API Credentials 

Log into [1Shot API](https://app.1shotapi.com), if it is your first time it will prompt you to create an organization. Go to your organization's [details page](https://app.1shotapi.com/organizations) and get your Organzation ID to input into [`docker-compose.env`](/docker-compose.env) in the `ONESHOT_BUSINESS_ID` variable.

On the [API Keys](https://app.1shotapi.com/api-keys) page, create a new API key and secret and input them into the [`docker-compose.env`](/docker-compose.env) file for the `ONESHOT_API_KEY` and `ONESHOT_API_SECRET`. 

### 3. Run the Demo Stack

First, build the webhook demo service:

```sh
docker compose build fastapi-service
```

Now bring up the Docker stack:

```
docker compose --env-file docker-compose.env up -d
```

You can open [http://localhost:4040](http://localhost:4040) to see HTTP calls arriving at your stack. 

If you go to the ["My Endpoints"](https://app.1shotapi.com/endpoints) page in 1Shot API, you should see and new endpoint created for you called "1Shot Webhook Demo". 

> [!NOTE] 
> You can stop the demo by running `docker compose down`

## 4. Trigger the Transaction Endpoint

On the details page of the "1Shot Webhook Demo" transaction endpoint, enter a recipient address and an amount and click "Execute" in the upper right-hand corner. Watch the [ngrok agent dashboard](http://localhost:4040) for callbacks from 1Shot. You should see a `200 OK` message in a few seconds on the `/python` route. 