# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:11:55 2021

@author: Francisco Munguia
"""

import numpy as np
import pygame
from pygame.locals import *
from sys import exit
import math
import time

import gym
from gym import spaces


from vector import Vector2D
from constants import *
from animation import Animation
from entity import Entity
from mario import Mario
from qbox import Qbox
from brick import Brick
from slub import Slub


class Mario_v1_1(gym.Env):
    def __init__(self):
        self.visualize=False
        self.win = pygame.display.set_mode((display_width,display_height),0,32)
        self.clock = pygame.time.Clock()
        self.setter=0
        self.dt=0
        self.mario=Mario(mario_1_path,set_width(4),set_height(1))
        self.reducer=0
        self.limitreached=False
        self.action=0
        self.landscape=landscape
        self.floor_list=floor_list
        self.fixed_objects=fixed_objects
        self.animated_objects=animated_objects
        self.mario.brick_objects,self.mario.q_objects,self.mario.slub_objects=self.buildObjects(q_objects,brick_objects,slub_objects)
        self.reward=0
        self.done=False
        self.matrix_state=np.zeros((13,11))
        self.size_y=self.mario.Image.get_height()
        self.size_x=self.mario.Image.get_width()
        self.j=0
        self.last_reducer=0
        self.action_space= spaces.Discrete(2)
        #self.matrix_state.reshape(13,11,1)
        self.observation_space=spaces.Box(low=0, high=1, shape=(13,11,1), dtype=np.float32)
        self.actual_reward_episode=[]
        self.actual_reward=0
        self.act_avg=[]
        self.avg_reward=[]
        self.actual_epoch=0
        self.epoch_reward=[]
        self.actual_step=0
    def step(self,action):
        self.mario.move(action)
        self.mario.update(self.dt,self.reducer)
        #self.state()
        if self.mario.position.x >= 160 and self.reducer<set_width(190):
            self.mario.position.x=159
            self.reducer+=self.mario.speed*self.dt
            self.limitreached=True
        elif self.mario.position.x <= 80 and self.limitreached and self.reducer>0:
            self.mario.position.x=81
            self.reducer-=self.mario.speed*self.dt
        for qbox,active in self.mario.q_objects:
            qbox.update(self.dt,self.reducer)
        for brick,active in self.mario.brick_objects:
            brick.update(self.dt,self.reducer)
        for slub,active in self.mario.slub_objects:
            slub.update(self.dt,self.reducer)
        self.checkEvents()
        self.actual_step+=1
        self.actual_epoch+=1
        if self.actual_step>3000:
            self.actual_step=0
            self.done=True
        if self.visualize:
            self.render()
        self.actual_reward+=self.reward
        if self.done:
            self.act_avg.append(self.actual_reward)
            self.actual_reward=0
        if self.actual_epoch%2400==0 and self.actual_epoch>0:
            epoch=math.floor(self.actual_epoch/2400)
            reward=(sum(self.act_avg)/len(self.act_avg))
            print("Epoch:",epoch, "Reward: ",reward)
            self.avg_reward.append(reward)
        return self.state(),self.reward,self.done,{}
    
    def reset(self):
        self.mario.brick_objects,self.mario.q_objects,self.mario.slub_objects=self.buildObjects(q_objects,brick_objects,slub_objects)
        self.reward=0
        self.done=False
        self.mario.hit_block=False
        self.mario.finished_game=False
        self.mario.hit_slub=False
        self.mario.reset()
        self.mario.die=False
        self.reducer=0
        return self.matrix_state.reshape(13,11,1)
    
    def render(self):
        self.win.blit(bg, (0,0)) 
        self.drawLandscape()
        self.drawFixedObjects()
        self.drawFloor()
        self.drawAnimatedObjects()
        self.mario.render(self.win)
        for qbox,active in self.mario.q_objects:
            qbox.render(self.win)
        for brick,active in self.mario.brick_objects:
            brick.render(self.win)
        for slub,active in self.mario.slub_objects:
            slub.render(self.win)
        pygame.display.update()
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 run = False

    def state(self):
        self.matrix_state=np.zeros((13,11))
        x=self.mario.position.x
        y=self.mario.position.y+self.mario.Image.get_height()/2
        y_max=set_height(0)
        y_min=set_height(0)-12*self.mario.Image.get_height()
        total_height=y_max-y_min
        y_width=self.mario.Image.get_height()
        j=((y/(y_width)))-2
        self.j=int(j)
        i=0
        if self.j>12:
            return self.matrix_state.reshape(13,11,1)
        self.matrix_state[int(j),int(i)]=0.2+float(int((self.mario.reducer/self.size_x-int(self.mario.reducer/self.size_x))*10)/100.0)
        ###
        x_max=self.mario.position.x
        x_rlim=x_max+set_width(10)
        for j in floor_list:
            k=display_height-1.5*floor.get_height()+floor.get_height()/2
            k=(k/floor.get_height())-3
            obj_x=j-self.mario.reducer+floor.get_width()
            obj_h_max=k+floor.get_height()
            obj_h_min=k
            if obj_x>=x_max and obj_x<=x_rlim:
                i=(obj_x-x_max)/floor.get_width()
                self.matrix_state[int(k),int(i)]=0.4
            k=display_height-0.5*floor.get_height()+floor.get_height()/2
            k=(k/floor.get_height())-3
            if obj_x>=x_max and obj_x<=x_rlim:
                i=(obj_x-x_max)/floor.get_width()  
                self.matrix_state[int(k),int(i)]=0.4
        for objects in fixed_objects,self.mario.animated_objects_list:
            for j,k,obj,name in objects:
                obj_x=j-self.mario.reducer+obj.get_width()
                k=(k/obj.get_height())-2
                if obj_x>=x_max and obj_x<=x_rlim:
                    i=((j-self.mario.reducer-x_max)/self.mario.Image.get_width())
                    if name=="Slub":
                        self.matrix_state[int(k),int(i)]=0.6
                    elif name=="Bricks" or name=="Qs":
                        self.matrix_state[int(k),int(i)]=0.1
                    elif name=="bigpipe":
                        for z in range(0,4):
                            self.matrix_state[int(k+7+z),int(i)]=0.4
                            self.matrix_state[int(k+7+z),int(i+1)]=0.4
                    elif name=="pipe":
                        for z in range(0,3):
                            self.matrix_state[int(k+8+z),int(i)]=0.4
                            self.matrix_state[int(k+8+z),int(i+1)]=0.4
                    else:
                        self.matrix_state[int(k),int(i)]=0.4
        if (set_width(205)-self.mario.reducer-self.mario.position.x)/floor.get_width()<11:
            for z in range(0,13):
                self.matrix_state[int(z),int(int((set_width(205)-self.mario.reducer-self.mario.position.x)/floor.get_width()))]=0.9
        iota=self.iota()
        return self.matrix_state.reshape(13,11,1)
    def iota(self):
        iota=[0,0,0]
        if self.j<12:
            if self.matrix_state[self.j,1]==0.0:
                iota[2]=1
            if self.matrix_state[self.j+1,0]==0.4 or self.matrix_state[self.j+1,0]==0.1:
                iota[1]=1
            if self.matrix_state[self.j+1,0]==0.0:
                iota[0]=1
                iota[2]=1
        return iota

    def checkEvents(self):
        if self.mario.die:
            self.mario.die=False
            self.reward=-10
            self.last_reducer=0
            self.done=True
        elif self.mario.hit_block:
            self.mario.hit_block=False
            self.reward=self.mario.reward
        elif self.mario.hit_bricks:
            self.mario.hit_bricks=False
            self.reward=1
        elif self.mario.hit_slub:
            self.mario.hit_slub=False
            self.reward=1
        elif self.mario.finished_game:
            self.reward=1
            self.last_reducer=0
            self.mario.finished_game=False
            self.done=True
        else:
            self.reward=0
        if int(self.mario.reducer/self.mario.Image.get_width())>self.last_reducer:
            self.reward+=1
            self.last_reducer=int(self.mario.reducer/self.mario.Image.get_width())
        return        
    def drawLandscape(self):
        for j,k,obj in self.landscape:
            self.win.blit(obj, (j-self.reducer,k))
    def drawFloor(self):
        for i in range(0,len(self.floor_list)):
            self.win.blit(floor, (floor_list[i]-self.reducer,display_height-1.5*floor.get_height()))
            self.win.blit(floor, (floor_list[i]-self.reducer,display_height-0.5*floor.get_height()))
    def drawFixedObjects(self):
        for j,k,obj,name in self.fixed_objects:
            self.win.blit(obj, (j-self.reducer,k))
    def drawAnimatedObjects(self):
        for j,k,obj in self.animated_objects:
            self.win.blit(obj, (j-self.reducer,k))
    def buildObjects(self,objlist,objlist2,objlist3):
        q_objects=[]
        brick_objects=[]
        slub_objects=[]
        for x,y,sprites,active in objlist:
            q_objects.append([Qbox(x,y,sprites),active])
        for x,y,sprites in objlist2:
            active=True
            brick_objects.append([Brick(x,y,sprites),active])
        for x,y,sprites in objlist3:
            active=True
            slub_objects.append([Slub(x,y,sprites),active])
        return brick_objects,q_objects,slub_objects
            


def main():
    pass
    
if __name__ == "__main__":
    main()

