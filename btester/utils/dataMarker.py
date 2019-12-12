
class DataMarker(object):
    def __init__(self, block = 15, length = 100, threshold = 0.005):
        self.block = block
        self.length = length
        self.threshold = threshold
    
    def count(self, tick, openIdx = 1, closeIdx = -1):
        res = []
        for i in range(self.length):
            last = (i + 1) * self.block - 1
            prev = i * self.block
            if (tick[last][closeIdx] - tick[prev][openIdx]) > self.threshold:
                for j in range(prev, last + 1):
                    res.append(1)
            else:
                for j in range(prev, last + 1):
                    res.append(0)
        return res