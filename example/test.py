from btester.envs import BTesterEnv
import os
import numpy as np
from stable_baselines.deepq.policies import LnMlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import DQN
import matplotlib.pyplot as plt
SYMBOL = 'EOS-USD-SWAP'
DATAPATH = os.path.join(os.environ['HOME'], 'Desktop/量化投资/okex/train/', '%s.pkl' % SYMBOL)
MAX_EPISODE = 10000
INIT_CASH = 10
settings = {
    "name": 'EOSUSESWAP_MIN',
    "symbol": SYMBOL,
    "INIT_LENGTH": 20,
    "init balance": INIT_CASH,
    "STATUS": ['open_price', 'high_price', 'low_price', 'close_price']
}

actions = {
    "buy_open": 0,
    "close": 1,
    "hold": 2
}

env = BTesterEnv(DATAPATH, actions = actions, settings = settings)
balance = []
env.reset()
while True:
    balance.append(env.balance)
    obs, reward, done, _ = env.step(0)
    if done:
        break

plt.plot(balance)
plt.show()