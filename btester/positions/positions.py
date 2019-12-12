from .position import Position

class Positions(object):
    def __init__(self, symbol, leverage = 10):
        self.symbol = symbol
        self.leverage = leverage
        self.position = []
        self.value = 0

    def _addPosition(self, side, price, size):
        pos = Position(side, price, size, self.leverage)
        self.value += pos.getValues()
        self.position.append(pos)

    def update(self, price):
        self.value = 0
        for pos in self.position:
            pos.update(price)
            self.value += pos.getValues()
        return self.value
        
    def settle(self, price):
        pnl = 0
        size = 0
        
        for pos in self.position:
            pnl += pos.settle(price)
            size += pos.size * pos.side
        
        self.position = []
        (size, side) = (-size, -1) if size < 0 else (size, 1)
        self._addPosition(side, price, size)
        return pnl

    def getPositionsValue(self):
        value = 0
        for pos in self.position:
            value += pos.getValues()
        return value

    def buy_open(self, price, size = 1):
        self._addPosition(1, price, size)
    
    def sell_open(self, price, size = 1):
        self._addPosition(-1, price, size)
    
    def close(self, price):
        """
        全平
        """
        value = self.getPositionsValue()
        self.position = []
        return value

