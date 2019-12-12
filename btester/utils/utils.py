def getTotalAssets(cash, position):
    return cash + position['price'] * position['size']

def getInfo(cash, position):
    info = {}
    info['cash'] = cash
    info['position'] = position
    info['assets'] = getTotalAssets(cash, position)
    info['risk'] = (info['assets'] - cash) / info['assets']
    return info

def getOCIdx(status):
    for i, s in enumerate(status):
        if s == 'open_price':
            openIdx = i
        elif s == 'close_price':
            closeIdx = i
    return openIdx, closeIdx