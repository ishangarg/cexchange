from baseorder import BaseOrder
from limit_order import LimitOrder
from order_book import OrderBook

def on_change(market, side, price, amount):
    print("market: " + str(market) + " side: " + str(side) + " price: " + str(price) + " amount: " + str(amount))

def main():
    limit_1 = LimitOrder(1, 1, BaseOrder.TYPE_ASK, 100, "btcusd", 10000)
    limit_2 = LimitOrder(2, 2, BaseOrder.TYPE_ASK, 50, "btcusd", 11000)
    limit_3 = LimitOrder(3, 4, BaseOrder.TYPE_ASK, 150, "btcusd", 12000)

    order_book = OrderBook("btcusd", BaseOrder.TYPE_ASK, on_change)
    order_book.add(limit_1)
    order_book.add(limit_2)
    order_book.add(limit_3)

    orders = order_book.all_limit_orders()
    print(str(orders))


if __name__ == "__main__":
    main()