from fastapi import FastAPI, Request, HTTPException, Depends

from uxly_1shot_client import verify_webhook

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

app = FastAPI()

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

# Put your endpoint's webhook public key here:
pubkey_base64 = "fATQhEx4hUP+EOStuUv7t4T+vjsJbKWgAT4ZPMQXvQA="

myWebhook = webhookAuthenticator(pubkey_base64)

@app.post("/python", dependencies=[Depends(myWebhook)])
async def handle_python_webhook(request: Request):
    return {"message": "Webhook received and signature verified"}

@app.get('/healthcheck-python')
async def root():
    return {'message': 'webhook sinker is up!'}
