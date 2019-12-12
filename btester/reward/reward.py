import numpy as np

def sharpRatio(values, baseline):
    r  = []
    # for val, i in enumerate(values):
        # r.append((val - values[i]) / val)

    values = np.array(values)
    # std = np.std(values, dtype = np.float32) + 1e-4
    return (values[-1] - values[-2]) / values[-1]  * 1000
    
def earningRatio(values, baseline):
    pass