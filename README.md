
[![Watch the tutorial](https://img.youtube.com/vi/UYWcTV2FwVo/maxresdefault.jpg)](https://youtu.be/UYWcTV2FwVo)

# Webhook Sinker

This tiny repo implements a docker stack for locally testing webhooks. It uses [ngrok](https://ngrok.com) to establish an introspective
tunnel from you local machine to a public URL which you can use as a webhook URL for testing [1Shot API](https://1shotapi.com) webhook callbacks. 

Checkout the [1Shot Docs](https://docs.1shotapi.com/transactions.html#webhooks) for more details on webhooks and also the official [1Shot Python sdk](https://pypi.org/project/uxly-1shot-client/).

## 1. Fire Up the Docker Stack

First, may a free account at [ngrok.com](https://ngrok.com) and grab your auth token from the [ngrok dashboard](https://dashboard.ngrok.com/endpoints) and input it in the [`docker-compose.env`](./docker-compose.env).

Also, create a static cloud endpoint by going to the [Domains tab](https://dashboard.ngrok.com/domains) to register a free static URL address. 
Put the endpoint url (including `https://`) into the `docker-compose.env` file too.

Now bring up the Docker stack:

```
docker compose --env-file docker-compose.env up -d
```

You can open [http://localhost:4040](http://localhost:4040) to see HTTP calls arriving at your stack. 

## 2. Create a 1Shot Transaction Endpoint

On the [1Shot Endpoints page](https://app.1shotapi.com/endpoints), create a new endpoint. Here are some example values you can input:

- Name: Sepolia TestToken Mint
- Description: Mint free test tokens on the Sepolia Testnet
- Blockchain: Sepolia
- Webhook: You NGrok URL with the routhe `/python` appended to the end
- Contract Address: [`0x17Ed2c50596E1C74175F905918dEd2d2042b87f3`](https://sepolia.etherscan.io/address/0x17Ed2c50596E1C74175F905918dEd2d2042b87f3)
- Function Name: `mint`
    - 1st parameter: `to` type `address`
    - 2nd parameter: `amount` type `uint`

## 3. Get the Webhook Public Key

Once you've created the transaction endpoint, click on the details of the endpoint and copy the webhook's public key. Paste this in into the 
demo server's [main.py](./src/python/main.py#L38) file. The fastAPI server will hot reload. 

## 4. Trigger the Transaction Endpoint

On the details page of the transaction you created, using the Input Parameters card to execute a transaction. Watch the ngrok tunnel inspector 
for callbacks from 1Shot. You should see a `200 OK` message in a few seconds on the `/python` route. 