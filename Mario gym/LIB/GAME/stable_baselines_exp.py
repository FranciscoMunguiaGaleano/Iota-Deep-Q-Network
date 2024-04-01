#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 10:39:31 2022

@author: robot
"""
import pygame
import yaml
import time

from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback,StopTrainingOnMaxEpisodes,EveryNTimesteps
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results
from stable_baselines3.common.monitor import Monitor

import gym
from gym import spaces

from game import Mario_v1_1

def save_data(data):
    with open(r'tmp/test.yaml', 'w') as outfile:
        data={'avr_r':data}
        yaml.dump(data, outfile, default_flow_style=False)
    

def main():
    pygame.init()
    pygame.display.set_caption("MEXITENDO")
    env = Mario_v1_1()
    t=env.clock.tick(30)
    env.dt=t/1000.0
    #env.visualize=True
    
    print("Training started")
    model = DQN("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=480000,log_interval=4)
    model.save("tmp/dql_mario_epochs")
    save_data(env.avg_reward)
    print("Training finshed")
#############################################################Testing
    model = DQN.load("tmp/dql_mario_epochs")
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
