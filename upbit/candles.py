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


def _get_candle_data(url: str) -> DataFrame:
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return pd.read_json(StringIO(response.text))
