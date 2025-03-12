from fastapi import FastAPI, Request, HTTPException, Depends
import json
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

app = FastAPI()

async def verify_signature_decorator(request: Request):
    try:
        # Extract the required fields from the request
        body = await request.json()  # Raw request body
        signature = body.pop("signature", None)  # Example header name
        print(f"Signature: {signature}")
        
        if not signature:
            raise HTTPException(status_code=400, detail="Signature header missing")
        # Decode the signature
        signature_bytes = base64.b64decode(signature)
        
        # Public key in base64 format
        pubkey_b64 = "FL75rx0IthykeGQhoMJ+ef7aQOwRXS+PTRsICqSxq3A="
        # Load the public key
        public_key = Ed25519PublicKey.from_public_bytes(
            base64.b64decode(pubkey_b64)
        )
        # Verify the signature
        public_key.verify(signature_bytes, json.dumps(body, separators=(',', ':'), sort_keys=True).encode('utf-8'))
    except InvalidSignature:
        raise HTTPException(status_code=403, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@app.post("/python", dependencies=[Depends(verify_signature_decorator)])
async def handle_python_webhook(request: Request):
    return {"message": "Webhook received and signature verified"}

@app.get('/healthcheck-python')
async def root():
    return {'message': 'webhook sinker is up!'}
