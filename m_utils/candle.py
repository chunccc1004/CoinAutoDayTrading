class Candle:
    # Candle Type
    CANDLE_TYPE_DICT: dict[str, dict[str, dict]] = {
        "single": {
            "Marubozu Lines": {
                # 장대양봉(음봉) 벽돌형 캔들 -> 긴 캔들이며, 위꼬리/아래꼬리가 없는 캔들 / 캔들의 길이가 길수록 보다 더 신뢰할 수 있는 상승(또는 하락) 신호
                "Efficiency Rank": "G+",
                "Continuation": 0.54,
                "Reversal": 0.46
            },
            "Marubozu Opening": {
                # 시가 벽돌형 캔들 -> 시가에 꼬리가 없는 양봉(또는 음봉) / 캔들의 길이가 길수록 보다 더 신뢰할 수 있는 상승(또는 하락) 신호
                "Efficiency Rank": "G",
                "Continuation": 0.53,
                "Reversal": 0.47
            },
            "Marubozu Closing": {
                # 종가 벽돌형 캔들 -> 중가에 꼬리가 없는 양봉(또는 음봉) / 캔들의 길이가 길수록 보다 더 신뢰할 수 있는 상승(또는 하락) 신호
                "Efficiency Rank": "E+",
                "Continuation": 0.52,
                "Reversal": 0.48
            },
            "Bullish Belt Holt": {
                # 상승샅바형 캔들 -> 추세하락중 발생하며, 이후 등장하는 캔들로 추가확인이 필요 / 짧은 위꼬리 붙고, 아래 꼬리 X / 캔들의 길이가 길수록 보다 더 신뢰할 수 있는 상승 신호
                "Efficiency Rank": "G+",
                "Up": 0.71,
                "Down": 0.29
            },
            "Bearish Belt Hold Line": {
                # 하락샅바형 캔들 -> 추세상승중 발생하며, 이후 등장하는 캔들로 추가확인이 필요 / 짧은 아래꼬리 붙고, 위 꼬리 X / 캔들의 길이가 길수록 보다 더 신뢰할 수 있는 하락 신호
                "Efficiency Rank": "G+",
                "Continuation": 0.54,
                "Reversal": 0.46
            },
            "Short Lines": {
                # 짧은 캔들 -> 짧은 몸통을 가지고 있고, 따라서 시가와 종가의 거리도 짧음, 가격의 변동이 거의 없음
                "Efficiency Rank": "H",
                "Continuation": 0.48,
                "Reversal": 0.52
            },
            "Long Lines": {
                # 긴 캔들 -> 몸통이 긴 또는 매우 긴 캔들 / 시가와 종가의 거리도 긺 / 가격 변동이 매우 큼을 의미 / 이전 캔들의 색과 긴 캔들의 색이 반대인 경우, 추세반전의 신호
                # 충분히 긴 또는 매우 긴 몸통의 캔들임을 확인하려면, 이전 캔들들의 평균 몸통 길이를 확인해야 함 -> 현재 캔들의 몸통은 이전 캔들의 평균 몸통보다 확실히 커야 함
                "Efficiency Rank": "C-",
                "Continuation": 0.55,
                "Reversal": 0.45
            },
            "Doji Lines": {
                # 십자형 캔들 -> 시가와 종가가 같음, 몸통이 있더라도 매우 짧음 / 위꼬리/아래꼬리가 없는 경우, 일자형 캔들
                # 추세진행중 나타나면 : (특히, 추세상 고점 또는 저점에서 나타나면) 추세의 강도가 약해진 것으로 해석 / 십자캔들이 반복되면 주가의 방향성이 없음을 의미
                # 추세상승에서 : 상승추세의 약화를 의미 /  특히, 장대양봉 후 십자캔들이 발생하면 그 다음 캔들이 주가의 방향을 결정
                # 추세하락 중의 십자캔들은 신뢰도가 조금 약함
                "Efficiency Rank": "",
                "Continuation": 0,
                "Reversal": 0
            },
            "Dragon Fly Doji": {
                # 잠자리형 캔들 -> 아래 꼬리가 긴 십자캔들
                # 추세하락중 발생 => 특히 추세상 저점에서 발생하면 추세상승 전환의 신호가 될 수 있음 / 아래꼬리의 길이가 길수록 보다 더 신뢰할 수 있는 추세상승 전환의 신호
                "Efficiency Rank": "J-",
                "Continuation": 0.50,
                "Reversal": 0.50
            },
            "Grave Stone Doji": {
                # 비석형 캔들 -> 길다른 위꼬리를 가지는 십자캔들
                # 추세상승중 발생 => 특히 추세의 고점에서 발생하면 추세하락 전환의 신호가 될 수 있음 / 위꼬리의 길이가 길수록 보다 더 신뢰할 수 있는 추세하락 전환의 신호
                "Efficiency Rank": "H",
                "Continuation": 0.49,
                "Reversal": 0.51
            },
            "Long Legged Doji": {
                # 긴꼬리 십자캔들 -> 십자캔들의 위꼬리/아래꼬리가 매우 긴 캔들
                # 긴꼬리 십자캔들은 추세보합의 신호가 될 수 있음
                # 만약 긴꼬리 십자캔들이 추세의 고점 또는 저점에서 발생하면, 추세의 반전 가능성을 의미 가능
                # 추세보합 : 가격이 일정 기간 동안 일정한 추세를 보이고 있는 동안 거래량이 감소하고 가격 변동이 크지 않은 상태
                "Efficiency Rank": "D",
                "Continuation": 0.51,
                "Reversal": 0.49
            },
            "Rickshaw Man": {
                # 중심선 십자캔들 -> 몸통이 위꼬리와 아래꼬리의 중간(halfway)에 있는 십자캔들 / 매우 긴 위꼬리/아래꼬리
                # 주가 보합의 신호가 될 수 있음
                # 주가 보합 : 특정 기간 동안 주식의 가격이 큰 폭으로 상승하거나 하락하는 대신에 상대적으로 변동 폭이 작고 일정한 수준에서 움직이는 상태
                "Efficiency Rank": "D",
                "Continuation": 0.51,
                "Reversal": 0.49
            },
            "Doji Gapping Down": {
                # 갭하락 십자캔들 -> 추세하락중 발생하며, 이후 등장하는 캔들로 추가확인이 필요
                # 이전 캔들과의 사이에 갭하락 존재 / 갭하락 후 십자캔들이 발생
                "Efficiency Rank": "I-",
                "Up": 0.56,
                "Down": 0.44
            },
            "Doji Gapping Up": {
                # 갭상승 십자캔들 -> 추세상승중 발생하며, 이후 등장하는 캔들로 추가확인이 필요
                # 이전 캔들과의 사이에 갭하락 존재 / 갭상승 후 십자캔들이 발생
                "Efficiency Rank": "J+",
                "Up": 0.43,
                "Down": 0.57
            },
            "Hammer": {
                # 망치형 캔들 -> 몸통은 짧고, 아래 꼬리가 매우 긺
                # 아래 꼬리는 몸통의 최소 두배 이상
                # 위꼬리는 없거나, 있다 해도 매우 짧아야 함
                # 일반적으로 추세 상승 전환의 신호가 될 수 있음
                # 추세하락중 발생하며, 이후 등장하는 캔들로 추가확인이 필요
                # 만약 추세의 저점에서 발생하면, 더 많은 신뢰
                # 캔들의 색깔은 중요하지 않음(양봉 음봉 모두 가능)
                # 만약 주가가 현재 캔들의 저가 아래로 떨어지면, 추세하락 연장의 확증 / 반대로 주가가 현재 캔들의 고가 위로 올라가면, 추세상승 전환의 신호가 될 수 있음
                "Efficiency Rank": "G",
                "Up": 0.60,
                "Down": 0.40
            },
            "Inverted Hammer": {
                # 역망치형 캔들 -> 몸통은 짧고, 위 꼬리가 매우 긺
                # 위 꼬리는 몸통의 최소 두배 이상
                # 아래 꼬리는 없거나, 있다 해도 매우 짧아야 함
                # 일반적으로 추세 하락 전환의 신호가 될 수 있음
                # 추세하락중 발생하며, 이후 등장하는 캔들로 추가확인이 필요
                # 만약 추세의 저점에서 발생하면, 더 많은 신뢰
                # 캔들의 색깔은 중요하지 않음(양봉 음봉 모두 가능)
                # 만약 주가가 현재 캔들의 저가 아래로 떨어지면, 추세하락 연장의 확증 / 반대로 주가가 현재 캔들의 고가 위로 올라가면, 추세상승 전환의 신호가 될 수 있음
                # 일반적으로 역망치 이전에는 긴 음봉 존재
                "Efficiency Rank": "A",
                "Up": 0.35,
                "Down": 0.65
            },
            "Hanging Man": {
                # 교수형 캔들 -> 캔들의 몸통은 짧고, 아래 꼬리가 매우 긺
                # 아래 꼬리는 몸통의 최소 두배 이상
                # 위꼬리는 없거나, 있다 해도 매우 짧아야 함
                # 일반적으로 추세하락 전환의 신호가 될 수 있음
                # 추세상승중 발생하며, 추가확인이 필요
                # 만약 추세의 고점에서 발생하면, 더욱 신뢰할 수 있는 패턴
                # 캔들의 색깔은 중요하지 않음(양봉 음봉 모두 가능)
                # 만약 주가가 현재 캔들의 저가 아래로 떨어지면, 추세하락 전환의 신호가 될 수 있음 / 반대로 주가가 현재 캔들의 고가 위로 올라가면, 추세상승 연장의 확증이 될 수 있음
                "Efficiency Rank": "I",
                "Up": 0.59,
                "Down": 0.41
            },
        }
    }

    def __init__(self, opening_price, high_price, low_price, trade_price, timestamp, candle_acc_trade_price, candle_acc_trade_volume):
        self.opening_price = opening_price
        self.high_price = high_price
        self.low_price = low_price
        self.trade_price = trade_price
        self.timestamp = timestamp
        self.candle_acc_trade_price = candle_acc_trade_price
        self.candle_acc_trade_volume = candle_acc_trade_volume

    def _get_type(self):
        a = 1
