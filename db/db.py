import sqlite3
from datetime import datetime
import pandas as pd


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                                    pk INTEGER PRIMARY KEY AUTOINCREMENT,
                                    created_at DATETIME,
                                    type TEXT,
                                    coin TEXT,
                                    price REAL,
                                    volume REAL,
                                    status TEXT
                                )''')
        self.conn.commit()

    # 구매 후, 히스토리 남김
    def history_insert(self, type, coin, price, volume):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(''' INSERT INTO trades (created_at, type, coin, price, volume, status)
                                VALUES (?, ?, ?, ?, ?, 'continue')''', (created_at, type, coin, price, volume))
        self.conn.commit()

    def trade_end_update(self, coin):
        self.cursor.execute(''' UPDATE trades
                                SET status = 'end'
                                WHERE coin=? AND status = 'continue' ''', (coin,))
        self.conn.commit()

    def select_last_pk(self, trade_type, coin):
        self.cursor.execute(""" SELECT pk FROM trades 
                                WHERE type=? AND coin=?
                                ORDER BY created_at DESC 
                                LIMIT 1""", (trade_type, coin))
        last_pk = self.cursor.fetchone()
        return last_pk[0]

    def break_even_calculate(self, coin):
        total_cost = 0
        total_volume = 0

        self.cursor.execute(""" SELECT * FROM trades 
                                WHERE status='continue' AND coin=? """, (coin,))

        for trade in self.cursor.fetchall():
            total_cost += trade[4] * trade[5]
            total_volume += trade[5]

        average_cost = total_cost / total_volume
        return average_cost

    def tmp_select_all(self):
        self.cursor.execute("SELECT * FROM trades")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
