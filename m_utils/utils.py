import time

from selenium.webdriver.remote.webelement import WebElement

from upbit import get_15m_candle_datas


# upbit
# 5분봉 3틱
def find_trading_market() -> list:
    market_list = _get_market_list()
    trading_market_list = []
    cnt_is_big = 0
    cnt_not_big = 0

    for market in market_list:
        print(f"진행 중 ({cnt_is_big + cnt_not_big}/{len(market_list)})")
        time.sleep(0.05)
        if _is_big_volume(market['market']):
            trading_market_list.append(market)
            cnt_is_big += 1
        else:
            cnt_not_big += 1
    print(f"만족 : {cnt_is_big}\n탈락 : {cnt_not_big}")

    return trading_market_list


# 거래 대금 순 마켓 load하는 함수
def _get_market_list() -> list:
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
    print(f"확인할 마켓 수 : {len(data_list)}")
    # scroll div
    scroll_div = driver.find_element(By.XPATH, xpath_scroll_div)

    # 스크롤을 아래로 내리기 (가상 스크롤링)
    while is_added:  # 예시로 3번 스크롤링
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_div)
        time.sleep(0.2)  # 스크롤 후 로딩을 위한 대기
        is_added, data_list = _collect_data(data_list, tbody)
        print(f"확인할 마켓 수 : {len(data_list)}")

    data_list = list(
        map(lambda x: {'market': _market_code_translation(x[2]), 'volume': float(x[5].replace('백만', '').replace(',', '')) * 1000000}, data_list))

    print("마켓 리스트 검색 완료")

    return data_list


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
        if not td_datas:
            continue
        elif td_datas[2] in [x[2] for x in data_list]:
            continue
        else:
            data_list.append(td_datas)
            is_added = True
    return is_added, data_list


# 현재 거래량이 몰려있는지 확인하는 코드
# 조건
# 1. 15분 봉으로 확인
# 2. 현재 봉부터 이전의 봉 2개까지 확인
# 3. 너무 작은 크기이면 어떻게 판단할 것인지 중요 -> 이전 가장 큰 값의 40%는 되는 값이어야 하는 것으로 하자
# 4. 확인하는 봉의 크기가 이전 봉보다 2배 이상 큰 경우로 감
def _is_big_volume(market: str) -> bool:
    df = get_15m_candle_datas(market)
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
                return True
            else:
                continue
    return False
