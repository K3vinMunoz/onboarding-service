import os
import hmac
import hashlib
from dotenv import load_dotenv

load_dotenv()

PEPPER = os.getenv("API_KEY_PEPPER")
if not PEPPER:
    raise RuntimeError("API_KEY_PEPPER no está definido en .env")

def hash_api_key(api_key: str) -> str:
    return hmac.new(
        key=PEPPER.encode("utf-8"),
        msg=api_key.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
