from btester.envs import BTesterEnv
import os
import numpy as np
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
import matplotlib.pyplot as plt
SYMBOL = 'EOS-USD-SWAP'
DATAPATH = os.path.join(os.environ['HOME'], 'Desktop/量化投资/okex/train/', '%s.pkl' % SYMBOL)
MAX_EPISODE = 10000
INIT_CASH = 10
settings = {
    "name": 'EOSUSESWAP_MIN',
    "symbol": SYMBOL,
    "INIT_LENGTH": 50,
    "init balance": INIT_CASH,
    "STATUS": ['open_price', 'high_price', 'low_price', 'close_price']
}

actions = {
    "buy_open": 0,
    "close": 1,
}


env = DummyVecEnv([lambda:
    BTesterEnv(DATAPATH, actions = actions, settings = settings)
])

DATAPATH = os.path.join(os.environ['HOME'], 'Desktop/量化投资/okex/test/', '%s.pkl' % SYMBOL)
tester = BTesterEnv(DATAPATH, actions = actions, settings = settings)



model = PPO2(MlpPolicy, env, verbose=1, gamma = 0.8)
for i in range(200):
    model.learn(total_timesteps = 10000)
    model.save("dqn_EOS")


    obs = tester.reset()
    value = []
    actions = []
    while True:
        action, _states = model.predict(obs)
        actions.append(action)
        obs, rewards, done, info = tester.step(action)
        
        if done:
            break
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.cla()
    plt.plot(tester.totalValue)
    plt.subplot(2, 1, 2)
    plt.cla()
    plt.plot(actions)
    plt.savefig('./%s.eps' % i)