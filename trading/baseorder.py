from constants import OrderError


class BaseOrder:
    id = None
    timestamp = None
    _type = None
    volume = None
    market = None
    TYPE_ASK = 'ask'
    TYPE_BID = 'bid'

    def __init__(self, id, timestamp, _type, volume, market) -> None:
        self.id = id
        self.timestamp = timestamp
        if _type == self.TYPE_ASK or _type == self.TYPE_BID:
            self._type = _type
        else:
            raise OrderError(self, "Order has to be Type Bid/Ask")
        self.volume = volume
        self.market = market
    
    def trade_with(self, _counter_order, _counter_book):
        pass

    def fill(self, _trade_price, _trade_volume, _trade_fund):
        pass

    def filled(self) -> bool:
        pass

    def label(self):
        pass

    def valid(self, attrs) -> bool:
        pass

    def attributed(self):
        pass

    def bid(self):
        return self._type == self.TYPE_BID

    def ask(self):
        return self._type == self.TYPE_ASK

    def min(self, a, b):
        if a < b:
            return a
        return b

    def max(self, a, b):
        if a > b:
            return a
        return b

