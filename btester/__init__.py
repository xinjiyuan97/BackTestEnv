from gym.envs.registration import register

register(
    id = 'btester-v0',
    entry_point = 'btester.envs:BTesterEnv',
)
