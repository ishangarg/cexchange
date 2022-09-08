class PriceLevel():
    price = 0
    orders = []

    def __init__(self, price ) -> None:
        self.price = price
        self.orders = []
        
    def top(self):
        return self.orders[0]

    def is_empty(self):
        return len(self.orders) < 1 
    
    def add(self, order):
        if not self.find(order.id):
            self.orders.append(order)

    def remove(self, order):
        o = self.find(order.id)
        self.orders.remove(o)

    def total(self):
        return 0

    def find(self, id):
        order = [o for o in self.orders if self.orders.id == id]
        return order