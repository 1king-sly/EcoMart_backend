import base64
from datetime import datetime

from httpx import AsyncClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DARAJA_BASE_URL = "https://sandbox.safaricom.co.ke"
CONSUMER_KEY = os.getenv("DARAJA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("DARAJA_CONSUMER_SECRET")
SHORTCODE = os.getenv("DARAJA_SHORTCODE")
PASSKEY = os.getenv("DARAJA_PASSKEY")
CALLBACK_URL = os.getenv("DARAJA_CALLBACK_URL")



async def get_access_token() -> str:
    """Fetch access token from Daraja API."""
    async with AsyncClient() as client:
        response = await client.get(
            f"{DARAJA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            auth=(CONSUMER_KEY, CONSUMER_SECRET),
        )
        response.raise_for_status()
        return response.json().get("access_token")


async def initiate_stk_push(amount: float, phone_number: str, order_id: str) -> bool:
    """Initiate Daraja STK Push for payment."""
    access_token = await get_access_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{SHORTCODE}{PASSKEY}{timestamp}".encode()
    ).decode()

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": order_id,
        "TransactionDesc": "Payment for order",
    }

    async with AsyncClient() as client:
        response = await client.post(
            f"{DARAJA_BASE_URL}/mpesa/stkpush/v1/processrequest",
            headers={"Authorization": f"Bearer {access_token}"},
            json=payload,
        )
        response.raise_for_status()
        result = response.json()
        print(result)
        return result
