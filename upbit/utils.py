from selenium.webdriver.remote.webelement import WebElement


def find_trading_market():
    a = 1


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
