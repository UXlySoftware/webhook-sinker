
[![Watch the tutorial](https://img.youtube.com/vi/UYWcTV2FwVo/maxresdefault.jpg)](https://youtu.be/UYWcTV2FwVo)

# Webhook Sinker

This tiny repo implements a docker stack for locally testing webhooks. It uses [ngrok](https://ngrok.com) to establish an introspective
tunnel from you local machine to a static public URL which you can use for testing [1Shot API](https://1shotapi.com) webhook callbacks. 

Checkout the [1Shot Docs](https://docs.1shotapi.com/basics/contract-methods.html#webhooks) for more details on webhooks and also the official [1Shot Python sdk](https://pypi.org/project/uxly-1shot-client/).

> [!IMPORTANT] 
> Be sure to go to the [Wallets](https://app.1shotapi.com/wallets) tab in 1Shot API and create a wallet for Sepolia Network and fund it with some testnet funds (try using Google's [Sepolia Testnet Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)).

## 1. Ngrok Setup

First, make a free account at [ngrok.com](https://ngrok.com) and grab your auth token from the [ngrok dashboard](https://dashboard.ngrok.com/endpoints) and input it in the [`docker-compose.env`](./docker-compose.env) for the `NGROK_AUTHTOKEN` variable.

Also, create a static cloud endpoint by going to the [Domains tab](https://dashboard.ngrok.com/domains) to register a free static URL address. 
Put the endpoint url (including `https://`) into the `docker-compose.env` file for the `TUNNEL_BASE_URL` variable.

## 2. Get your 1Shot API Credentials 

Log into [1Shot API](https://app.1shotapi.com), if it is your first time it will prompt you to create an business. Go to your business's [details page](https://app.1shotapi.com/businesses) and get your Business ID to input into [`docker-compose.env`](/docker-compose.env) in the `ONESHOT_BUSINESS_ID` variable. Your Business ID is also available in the header of the 1Shot API app.

On the [API Keys](https://app.1shotapi.com/api-keys) page, create a new API key and secret and input them into the [`docker-compose.env`](/docker-compose.env) file for the `ONESHOT_API_KEY` and `ONESHOT_API_SECRET`. 

### 3. Run the Demo Stack

First, build the webhook demo service:

```sh
docker compose build fastapi-service
```

Now bring up the Docker stack and follow the server logs:

```
docker compose --env-file docker-compose.env up -d
docker logs -f fastapi
```

The stack is set to mount the `/src/python` directory into the running container, so if you edit the code in [`/src/python/main.py`](/src/python/main.py) and save, FastAPI will reload the changes for you automatically. If you open [http://localhost:4040](http://localhost:4040) in your browser, you will see HTTP calls arriving at your stack. 

Check out the ["My Smart Contracts"](https://app.1shotapi.com/smart-contracts) page in 1Shot API, you should see and new endpoint created for you called "1Shot Webhook Demo". 

> [!NOTE] 
> You can stop the demo by running `docker compose down`

## 4. Trigger the Contract Method

On the details page of the "1Shot Webhook Demo" Contract Method, enter a recipient address and an amount and click "Execute" in the upper right-hand corner. Alternatively, you can visit the `/execute` route of your ngrok url in your browser to automatically trigger an execution. Watch the [ngrok agent dashboard](http://localhost:4040) for callbacks from 1Shot. You should see a `200 OK` message in a few seconds on the `/python` route. 