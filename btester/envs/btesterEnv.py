import logging
import random
import gym
import os
from gym import spaces
from tqdm import tqdm
from btester.dataprovider import DataProvider
from btester.positions import Positions
from btester.reward import sharpRatio
import numpy as np
class BTesterEnv(gym.Env):
    metadata = {
        'video.frames_per_second': 2
    }

    actions = {
        "buy_open": 0,
        "close": 1,
        "hold": 2
    }

    config = {
        "name": None,
        "symbol": None,
        "dump path": "./record/",
        "future_info": {
                'close_commission_ratio': 0.0005,
                'open_commission_ratio': 0.0005,
                'close_commission_today_ratio': 0.0005,
                "leverage": 10,
                "settle_interval": 1440,
                "interval": 'min'
        },
        "init balance": 5,
        "INIT_LENGTH": 100,
        "STATUS": ['volume', 'open_price', 'high_price', 'low_price', 'close_price'], 
        "benchmark": 0.01
    }

    def __init__(self, datapath, actions = None, settings = None, rewardType = "sharp"):
        super(BTesterEnv, self).__init__()
        if settings:
            self.config.update(settings)
        if actions:
            self.actions = actions
        self.STATUS = self.config['STATUS']
        self.ccr = self.config['future_info']['close_commission_ratio']
        self.ocr = self.config['future_info']['open_commission_ratio']
        self.cctr = self.config['future_info']['close_commission_today_ratio']
        self.init_length = self.config['INIT_LENGTH']
        self.settle_interval = self.config['future_info']['settle_interval']
        obs_shape = (self.config['INIT_LENGTH'], len(self.STATUS))
        self.action_space = spaces.Discrete(len(self.actions.keys()))
        self.observation_space = spaces.Box(low = -10, high = 10, shape = obs_shape)
        self.dp = DataProvider(datapath, self.STATUS)
        self.val2action = {}
        self.leverage = self.config['future_info']['leverage']
        for k, v in self.actions.items():
            self.val2action[v] = k

        for i, s in enumerate(self.STATUS):
            if s == 'close_price':
                self.closeIdx = i
            elif s == 'open_price':
                self.openIdx = i
        
        if rewardType == 'sharp':
            self.reward_func = sharpRatio
        else:
            self.reward_func = earningRatio


    def _getInitObs(self):
        obs = []
        for _ in range(self.init_length):
            d, tag = next(self.flow)
            obs.append(d)
        return obs

    def _takeAction(self, action):
        action = self.val2action[action]
        closePrice = self.obs[-2][self.closeIdx]
        openPrice = self.obs[-1][self.openIdx]
        
        if action == "buy_open": 
            if self.side < 0:
                self._close(closePrice)
            if self.side == 0:
                self.side = 1
                additionalCost = self.ocr * self.leverage * openPrice 
                cost = additionalCost + openPrice
                if cost > self.balance:
                    return
                self.balance -= cost
                self.positions.buy_open(openPrice)

        elif action == "sell_open":
            if self.side > 0:
                self._close(closePrice)
            if self.side == 0:
                additionalCost = self.ocr * self.leverage * openPrice 
                cost = additionalCost + openPrice
                if cost > self.balance:
                    return
                self.balance -= cost
                self.positions.sell_open(openPrice)
                self.side = -1

        elif action == "close": 
            self._close(closePrice)
        else:
            pass

    def _close(self, price):
        value = self.positions.close(price)
        value -= value * self.ccr
        self.balance += value 
        self.side = 0

    def reset(self):
        self.currentStep = random.randint(0, self.dp.length - self.init_length)
        self.flow = self.dp.reset(self.currentStep)
        self.tqbar = self.dp.getProcessBar(self.init_length)
        self.balance = self.config['init balance']
        self.obs = self._getInitObs()
        self.positions = Positions(self.config['symbol'], self.leverage)
        self.side = 0
        self.timer = 0
        self.totalValue = [self.balance]
        self.record = False 
        return np.array(self.obs) / 10

    def step(self, action):
        self.tqbar.update(1)
        self.timer += 1
        reward = 0
        done = False
        try:
            obs, tag = next(self.flow)
            self.obs.append(obs)
            self._takeAction(action)
            self.obs = self.obs[1:]
        
        except:
            done = True
            print(self.totalValue[-1]) 
        
        value = self.positions.update(self.obs[-1][self.closeIdx]) + self.balance
        self.totalValue.append(value)
        if self.timer % self.settle_interval == 0:
            self._settle()
        reward = self.reward_func(self.totalValue, self.config['benchmark'])

        if done or value + self.balance < self.obs[-1][self.closeIdx]:
            done = True
            self.tqbar.close()
            print(self.totalValue[-1])
        else:
            done = False
        return np.array(self.obs) / 10, reward, done, {}

    def render(self):
        self.record = True

    def _settle(self):
        currentPrice = self.obs[-1][self.closeIdx]
        self.balance += self.positions.settle(currentPrice)

if __name__ == "__main__":
    datapath = os.path.join(os.environ['HOME'], 'Desktop/量化投资/okex/data/EOS-USD-SWAP.pkl')
    assert os.path.exists(datapath)
    env = BTesterEnv('/data/EOS-USD-SWAP.pkl') 