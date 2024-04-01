# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 18:07:32 2022

@author: C1982450
"""

import pygame
import yaml
import time

#from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN


from game import Flappy_v1_0

def save_data(data):
    with open(r'tmp/dddql.yaml', 'w') as outfile:
        data={'avr_r':data}
        yaml.dump(data, outfile, default_flow_style=False)
    

def main():
    pygame.init()
    pygame.display.set_caption("TACOBIRD")
    env = Flappy_v1_0()
    t=env.clock.tick(30)
    env.dt=t/1000.0
    #env.visualize=True
    
    print("Training started")
    model = DQN('MlpPolicy', env, verbose=0,double_q=True,policy_kwargs=dict(dueling=True))
    model.learn(total_timesteps=480000)
    model.save("tmp/dddql_flappy_epochs")
    save_data(env.avg_reward)
    print("Training finshed")
#############################################################Testing
    model = DQN.load("tmp/dddql_flappy_epochs")
    print("model ready")
    obs = env.reset()
    run=True
    while run:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 run = False
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        if dones:
             env.reset()
        time.sleep(0.01)
        env.render()
    pygame.quit()
    
if __name__ == "__main__":
    main()