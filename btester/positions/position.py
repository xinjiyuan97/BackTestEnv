class Position(object):
    def __init__(self, side, price, size, leverage = 10):
        self.side = side # long 1 / short -1
        self.price = price
        self.size = size
        self.pnl = 0
        self.leverage = leverage

    def update(self, price):
        self.pnl = (price - self.price) * self.size * self.leverage * self.side

    def settle(self, price):
        self.update(price)
        self.price = price
        return self.pnl

    def getValues(self):
        return self.price * self.size + self.pnl