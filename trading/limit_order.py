from baseorder import BaseOrder
from market_order import MarketOrder
from constants import MarketOrderBookError, NotEnoughVolume, OrderError

class LimitOrder(BaseOrder):

    price = 0

    def __init__(self, id, timestamp, _type, volume, market, price) -> None:
        super().__init__( id, timestamp, _type, volume, market)
        self.price = price
        if not self.valid():
            raise OrderError(self, "Order Is Not Valid")


    def trade_with(self, _counter_order, _counter_book):
        if type(_counter_order) == MarketOrder:
            raise MarketOrderBookError("Market Order In Order Book Detected")

        if not self.crossed(_counter_order.price):
            return
        
        trade_price  = _counter_order.price
        trade_volume = self.min(self.volume, _counter_order.volume)
        trade_funds  = trade_price * trade_volume

        return trade_price, trade_volume, trade_funds


    def fill(self, _trade_price, trade_volume, _trade_funds):
        if trade_volume > self.volume:
            raise NotEnoughVolume("Not Enough Volume")
        self.volume -= trade_volume


    def filled(self):
        return self.volume <= 0


    def crossed(self, price):
        if self._type == self.TYPE_ASK:
            return price >= self.price
        else:
            return price <= self.price


    def label(self):
        return "Order: %d volume : %f price : %f" % (self.id, self.volume, self.price)


    def valid(self):
        return self.price > 0 and not self.timestamp == None and not self.id == None

    
    def attributes(self):
      return { 'id': self.id, 'timestamp': self.timestamp, 'type': self._type, 
      'volume': self.volume, 'price': self.price,'market': self.market,  'ord_type': 'limit' }

        
