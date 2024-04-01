# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 15:25:51 2021

@author: Francisco Munguia Galeano
"""

import sys
import os

MAIN_PATH=os.path.dirname(os.path.abspath(__file__))

import numpy as np
import pygame
#from pygame.locals import *
from sys import exit
import math
import time

import gym
from gym import spaces
import yaml



##############################
import time
from colored import fg, bg, attr
from IPython.display import clear_output
import random
import numpy as np
import json
import pygame
from pygame.locals  import *
from stable_baselines3.common.env_checker import check_env

ROWS=10
COLS=10

class TaxiGym_v1_0(gym.Env):
    def __init__(self):
        super().__init__()
        self.v_walls=[[-0.5,0],[-0.5,1],[-0.5,2],[-0.5,3],[-0.5,4],[4.5,0],[4.5,1],[4.5,2],[4.5,3],[4.5,4],[0.5,0],[0.5,1],[1.5,4],[2.5,0],[2.5,1]]
        self.v_walls_s=[[0,0],[0,1],[0,2],[0,3],[0,4],[10,0],[10,1],[10,2],[10,3],[10,4],[2,0],[2,1],[4,4],[6,0],[6,1]]
        self.h_walls=[[0,-0.5],[1,-0.5],[2,-0.5],[3,-0.5],[4,-0.5],[1,4.5],[2,4.5],[3,4.5],[4,4.5],[0,4.5]]
        self.pas_pos=[]
        self.des_pos=[]
        self.taxi_pos=[0,0]
        self.letres_pos=[]
        self.actions=[0,1,2,3,4,5]
        self.goal=[]
        self.global_done=False
        self.seed=None
        self.done=False
        self.visualize=False
        self.matrix_state_ql=np.zeros((11,5))
        self.action_space= spaces.Discrete(6)

        #self.matrix_state.reshape(13,11,1)
        self.observation_space=spaces.Box(low=0, high=1, shape=(11,5,1), dtype=np.float64)
        self.actual_reward_episode=[]
        self.actual_reward=0
        self.act_avg=[]
        self.avg_reward=[]
        self.actual_episode=0
        self.actual_step=0
        self.actual_epoch=0
        self.reset()
    def step(self,action):
        if action==0:
            taxi_next_pos=[self.taxi_pos[0],self.taxi_pos[1]+1]
            if self.collition(taxi_next_pos)==False:
                self.taxi_pos=taxi_next_pos
                self.build_env()
                self.done=False
                self.check_progress(0)
                return self.state(),self.reward_function(),False,{}
            else:
                self.done=True
                self.check_progress(0)
                return self.state(),0,True,{}
        elif action==1:
            taxi_next_pos=[self.taxi_pos[0]+1,self.taxi_pos[1]]
            if self.collition(taxi_next_pos)==False:
                self.taxi_pos=taxi_next_pos
                self.build_env()
                self.done=False
                self.check_progress(0)
                return self.state(),self.reward_function(),False,{}
            else:
                self.done=True
                self.check_progress(0)
                return self.state(),0,True,{}
        elif action==2:
            taxi_next_pos=[self.taxi_pos[0],self.taxi_pos[1]-1]
            if self.collition(taxi_next_pos)==False:
                self.taxi_pos=taxi_next_pos
                self.build_env()
                self.done=False
                self.check_progress(0)
                return self.state(),self.reward_function(),False,{}
            else:
                self.done=True
                self.check_progress(0)
                return self.state(),0,True,{}
        elif action==3:
            taxi_next_pos=[self.taxi_pos[0]-1,self.taxi_pos[1]]
            if self.collition(taxi_next_pos)==False:
                self.taxi_pos=taxi_next_pos
                self.build_env()
                self.done=False
                self.check_progress(0)
                return self.state(),self.reward_function(),False,{}
            else:
                self.done=True
                self.check_progress(0)
                return self.state(),0,True,{}
        elif action==4:
            if self.taxi_pos==self.pas_pos and self.picked==False:
                self.picked=True
                if self.pas_pos==self.goal:
                    goal=True
                else:
                    goal=False
                self.taxi_color=2
                self.pas_color=0
                self.build_env()
                self.done=False
                self.check_progress(10)
                return self.state(),10,False,{}
            else:
                self.done=False
                self.check_progress(0)
                return self.state(),0,True,{}
        elif action==5:
            if self.taxi_pos==self.des_pos and self.picked==True:
                self.picked=False
                self.global_done=True
                if self.des_pos==self.goal:
                    self.global_done=True
                    goal=True
                else:
                    goal=False
                    self.done=True
                self.check_progress(10)
                return self.state(),10,True,{}
            for name,pos in self.letres_pos:
                if pos==self.taxi_pos and self.picked==True:
                    self.picked=False
                    self.taxi_color=3
                    self.pas_pos=pos
                    self.pas_color=12
                    self.build_env()
            self.done=True
            self.check_progress(0)
            return self.state(),0,True,{}            
        else:
            print("Action not allowed!!")
        ###
    def check_progress(self,r):
        if self.visualize:
            self.render()
        self.actual_step+=1
        self.actual_epoch+=1
        if self.actual_step>3000:
            self.actual_step=0
            self.done=True
        self.actual_reward+=r
        if self.done:
            self.act_avg.append(self.actual_reward)
            self.actual_reward=0
        if self.actual_epoch%2400==0 and self.actual_epoch>0:
            epoch=math.floor(self.actual_epoch/2400)
            try:
                reward=(sum(self.act_avg)/len(self.act_avg))
            except:
                reward=0
            print("Epoch:",epoch, "Reward: ",reward)
            self.avg_reward.append(reward)
    def reset(self):
        self.global_done=False
        self.picked=False
        self.pas_pos=[]
        self.des_pos=[]
        self.letres_pos=[]
        self.taxi_color=3
        self.pas_color=12
        self.des_color=5
        self.sample_start()
        return self.state()
    def render(self):
        #os.system('cls')
        print("\033[H\033[J") 
        print('%s%s%s'% (bg(7),"+---------+",attr(0)))
        for i in range(0,5):
            for j in range(0,6): 
                print('%s%s%s'%(fg(0),bg(7),self.environment[1][4-i][j])+'%s%s%s'% (fg(self.environment[3][4-i][j]),bg(self.environment[2][4-i][j]),self.environment[0][4-i][j]),end='')
        print('%s%s%s'% (bg(7),"+---------+",attr(0)))
    def state(self):
        self.matrix_state_ql=np.zeros((11,5))
        for x,y in self.v_walls_s:
            self.matrix_state_ql[x][y]=0.2
        if self.picked:
            if self.taxi_pos==self.pas_pos:
                self.matrix_state_ql[self.get_taxi_pos()]=0.6
            else:
                self.matrix_state_ql[self.get_taxi_pos()]=0.5
        else:
            if self.taxi_pos==self.pas_pos:
                self.matrix_state_ql[self.get_taxi_pos()]=0.4
            else:
                self.matrix_state_ql[self.get_taxi_pos()]=0.3
        #return self.matrix_state_ql
        return self.matrix_state_ql.reshape(11,5,1)
    def reward_function(self):
        reward=0.0
        if self.picked==True:
            reward= 1-(math.sqrt(((self.des_pos[0]-self.taxi_pos[0])**2)+ ((self.des_pos[1]-self.taxi_pos[1])**2)))/25.0
            return reward
        else:
            reward= 1-(math.sqrt(((self.pas_pos[0]-self.pas_pos[0])**2)+ ((self.pas_pos[1]-self.taxi_pos[1])**2)))/25.0
            return reward
    def action_space(self):
        return self.actions
    def action_size(self):
        return len(self.actions)
    def state_size(self):
        return len(self.state())
    def set_seed(self,seed):
        self.seed=seed
        random.seed(self.seed)
    def fixed_start(self):
        L='YRGB'
        stops=random.sample(L,len(L))
        #stops_pos=[[[0,0],[0,1]],[[0,4],[1,4]],[[3,4],[4,4]],[[3,1],[4,1],[3,0],[4,0]]]
        stops_pos=[[[0,0],[0,0]],[[0,4],[0,4]],[[4,4],[4,4]],[[4,0],[4,0],[4,0],[4,0]]]
        #stops_pos=[[[0,0]],[[0,4]],[[4,4]],[[3,0]]]
        passenger=random.sample(L,1)[0]
        L=L.replace(passenger,'')
        destination=random.sample(L,1)[0]
        tax_coor=[]
        for x in range(0,5):
            for y in range(0,5):
                tax_coor.append([x,y])
        lim=1
        for i in range(0,4):
            if i==3:
                lim=3
            self.letres_pos.append([stops[i],stops_pos[i][random.randint(0, lim)]])
            if stops[i]==passenger:
                self.pas_pos=self.letres_pos[i][1]
            elif stops[i]==destination:
                self.des_pos=self.letres_pos[i][1]
                forb=[]
        for letre,pos in self.letres_pos:
            forb.append(pos)
        for remv in forb:
            tax_coor.remove(remv)
        self.taxi_pos=random.sample(tax_coor,1)[0]
        self.build_env()
    def sample_start(self):
        L='YRGB'
        stops=random.sample(L,len(L))
        #stops_pos=[[[0,0],[0,1]],[[0,4],[1,4]],[[3,4],[4,4]],[[3,1],[4,1],[3,0],[4,0]]]
        stops_pos=[[[0,0],[0,0]],[[0,4],[0,4]],[[4,4],[4,4]],[[3,0],[3,0],[3,0],[3,0]]]
        #stops_pos=[[[0,0]],[[0,4]],[[4,4]],[[3,0]]]
        passenger=random.sample(L,1)[0]
        L=L.replace(passenger,'')
        destination=random.sample(L,1)[0]
        tax_coor=[]
        for x in range(0,5):
            for y in range(0,5):
                tax_coor.append([x,y])
        lim=1
        for i in range(0,4):
            if i==3:
                lim=3
            self.letres_pos.append([stops[i],stops_pos[i][random.randint(0, lim)]])
            if stops[i]==passenger:
                self.pas_pos=self.letres_pos[i][1]
            elif stops[i]==destination:
                self.des_pos=self.letres_pos[i][1]
                forb=[]
        for letre,pos in self.letres_pos:
            forb.append(pos)
        for remv in forb:
            tax_coor.remove(remv)
        self.taxi_pos=random.sample(tax_coor,1)[0]
        self.build_env()

    def get_env(self):
        return self.taxi_color,self.pas_color,self.des_color,self.letres_pos,self.picked
    def set_env(self,taxi_color,pas_color,des_color,letres_pos,picked):
        self.taxi_color=taxi_color
        self.pas_color=pas_color
        self.des_color=des_color
        self.letres_pos=letres_pos
        self.picked=picked
        self.build_env()
        return
    def build_env(self):
        self.canvas()
        self.environment[0][self.taxi_pos[1]][self.taxi_pos[0]]=' '
        self.environment[2][self.taxi_pos[1]][self.taxi_pos[0]]=self.taxi_color
        self.environment[3][self.pas_pos[1]][self.pas_pos[0]]=self.pas_color
        self.environment[3][self.des_pos[1]][self.des_pos[0]]=self.des_color
        for name,pos in self.letres_pos:
            self.environment[0][pos[1]][pos[0]]=name
    def canvas(self):
        self.environment=[[[' ',' ',' ',' ',' ','\n'],
                           [' ',' ',' ',' ',' ','\n'],
                           [' ',' ',' ',' ',' ','\n'],
                           [' ',' ',' ',' ',' ','\n'],
                           [' ',' ',' ',' ',' ','\n']],

                          [[':',':',':',':',':',':'],
                           [':',':',':',':',':',':'],
                           [':',':',':',':',':',':'],
                           [':',':',':',':',':',':'],
                           [':',':',':',':',':',':'],],
                          
                          [[7,7,7,7,7,7],
                           [7,7,7,7,7,7],
                           [7,7,7,7,7,7],
                           [7,7,7,7,7,7],
                           [7,7,7,7,7,7],],
                          
                          [[0,0,0,0,0,0],
                           [0,0,0,0,0,0],
                           [0,0,0,0,0,0],
                           [0,0,0,0,0,0],
                           [0,0,0,0,0,0],] 
                         ]
        for x,y in self.v_walls:
            self.environment[1][y][int(x+0.5)]='|'
    def collition(self,taxi_next_pos):
        x_i_taxi,y_i_taxi=self.taxi_pos
        x_f_taxi,y_f_taxi=taxi_next_pos
        if x_i_taxi==x_f_taxi:
            for x,y in self.h_walls:
                if y < y_f_taxi and y > y_i_taxi:
                    return True
                elif y> y_f_taxi and y < y_i_taxi:
                    return True
        elif y_i_taxi==y_f_taxi:
            for x,y in self.v_walls:
                if y_i_taxi==y:
                    if x < x_f_taxi and x > x_i_taxi:
                        return True
                    elif x> x_f_taxi and x < x_i_taxi:
                        return True
        return False
    def iota(self):
        N,S,E,W,P,D=1,1,1,1,0,0
        if self.taxi_pos==self.pas_pos and not self.picked:
            N,S,E,W,P,D=0,0,0,0,1,0
            return np.array([N,E,S,W,P,D])
        if self.taxi_pos==self.des_pos and self.picked:
            N,S,E,W,P,D=0,0,0,0,0,1
            return np.array([N,E,S,W,P,D])
        for x,y in self.v_walls:
            if [self.taxi_pos[0]-1,self.taxi_pos[1]] == [x-0.5,y]:
                W=0
            if [self.taxi_pos[0]+1,self.taxi_pos[1]] == [x+0.5,y]:
                E=0
        for x,y in self.h_walls:
            if [self.taxi_pos[0],self.taxi_pos[1]-1] == [x,y-0.5]:
                S=0
            if [self.taxi_pos[0],self.taxi_pos[1]+1] == [x,y+0.5]:
                N=0
        #return np.array([N,E,S,W,P,D])*float(1/[N,E,S,W,P,D].count(1))    
        return np.array([N,E,S,W,P,D])
    def get_taxi_pos(self):
        if self.taxi_pos[0]==0:
            return 1,self.taxi_pos[1]
        if self.taxi_pos[0]==1:
            return 3,self.taxi_pos[1]
        if self.taxi_pos[0]==2:
            return 5,self.taxi_pos[1]
        if self.taxi_pos[0]==3:
            return 7,self.taxi_pos[1]
        if self.taxi_pos[0]==4:
            return 9,self.taxi_pos[1]
#############################
    
def main():
    env = TaxiGym_v1_0()
    print(env.reset())
    check_env(env)
    env.visualize=True
    run=True
    while run:
        for x in range(0,5):
            for y in range(0,5):
                env.picked=False
                env.taxi_pos=[x,y]
                env.build_env()
                iota=env.iota()
                obs=env.state()
                env.render()
                print(iota)
                time.sleep(2)
    
    
if __name__ == "__main__":
    main()