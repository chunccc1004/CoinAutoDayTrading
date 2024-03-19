import datetime
import time

import db
import m_binance
import m_utils

if __name__ == "__main__":
    db_trading = db.Database("trading")

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

    while True:
        now = datetime.datetime.now()
        ticker = binance.fetch_ticker(symbol)
        cur_price = ticker['last']
        amount = m_utils.cal_amount(usdt, cur_price)

        if now.hour == 8 and now.minute == 50 and (0 <= now.second < 10):
            if op_mode and position['type'] is not None:
                m_utils.exit_position(db_trading, binance, cur_price, symbol, position)
                op_mode = False  # 9시 까지는 다시 포지션 진입하지 않음
                print("exit_position")

        # update target price
        if now.hour == 9 and now.minute == 0 and (20 <= now.second < 30):
            long_target, short_target = m_utils.cal_target(binance, symbol)
            balance = binance.fetch_balance()
            usdt = balance['total']['USDT']
            op_mode = True
            time.sleep(10)

        if op_mode and position['type'] is None:
            m_utils.enter_position(db_trading, binance, symbol, cur_price, long_target, short_target, amount, position)

        print(now, cur_price)
        time.sleep(1)
