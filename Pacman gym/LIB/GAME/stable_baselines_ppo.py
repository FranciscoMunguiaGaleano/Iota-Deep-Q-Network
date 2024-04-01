#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:13:10 2022

@author: care-o-bot
"""

import pygame
import yaml
import time

#from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines3 import PPO


from game import Pacman_v1_1

def save_data(data):
    with open(r'tmp/ppo.yaml', 'w') as outfile:
        data={'avr_r':data}
        yaml.dump(data, outfile, default_flow_style=False)
    

def main():
    pygame.init()
    pygame.display.set_caption("MEXIPACMAN")
    env = Pacman_v1_1()
    t=env.clock.tick(30)
    env.dt=t/1000.0
    #env.visualize=True
    
    print("Training started")
    model = PPO('MlpPolicy', env, verbose=0)
    model.learn(total_timesteps=480000)
    model.save("tmp/ppo_pacman_epochs")
    save_data(env.avg_reward)
    print("Training finshed")
#############################################################Testing
    model = PPO.load("tmp/ppo_pacman_epochs")
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