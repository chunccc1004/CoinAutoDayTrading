# Private 데이터를 수신하기 위해서는 Websocket 연결 시 인증
def read_all_assets():
    import jwt
    import os
    import requests
    import uuid
    from dotenv import load_dotenv

    load_dotenv()
    access_key = os.environ.get('UPBIT_OPEN_API_ACCESS_KEY')
    secret_key = os.environ.get('UPBIT_OPEN_API_SECRET_KEY')
    server_url = os.environ.get('UPBIT_OPEN_API_SERVER_URL')

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
        'Authorization': authorization,
    }
    params=""

    res = requests.get(server_url + '/v1/accounts', params=params, headers=headers)
    print(res.json())
