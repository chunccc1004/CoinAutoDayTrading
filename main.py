import time

import m_binance
import db
import upbit
import m_utils

if __name__ == "__main__":
    # upbit.chance()
    # db_trading = db.Database("trading")
    # # db_trading.bid_history_insert("test", "100", "100")
    # # last = db_trading.select_last_pk("bid", "test")
    # # print(last)
    #
    # average = db_trading.break_even_calculate("test")
    # print(average)
    # print(m_utils.find_trading_market())
    # while True:
    #     print(binance.Api().present_price())
    #     time.sleep(1)
    binance = m_binance.Api().binance
    symbol = "BTC/USDT"
    long_target, short_target = m_utils.cal_target(binance, symbol)
    balance = binance.fetch_balance()
    usdt = balance['total']['USDT']
    op_mode = False
    position = {
        "type": None,
        "amount": 0
    }

    ticker = binance.fetch_ticker(symbol)
    cur_price = ticker['last']

    amount = m_utils.cal_amount(usdt, cur_price)
    print(usdt)
    print(cur_price)
    print(amount)
