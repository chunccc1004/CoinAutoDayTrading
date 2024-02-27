from io import StringIO

import pandas as pd
import requests
from pandas import DataFrame
from selenium.webdriver.remote.webelement import WebElement

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


# 거래 대금 순 마켓 load하는 함수
def get_market_list():
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from chromedriver_py import binary_path
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By

    print("마켓 리스트 검색 시작")

    # 접속
    options = Options()
    options.add_argument("headless")

    driver = webdriver.Chrome(options=options, service=Service(executable_path=binary_path))
    driver.get("https://upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC")

    xpath_table = '//*[@id="UpbitLayout"]/div[3]/div/section[2]/article/span[2]/div/div/div[1]/table'
    xpath_scroll_div = '//*[@id="UpbitLayout"]/div[3]/div/section[2]/article/span[2]/div/div/div[1]'

    # table 읽고 정리
    table = driver.find_element(By.XPATH, xpath_table)
    # tbody
    tbody = table.find_element(By.TAG_NAME, "tbody")
    # tbody > tr > td
    data_list = []
    is_added, data_list = _collect_data(data_list, tbody)
    # scroll div
    scroll_div = driver.find_element(By.XPATH, xpath_scroll_div)

    # 스크롤을 아래로 내리기 (가상 스크롤링)
    while is_added:  # 예시로 3번 스크롤링
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_div)
        time.sleep(0.1)  # 스크롤 후 로딩을 위한 대기
        is_added, data_list = _collect_data(data_list, tbody)

    data_list = list(
        map(lambda x: {'market': _market_code_translation(x[2]), 'volume': float(x[5].replace('백만', '').replace(',', '')) * 1000000}, data_list))
    for tmp in data_list:
        print(tmp)

    time.sleep(1000)


# market code api에 맞게 수정하는 함수
def _market_code_translation(market: str):
    market = market.split('\n')[1].split('/')
    return f'{market[1]}-{market[0]}'


# table에서 데이터 수집하는 함수
def _collect_data(data_list: list, tbody: WebElement):
    from selenium.webdriver.common.by import By

    is_added = False
    for tr in tbody.find_elements(By.TAG_NAME, "tr"):
        td_datas = []
        for td in tr.find_elements(By.TAG_NAME, "td"):
            td_datas.append(td.get_attribute("innerText"))
        if td_datas == [] or td_datas in data_list:
            pass
        else:
            data_list.append(td_datas)
            is_added = True
    return is_added, data_list
