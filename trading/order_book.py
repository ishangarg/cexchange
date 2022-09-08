from bintrees import RBTree
from price_levels import PriceLevel
from constants import OrderError, NotEnoughVolume, MarketOrderBookError
from limit_order import LimitOrder
from market_order import MarketOrder
from .baseorder import BaseOrder

class OrderBook():

    market = None
    limit_orders = None
    market_orders = None
    side = None

    on_change = None

    def __init__(self, market, side, on_change) -> None:
        self.market = market
        self.side = side
        self.limit_orders = RBTree()
        self.market_orders = RBTree()
        self.on_change = on_change
    
    def notify_onchange(self, market, side, price, amount=None):
        if self.on_change == None:
            return
        
        self.on_change(market, side, price, amount)

    def limit_top(self, order):
        if order.side == BaseOrder.TYPE_ASK:
            return self.ask_limit_top()
        elif order.side == BaseOrder.TYPE_BID:
            return self.bid_limit_top()
        else:
            raise ValueError("Unknown Order Side")


    def best_limit_price(self):
        return


    def top(self):
        if not self.market_orders.is_empty():
            order = self.market_orders.min_item()
            raise MarketOrderBookError('market order in orderbook detected')

        return self.limit_top()

    def fill_top(self, trade_price, trade_volume, trade_funds):
        order = self.top()
        if order == None:
            raise NotEnoughVolume("No Top Order In The Ordder Book")

        order.fill(trade_price, trade_volume, trade_funds)
        if order.filled():
            self.remove(order)
        else:
            self.notify_onchange(self.market, self.side, order.price, self.limit_orders.get(order.price).total())
        

    def find(self,order):
        if type(order) == LimitOrder:
            o = self.limit_orders.get(order.price, None)
        elif type(order) == MarketOrder:
            o = self.market_orders.get(order.price, None)
        
        if o == None:
            raise OrderError(order, "Order Not In OrderBook")
        
        return o.find(order.id)

    def add(self, order):
        if order.volume <= 0:
            raise NotEnoughVolume("Cannot add 0 or negative volume")

        if type(order) == LimitOrder:
            try:
                o = self.find(order)
                o.add(order)
            except OrderError:
                o = PriceLevel(order.price)
                o.add(order)
                self.limit_orders.insert(order.price, o)
            self.notify_onchange(self.market, self.side, order.price, o.total())
        elif type(order) == MarketOrder:
            raise MarketOrderBookError("Cannot Add Market Orders To Order Book")

    def remove(self, order):
        if type(order) == LimitOrder:
            return
        elif type(order) == MarketOrder:
            return
        else:
            raise ValueError("Unknown Order Side")

    def all_limit_orders(self):
        orders = {}
        for k,v in self.limit_orders.items():
            orders[k] = v.orders

        return orders

    def remove_limit_order(self, order):
        price_level = self.limit_orders.get(order.price, None)
        
        if price_level == None:
            return
        
        o = price_level.find(order.id)

        if o == None:
            return

        price_level.remove(order)
        if price_level.orders.is_empty():
            self.limit_orders.pop(order.price)

        return order

    def remove_market_order(self, order):
        price_level = self.market_orders.get(order.price, None)

        if price_level == None:
            return

        #self.market_orders.delete(order.id) #needs to be implemented
        return order

    
    def ask_limit_top(self): # lowest price wins
      if self.limit_orders.is_empty():
        return
      price, orders = self.limit_orders.min_item()
      return orders.top()
    
    def  bid_limit_top(self): # highest price wins
        if self.limit_orders.is_empty():
            return
        price, orders = self.limit_orders.max_item()
        return orders.top()
        