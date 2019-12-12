import numpy as np
import pickle
import os
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
from tqdm import tqdm
from ..utils import getOCIdx
class DataProvider(object):
    def __init__(self, path, status, marker = None):
        self.status = status
        self.data = pickle.load(open(path, 'rb'))[status].to_numpy()
        self.length = len(self.data)
        self.marker = marker
        if marker:
            self.marker = marker
            openIdx, closeIdx = getOCIdx(status)
            self.tag = marker.count(self.data, openIdx, closeIdx)

    def reset(self, index = 0):
        self.index = index
        def dataProvider(index, data):
            while index < len(data):
                if self.marker and index < len(self.tag) - 1:
                    yield data[index], self.tag[index + 1]
                else:
                    yield data[index], None
                index += 1
            return None
        return dataProvider(index, self.data)

    def rawData(self):
        return self.data

    def getProcessBar(self, initLength = 1):
        self.tqbar = tqdm(total = self.data.shape[0], initial = initLength + self.index)
        return self.tqbar
        
if __name__ == "__main__":
    symbol = 'EOS-USD-SWAP'
    datapath = os.path.join(os.environ['HOME'], 'Desktop/量化投资/okex/train/', '%s.pkl' % symbol)
    status = ['volume', 'open_price', 'high_price', 'low_price', 'close_price']
    dp = DataProvider(datapath, status)
    d = dp.reset()
    data = next(d)
    print(np.append(data, [0]))