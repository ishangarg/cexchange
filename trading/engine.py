import datetime
import time
from order_book_manager import OrderBookManager

class Engine():

    ORDER_SUBMIT_MAX_ATTEMPTS = 3
    MIN_INCREMENT_COUNT_TO_SNAPSHOT = 20
    MIN_PERIOD_TO_SNAPSHOT = 10 #seconds
    MAX_PERIOD_TO_SNAPSHOT = 60 #seconds

    ORDERBOOK = None
    MODE = None
    QUEUE = None

    INITIALIZING = None
    SNAPSHOT_TIME = None
    INCREMENT_COUNT = 0
    SEQUENCE_NUMBER = 0

    market = None

    def __init__(self, market) -> None:
        self.market = market
        self.ORDERBOOK = OrderBookManager(self.market.symbol)
        pass

    def publish_increment(self):
        if self.INITIALIZING:
            return
        
        if self.INCREMENT_COUNT < self.MIN_INCREMENT_COUNT_TO_SNAPSHOT and self.SNAPSHOT_TIME <= datetime.datetime.now() - self.MAX_PERIOD_TO_SNAPSHOT:
            self.INCREMENT_COUNT = 0
        
        self.INCREMENT_COUNT += 1
