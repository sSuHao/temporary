import json
import hmac
import hashlib
import base64
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# set key and secret
api_key = "pastekeyhere"
api_key_secret = "pastesecretkeyhere"

# prepare header and payload

header = {
    "typ": "JWT",
    "alg": "HS256", # only support HS256
    "cty": "stringee-api;v=1"
}

payload = {
    'jti': api_key + '-' + str(int(time.time())),
    "iss": api_key, # API key sid
    "exp": int(time.time()) + 1800, # expiration time
    "rest_api": True
}

# encode header and payload
encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode('utf-8')).decode('utf-8').rstrip("=")
encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8').rstrip("=")

# prepare signature
signature = hmac.new(api_key_secret.encode('utf-8'), msg=(encoded_header + "." + encoded_payload).encode('utf-8'), digestmod=hashlib.sha256).digest()
encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip("=")

# generate final JWT token string
jwt_token = encoded_header + "." + encoded_payload + "." + encoded_signature

headers = {
    'X-STRINGEE-AUTH': jwt_token,
    'Content-Type': 'application/x-www-form-urlencoded',
}

def make_request(data):
    response = requests.post('https://api.stringee.com/v1/call2/callout', headers=headers, data=data)
    print(response.text)

data_list = [
    '{"from": {"type": "external","number": "sotongdai","alias": "sotongdai"},"to": [{"type": "external","number": "songuoinhan","alias": "songuoinhan"}]}'
]

# Goi dong thoi toi da duoc 4 so 1 luc
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(make_request, data_list)
