import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, Depends

from uxly_1shot_client import verify_webhook

# we import the async 1Shot client from the oneshot.py file as a singleton
from oneshot import oneshot_client, BUSINESS_ID

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# read our static url from the environment
CALLBACK_URL = os.getenv("TUNNEL_BASE_URL") + "/1shot"

# example of a wrapper class to handle webhook verification with FastAPI
# you could make a call in here to a database to look up the public key based on the content of body["data"]["transactionId"]
class webhookAuthenticator:
    def __init__(self, pubkey_b64: str):
        try:
            self.public_key = pubkey_b64
        except ValueError as e:
            print(f"Error: {e}")

    async def __call__(self, request: Request):
        try:
            # Extract the required fields from the request
            body = await request.json()  # Raw request body
            signature = body.pop("signature", None)  # Example header name

            if not signature:
                raise HTTPException(status_code=400, detail="Signature field missing")

            # Verify the signature
            is_valid = verify_webhook(
                body=body,
                signature=signature,
                public_key=self.public_key
            )

            if not is_valid:
                raise HTTPException(status_code=403, detail="Invalid signature")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal error: {e}")

# for convenience, we are going to automaically create an endoint when we start the FastAPI server
# on restarts, we will check if the endpoint exists and if it does, we will skip creating it
# this will save us the hassle of having to create it manually
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event to check for or create a demo 1Shot API transaction endpoint."""
    # lets start by checking that we have an escrow wallet provisioned for our account on the Sepolia network
    # if not we will exit since we must have one to continue
    wallets = await oneshot_client.wallets.list(BUSINESS_ID, {"chain_id": "11155111"})
    logger.info(f"Wallet balance: {float(wallets.response[0].account_balance_details.balance)}")
    if not ((len(wallets.response) >= 1) and (float(wallets.response[0].account_balance_details.balance) > 0.0001)):
        raise RuntimeError(
            "Escrow wallet not provisioned or insufficient balance on the Sepolia network. "
            "Please ensure an escrow wallet exists and has sufficient funds by logging into https://app.1shotapi.dev/escrow-wallets."
        )
    else:
        logger.info("Escrow wallet is provisioned and has sufficient funds.")

    # to keep this demo self contained, we are going to check our 1Shot API account for an existing transaction endpoint for the 
    # contract at 0x17Ed2c50596E1C74175F905918dEd2d2042b87f3 on the Sepolia network, if we don't have one, we'll create it automatically
    # then we'll use that endpoint in the conversation flow to deploy tokens from a Telegram conversation
    # for a more serious application you will probably create your required contract function endpoints ahead of time
    # and input their transaction ids as environment variables
    transaction_endpoints = await oneshot_client.transactions.list(
        business_id=BUSINESS_ID,
        params={"chain_id": "11155111", "name": "1Shot Webhook Demo"}
    )
    if len(transaction_endpoints.response) == 0:
        logger.info("Creating new transaction endpoint for webhook demo.")
        endpoint_payload = {
            "chain": "11155111",
            "contractAddress": "0x17Ed2c50596E1C74175F905918dEd2d2042b87f3",
            "escrowWalletId": wallets.response[0].id,
            "name": "1Shot Webhook Demo",
            "description": "This mints some tokens on a predeployed ERC20 contract on the Sepolia Network.",
            "callbackUrl": f"{CALLBACK_URL}", # this will register our ngrok static url as the callback url for the transaction endpoint
            "stateMutability": "nonpayable",
            "functionName": "mint",
            "inputs": [
                {
                    "name": "to",
                    "type": "address",
                    "index": 0,
                },
                {
                    "name": "amount",
                    "type": "uint",
                    "index": 1
                }
            ],
            "outputs": []
        }
        transaction_endpoint = await oneshot_client.transactions.create(
            business_id=BUSINESS_ID,
            params=endpoint_payload
        )
        app.state.myWebhook = webhookAuthenticator(transaction_endpoint.public_key)
    else:
        app.state.myWebhook = webhookAuthenticator(transaction_endpoints.response[0].public_key)
        logger.info(f"Transaction endpoint already exists, skipping creation.")

    yield

# create the FastAPI app and register the lifespan event
app = FastAPI(lifespan=lifespan)

@app.post("/1shot", dependencies=[Depends(lambda: app.state.myWebhook)])
async def handle_python_webhook(request: Request):
    return {"message": "Webhook received and signature verified"}

@app.get('/healthcheck')
async def root():
    return {'message': 'webhook sinker is up!'}
