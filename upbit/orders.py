# 마켓별 주문 가능 정보 확인
def order(order_type: str, price: str, volume: str):
    import jwt
    import hashlib
    import os
    import requests
    import uuid
    from urllib.parse import urlencode, unquote

    access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
    secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
    server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

    if order_type == "bid":  # 매수 -> price 필수
        params = {
            'market': 'KRW-BTC',
            'side': order_type,
            'ord_type': 'limit',
            'price': price,
        }
    else:  # 매도 -> volume 필수
        params = {
            'market': 'KRW-BTC',
            'side': order_type,
            'ord_type': 'limit',
            'volume ': volume,
        }
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }

    res = requests.post(server_url + '/v1/orders', json=params, headers=headers)
    res.json()
