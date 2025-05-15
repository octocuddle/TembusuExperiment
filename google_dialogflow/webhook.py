from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.post("/webhook")
async def dialogflow_webhook(request: Request):
    body = await request.json()
    parameters = body.get("queryResult", {}).get("parameters", {})
    intent = body.get("queryResult", {}).get("intent", {}).get("displayName", "")
    session = body.get("session")

    print(f'[Webhook] intent: {intent}')
    print(f'[Webhook] parameters: {parameters}')

    if intent == "borrow - authentication":
        return await handle_borrow_authentication(parameters, session)
    
    if intent == "borrow - authentication - qr":
        return await handle_qr_submission(parameters)

async def handle_borrow_authentication(params, session):
    matric = params.get("MatricNum")
    email = params.get("emailAdd")
    VALID_MATRIC = "A1234567X"
    VALID_EMAIL = "john@example.com"

    if matric == VALID_MATRIC and email == VALID_EMAIL:
        return {
            "fulfillmentText": "✅ Matric and email valid. Please upload your book QR code.",
            "outputContexts": [
                {
                    "name": f"{session}/contexts/awaiting_borrow_qr",
                    "lifespanCount": 2
                }
            ]
        }
    return {
        "fulfillmentText": "❌ Invalid matric or email. Please provide your matriculation number and email address correctly."
    }

async def handle_qr_submission(params):
    qr = params.get("QRcode")
    if qr:
        return {"fulfillmentText": f"✅ QR code received: {qr}. Proceeding with book borrowing..."}
    return {"fulfillmentText": "❌ Could not process QR code. Please try again."}
