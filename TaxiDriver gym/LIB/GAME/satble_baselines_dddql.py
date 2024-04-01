# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 18:07:32 2022

@author: C1982450
"""

import pygame
import yaml
import time

#from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines3 import DQN


from game import TaxiGym_v1_0

def save_data(data):
    with open(r'tmp/dddql.yaml', 'w') as outfile:
        data={'avr_r':data}
        yaml.dump(data, outfile, default_flow_style=False)
    

def main(): 
    
    env = TaxiGym_v1_0()
    #env.visualize=True
    
    print("Training started")
    model = DQN('MlpPolicy', env, verbose=0)
    model.learn(total_timesteps=480000)
    model.save("tmp/dddql_taxi_epochs")
    save_data(env.avg_reward)
    print("Training finshed")
    model = DQN('MlpPolicy', env, verbose=0)
    model.learn(total_timesteps=480000)
    model.save("tmp/dddql_taxi_epochs")
    save_data(env.avg_reward)
    print("Training finshed")
#############################################################Testing
    model = DQN.load("tmp/dddql_taxi_epochs")
    print("model ready")
    obs = env.reset()
    run=True
    while run:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        if dones:
             env.reset()
        time.sleep(1)
        env.render()
    pygame.quit()
    
if __name__ == "__main__":
    main()