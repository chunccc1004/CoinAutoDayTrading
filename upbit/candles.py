from io import StringIO

import pandas as pd
import requests
from pandas import DataFrame

CANDLE_BASE_URL = "https://api.upbit.com/v1/candles/"


def get_5m_candle_datas(market: str) -> DataFrame:
    url = f"{CANDLE_BASE_URL}minutes/5?market={market}&count=100"
    return _get_candle_data(url)


def get_15m_candle_datas(market: str) -> DataFrame:
    url = f"{CANDLE_BASE_URL}minutes/15?market={market}&count=100"
    return _get_candle_data(url)


def get_1h_candle_datas(market: str) -> DataFrame:
    url = f"{CANDLE_BASE_URL}minutes/60?market={market}&count=100"
    return _get_candle_data(url)


def get_4h_candle_datas(market: str) -> DataFrame:
    url = f"{CANDLE_BASE_URL}minutes/240?market={market}&count=100"
    return _get_candle_data(url)


# 현재 거래량이 몰려있는지 확인하는 코드
# 조건
# 1. 15분 봉으로 확인
# 2. 현재 봉부터 이전의 봉 2개까지 확인
# 3. 너무 작은 크기이면 어떻게 판단할 것인지 중요 -> 이전 가장 큰 값의 40%는 되는 값이어야 하는 것으로 하자
# 4. 확인하는 봉의 크기가 이전 봉보다 2배 이상 큰 경우로 감
def is_big_volume(market: str) -> bool:
    df = get_15m_candle_datas(market)
    print(df['candle_acc_trade_volume'])
    volume_data = df['candle_acc_trade_volume']
    check_bar_cnt = 3

    # 조건 3 확인
    check_range_volume_data = volume_data.head(check_bar_cnt)
    max_val = volume_data.max()
    if any(check_range_volume_data >= max_val * 0.4):
        # 조건 4 진입
        for i in range(0, check_bar_cnt):
            check_bar = volume_data[i]
            pre_bar = volume_data[i + 1]

            if check_bar >= pre_bar * 2:
                print(True)
                return True
            else:
                print(f"check_bar : {check_bar}\npre_bar : {pre_bar}\nratio : {pre_bar / check_bar}")
    return False


def _get_candle_data(url: str) -> DataFrame:
    headers = {"accept": "application/json"}
    return pd.read_json(StringIO(requests.get(url, headers=headers).text))
