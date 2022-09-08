class OrderError(Exception):
    '''Order Error'''

    def __init__(self, order, message='') -> None:
        self.order = order
        self.message = message
        super().__init__(self.message)
        

class TradeError(Exception):
    '''Error Related to Trading'''

    def __init__(self, trade, message='') -> None:
        self.trade = trade
        self.message = message
        super().__init__(self.message)



class NotEnoughVolume(Exception):
    '''Thrown when volume isn't there'''
    pass


class ExceedSumLimit(Exception):
    '''Thrown when order book sum doens't match'''
    pass

class MarketOrderBookError(OrderError):
    '''Thrown when there's an error in Market ORder Book'''
    pass

class TradeExecutionError(Exception):
    '''Thrown when there's trade execution error'''
    pass