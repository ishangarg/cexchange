from order_book import OrderBook
from baseorder import BaseOrder

class OrderBookManager():
    ask_orders = None
    bid_orders = None
    market = None

    def __init__(self, market, on_change) -> None:
        self.market = market
        self.ask_orders = OrderBook(self.market, BaseOrder.TYPE_ASK,  on_change)
        self.bid_orders = OrderBook(self.market, BaseOrder.TYPE_BID,  on_change)

    def get_books(self, type):
        if type == BaseOrder.TYPE_ASK:
            return self.ask_orders, self.bid_orders
        elif type == BaseOrder.TYPE_BID:
            return self.bid_orders, self.ask_orders