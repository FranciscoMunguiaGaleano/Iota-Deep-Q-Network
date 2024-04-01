#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:02:48 2022

@author: robot
"""

import pygame
import yaml
import time

#from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN


from game import Mario_v1_1

def save_data(data):
    with open(r'tmp/ddql.yaml', 'w') as outfile:
        data={'avr_r':data}
        yaml.dump(data, outfile, default_flow_style=False)
    

def main():
    pygame.init()
    pygame.display.set_caption("MEXITENDO")
    env = Mario_v1_1()
    t=env.clock.tick(30)
    env.dt=t/1000.0
    #env.visualize=True
    
    #print("Training started")
    #model = DQN('MlpPolicy', env, verbose=0,double_q=True,policy_kwargs=dict(dueling=False))
    #model.learn(total_timesteps=480000)
    #model.save("tmp/ddql_mario_epochs")
    #save_data(env.avg_reward)
    #print("Training finshed")
#############################################################Testing
    model = DQN.load("tmp/dql_mario_epochs")
    #model = DQN.load("deepq_mario")
    print("model ready")
    obs = env.reset()
    run=True
    n=0
    while run:
        if n==0:
            time.sleep(5)
            n+=1
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 run = False
        action, _states = model.predict(obs)
        #print(action)
        obs, rewards, dones, info = env.step(action)
        if dones:
             env.reset()
        time.sleep(0.01)
        env.render()
    pygame.quit()
    
if __name__ == "__main__":
    main()
