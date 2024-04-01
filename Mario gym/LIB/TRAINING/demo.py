# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:30:20 2022

@author: C1982450
"""

import sys
import os

LOCAL_PATH=os.path.dirname(os.path.abspath(__file__))
MAIN_PATH=LOCAL_PATH+'/../..'


ENV_PATH=MAIN_PATH+"/LIB/GAME"
LIB_PATH=MAIN_PATH+"/LIB"
BIN_PATH=MAIN_PATH+"/BIN"
TRN_PATH=MAIN_PATH+"/LIB/TRAINING"

sys.path.insert(1, ENV_PATH)
sys.path.insert(1, TRN_PATH)
sys.path.insert(1, LIB_PATH)

from game import Mario_v1_0 as envi
from agents import *
import yaml
import pygame
from colored import fg, bg, attr
from IPython.display import clear_output
import time



CONF_PATH=MAIN_PATH+"/CONF"
DEMO_PATH=MAIN_PATH+"/DEMO"
DOC_PATH=MAIN_PATH+"/DOC"
ENV_PATH=MAIN_PATH+"/LIB/GAME"
LIB_PATH=MAIN_PATH+"/LIB"
LOG_PATH=MAIN_PATH+"/LOG"
IMG_PATH=MAIN_PATH+"/IMG"
POLICIES_PATH=MAIN_PATH+"/BIN"
TEMP_PATH=MAIN_PATH+"/TEMP"
TRN_PATH=MAIN_PATH+"/LIB/TRAINING"
NOTHING=0
JUMP_WEAK=1
JUMP_STRONG=2
RIGHT_R=3
LEFT_R=4

class Demo():
    def __init__(self,model_name):
        print("Demo "+model_name)
        self.environment=envi()
        self.main=tf.keras.models.load_model(BIN_PATH+"/"+model_name)
        self.episodes=0
        self.actions={0:JUMP_STRONG,1:RIGHT_R}
        self.environment.dt=30.0/1000.0
    def act(self,s):
        #print(self.main(s))
        #time.sleep(0.2)
        return np.argmax(self.main(s))
    def run_demo(self,episodes_num,max_steps):
        r=0
        steps=0
        while self.episodes<episodes_num:
            steps=0
            s=self.environment.reset()
            d=False
            #print(steps)
            while not d:
                steps+=1
                for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                      pygame.quit()
                if steps%max_steps==0:
                    break
                s=tf.convert_to_tensor([s.flatten()],dtype=tf.float32)
                action=self.act(s)
                s_,d,r=self.environment.step(self.actions[action])
                self.environment.render()
                s=s_
                time.sleep(0.01)
            self.episodes+=1
        self.episodes=0
    def run_demo_iota(self,episodes_num):
        r=0
        while self.episodes<episodes_num:
            s=self.environment.reset()
            d=False
            while not d:
                for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                      pygame.quit()
                s=tf.convert_to_tensor([s.flatten()],dtype=tf.float32)
                iota=self.environment.iota()[1:]
                action=self.act_iota(s,iota)
                s_,d,r=self.environment.step(self.actions[action])
                self.environment.render()
                s=s_
                #if d:
                #    break
                time.sleep(0.01)
            self.episodes+=1
        self.episodes=0
    def act_iota(self,state,iota):
        probs=self.main(state)[0]
        #print(probs)
        probabilities=[]
        choices=[]
        for i in range(0,len(iota)):
            if iota[i]>0:
                probabilities.append(probs[i])
                choices.append(i)
            if len(probabilities)>0:
                action=choices[np.argmax(np.array(probabilities))]
                argmax=np.amax(np.array(probabilities))
            else:
                action=0
                argmax=None
            #time.sleep(0.1)
        return action
if __name__ == "__main__":
    #demo_epocs=[["dql",300],["ddql",200],["dudql",1500],["dddql",1000]]
    demo_epocs=[["dql",300]]
    episodes=2
    while True:
        experiment_demo=input("Select experiment: ")
        if experiment_demo=='normal':
            for vid,max_steps in demo_epocs:
                pygame.init()
                pygame.display.set_caption(vid)
                demo=Demo(vid)
                demo.run_demo(episodes,max_steps)
                pygame.quit()
        elif experiment_demo=='normal_episodes':
            for vid,max_steps in demo_epocs:
                pygame.init()
                pygame.display.set_caption(vid+"_episodes")
                demo=Demo(vid+"_episodes")
                demo.run_demo(episodes,max_steps)
                pygame.quit()
        elif experiment_demo=='iota':
            for vid,max_steps in demo_epocs:
                exp="i"+vid+"l1"
                pygame.init()
                pygame.display.set_caption(exp)
                demo=Demo(exp)
                demo.run_demo_iota(episodes)
                pygame.quit()
        elif experiment_demo=='iota_episodes':
            for vid,max_steps in demo_epocs:
                exp="i"+vid+"l1_episodes"
                pygame.init()
                pygame.display.set_caption(exp)
                demo=Demo(exp)
                demo.run_demo_iota(episodes)
                pygame.quit()
        elif experiment_demo=='iota_l2':
            for vid,max_steps in demo_epocs:
                exp="i"+vid+"l1l2"
                pygame.init()
                pygame.display.set_caption(exp)
                demo=Demo(exp)
                demo.run_demo_iota(episodes)
                pygame.quit()
        elif experiment_demo=='iota_episodes_l2':
            for vid,max_steps in demo_epocs:
                exp="i"+vid+"l1l2_episodes"
                pygame.init()
                pygame.display.set_caption(exp)
                demo=Demo(exp)
                demo.run_demo_iota(episodes)
                pygame.quit()
        elif experiment_demo=='iota_l2l3':
            for vid,max_steps in demo_epocs:
                exp="i"+vid+"l1l2l3"
                pygame.init()
                pygame.display.set_caption(exp)
                demo=Demo(exp)
                demo.run_demo_iota(episodes)
                pygame.quit()
        elif experiment_demo=='iota_episodes_l2l3':
            for vid,max_steps in demo_epocs:
                exp="i"+vid+"l1l2l3_episodes"
                pygame.init()
                pygame.display.set_caption(exp)
                demo=Demo(exp)
                demo.run_demo_iota(episodes)
                pygame.quit()
        elif experiment_demo=='-h':
            print("[INFO]:Valid options:")
            print("  a) normal")
            print("  b) normal_episodes")
            print("  c) iota") 
            print("  d) iota_episodes")
            print("  e) iota_l2") 
            print("  f) iota_episodes_l2")
            print("  g) iota_l2l3") 
            print("  h) iota_episodes_l2l3")
            print("  i) exit()")
        elif experiment_demo=='exit()':
            break
        else:
            print("Not valid")
