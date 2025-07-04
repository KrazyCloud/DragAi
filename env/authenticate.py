import jwt
from fastapi import WebSocketDisconnect
import datetime
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret") 
ALGORITHM = "HS256"

# Fix padding issue
missing_padding = len(SECRET_KEY) % 4
if missing_padding:
    SECRET_KEY += "=" * (4 - missing_padding)
    
print("Secret Key after Base 64:",SECRET_KEY)
SECRET_KEY_DECODE = base64.b64decode(SECRET_KEY)
print("Secret Key Decode after Base 64:",SECRET_KEY_DECODE)

async def authenticate_token(token: str):
    try:
        if not token or len(token.split('.')) != 3:
            raise WebSocketDisconnect("Token is malformed or incomplete")
        
        print(f'Token: {token}')
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        print("Checking the unverfied token",unverified_payload)

        exp_time = datetime.datetime.utcfromtimestamp(unverified_payload["exp"])
        current_time = datetime.datetime.utcnow()

        print(f"⏳ Token Expiration Time (UTC): {exp_time}")
        print(f"🕒 Current Time (UTC): {current_time}")

        payload = jwt.decode(token, SECRET_KEY_DECODE, algorithms=[ALGORITHM])
        print("Payload",payload)

        exp_time = datetime.datetime.utcfromtimestamp(payload["exp"])
        current_time = datetime.datetime.utcnow()
        print(f"Token Expiration Time (UTC): {exp_time}")
        print(f"Current Time (UTC): {current_time}")
        
        if current_time > exp_time:
            print("❌ Token Expired!")
            raise Exception("Token expired")

        print("✅ Token is valid")
        return payload
    
    except jwt.ExpiredSignatureError:
        raise WebSocketDisconnect("❌ Signature has expired")
    except jwt.InvalidSignatureError:
        raise WebSocketDisconnect("❌ Invalid Token Signature")
    except jwt.DecodeError:
        raise WebSocketDisconnect("Failed to decode token")
    except Exception as e:
        raise WebSocketDisconnect(f"Unknown error: {str(e)}")
