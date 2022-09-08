from baseorder import BaseOrder

class MarketOrder(BaseOrder):

    locked = 0
    
    def __init__(self) -> None:
        super().__init__()
