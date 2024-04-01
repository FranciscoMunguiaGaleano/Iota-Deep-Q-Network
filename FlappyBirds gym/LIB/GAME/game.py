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
from pygame.locals import *
from sys import exit
import math
import time


from vector import Vector2D
from constants import *
from animation import Animation
from entity import Entity
from bird import Bird

import gym
from gym import spaces
import yaml

class Flappy_v1_0(gym.Env):
    def __init__(self):
        self.visualize=False
        self.win = pygame.display.set_mode((display_width,display_height),0,32)
        self.clock = pygame.time.Clock()
        self.setter=0
        self.dt=0
        self.bird=Bird(bird_1_path,set_width(2),set_height(10))
        self.reducer=0
        self.limitreached=False
        self.action=0
        #self.landscape=landscape
        #self.floor_list=floor_list
        self.fixed_objects=fixed_objects
        #self.animated_objects=animated_objects
        #self.mario.brick_objects,self.mario.q_objects,self.mario.slub_objects=self.buildObjects(q_objects,brick_objects,slub_objects)
        self.reward=0
        self.done=False
        self.matrix_state=np.zeros((ROWS,COLS))
        self.size_y=self.bird.Image.get_height()
        self.size_x=self.bird.Image.get_width()
        self.j=0
        self.i=0
        self.last_reducer=0
        self.score=0
        self.font = pygame.font.SysFont('comicsans', 30)
        self.vidas=10
        self.action_space= spaces.Discrete(2)
        #self.matrix_state.reshape(13,11,1)
        self.observation_space=spaces.Box(low=0, high=1, shape=(ROWS,COLS,1), dtype=np.float32)
        self.actual_reward_episode=[]
        self.actual_reward=0
        self.act_avg=[]
        self.avg_reward=[]
        self.actual_episode=0
        self.actual_step=0
        self.actual_epoch=0
    def step(self,action):
        self.bird.move(action)
        self.bird.update(self.dt,self.reducer)
        self.reducer+=self.bird.speed*self.dt
        #self.state()
        self.checkEvents()
        if self.visualize:
            self.render()
        self.actual_step+=1
        self.actual_epoch+=1
        if self.actual_step>3000:
            self.actual_step=0
            self.done=True
        self.actual_reward+=self.reward
        if self.done:
            self.act_avg.append(self.actual_reward)
            self.actual_reward=0
        if self.actual_epoch%2400==0 and self.actual_epoch>0:
            epoch=math.floor(self.actual_epoch/2400)
            try:
                reward=(sum(self.act_avg)/len(self.act_avg))
                self.avg_reward.append(reward)
                print("Epoch:",epoch, "Reward: ",reward)
            except:
                print("Epoch:",epoch)
            
# =============================================================================
#         self.actual_reward+=self.reward
#         if self.done:
#             self.actual_episode+=1
#             self.act_avg.append(self.actual_reward)
#             self.avg_reward.append(sum(self.act_avg)/len(self.act_avg))
#             self.actual_reward=0
#             print("Episode: ",self.actual_episode, "Avg: ",self.avg_reward[-1])
# =============================================================================
        
        return self.state(),self.reward,self.done,{} 
    def reset(self):
        #self.bird.brick_objects,self.bird.q_objects,self.bird.slub_objects=self.buildObjects(q_objects,brick_objects,slub_objects)
        
        #level=[]
        #for i in range(0,50):
        #    level.append(random.sample(lista, 1)[0])
              #################################
        #index=0 
        #fixed_objects=[]   
        #for pipes in level:
        #    fixed_objects.append([set_width(10+(5*index)),set_height(pipes),pipe,"pipe",0])
        #    fixed_objects.append([set_width(10+(5*index)),set_height(pipes)-450,pygame.transform.rotate(pipe, 180),"invpipe",0])
        #    index+=1
        #idx=0
        self.fixed_objects=fixed_objects
        idx=0
        for obj in enumerate(self.fixed_objects):
            self.fixed_objects[idx][4]=0
            idx+=1
        self.score=0
        self.reward=0
        self.done=False
        self.bird.hit_block=False
        self.bird.finished_game=False
        self.bird.hit_slub=False
        self.bird.reset()
        self.bird.die=False
        self.reducer=0
        return self.matrix_state.reshape(ROWS,COLS,1)
    def render(self):
        self.win.blit(bg, (0,0)) 
        self.drawLandscape()
        self.drawFixedObjects()
        self.drawFloor()
        win.blit(self.font.render(str(self.score), 1, (255,255,255)), ((display_width/2)-15, 40))
        self.drawAnimatedObjects()
        self.bird.render(self.win) 
        for qbox,active in self.bird.q_objects:
            qbox.render(self.win)
        for brick,active in self.bird.brick_objects:
            brick.render(self.win)
        for slub,active in self.bird.slub_objects:
            slub.render(self.win)
        pygame.display.update()
    def state(self):
        self.matrix_state=np.zeros((ROWS,COLS))
        x=self.bird.position.x+self.bird.Image.get_width()/2
        y=self.bird.position.y-self.bird.Image.get_height()/2
        #display_width=288
        #display_height
        y_max=display_height
        y_min=0
        total_height=y_max-y_min
        y_width=self.bird.Image.get_height()
        j=((y/(y_width)))
        self.j=int(j)
        i=x/self.bird.Image.get_width()
        self.i=int(i)
        #if self.j>:
        #    return self.matrix_state.reshape(ROWS,COLS,1)
        #print(0.2+float(int((self.mario.reducer/self.size_x-int(self.mario.reducer/self.size_x))*100)/1000.0))
        #print(0.2+float(int((self.bird.reducer/self.size_x-int(self.bird.reducer/self.size_x))*10)/100.0)+float(int((j-int(j))*10)/1000.0))
        self.matrix_state[int(j),int(i)]=0.2+float(int((self.bird.reducer/self.size_x-int(self.bird.reducer/self.size_x))*10)/100.0)+float(int((j-int(j))*10)/1000.0)
        ###
        x_max=self.bird.position.x
        x_rlim=x_max+display_width

        for j,k,obj,name,point in fixed_objects:
            obj_x=j-self.bird.reducer+obj.get_width()       
            if obj_x>=x_max and obj_x<=x_rlim:
                i=((j-self.reducer)/self.bird.Image.get_width())
                if name=="invpipe":
                    for row in range(0,int(((k+obj.get_height())/y_width))+1):
                        self.matrix_state[row,int(i)]=0.6
                        self.matrix_state[row,int(i)+1]=0.6

                elif name=="pipe":
                    for row in range(int(k/self.bird.Image.get_height())-1,ROWS-2):
                        self.matrix_state[row,int(i)]=0.4
                        self.matrix_state[row,int(i)+1]=0.4
                else:pass
        for i in range(0,COLS):
            self.matrix_state[ROWS-1,int(i)]=0.1
            self.matrix_state[ROWS-2,int(i)]=0.1
            self.matrix_state[ROWS-3,int(i)]=0.1
        #matrix=self.matrix_state*10
        #matrix=matrix.astype(int)
        #print(matrix)
        #print(self.matrix_state[self.j,0])
        #print(self.matrix_state[self.j,1])
        iota=self.iota()
        #print(iota)
        return self.matrix_state.reshape(ROWS,COLS,1)
    def iota(self):
        #0,1
        #stay,fly
        iota=[1,1]
        #RIGHT UP
        if self.matrix_state[self.j,self.i+1]==0.6 or self.matrix_state[self.j,self.i+2]==0.6 or self.matrix_state[self.j,self.i+3]==0.6:
            iota[1]=0
        if self.matrix_state[self.j-1,self.i+1]==0.6 or self.matrix_state[self.j-1,self.i+2]==0.6 or self.matrix_state[self.j-1,self.i+3]==0.6:
            iota[1]=0
        if self.matrix_state[self.j-1,self.i-1]==0.6 or self.matrix_state[self.j-1,self.i-2]==0.6:
            iota[1]=0
        #UP    
        if self.matrix_state[self.j-1,self.i]==0.6 or self.matrix_state[self.j-1,self.i]==0.6:
            iota[1]=0
        ##RIGHT DOWN
        if self.matrix_state[self.j,self.i+1]==0.4 or self.matrix_state[self.j,self.i+2]==0.4 or self.matrix_state[self.j,self.i+3]==0.4:
            iota[0]=0
        if self.matrix_state[self.j+1,self.i+1]==0.4 or self.matrix_state[self.j+1,self.i+2]==0.4 or self.matrix_state[self.j+1,self.i+3]==0.4:
            iota[0]=0
        if self.matrix_state[self.j+1,self.i-1]==0.4 or self.matrix_state[self.j+1,self.i-2]==0.4:
            iota[0]=0
        #DOWN
        if self.matrix_state[self.j+1,self.i]==0.4 or self.matrix_state[self.j+2,self.i]==0.4 or self.matrix_state[self.j+1,self.i]==0.1 or self.matrix_state[self.j+2,self.i]==0.1:
            iota[0]=0
        return iota
    def dummy_iota(self):
        #0,1
        #stay,fly
        iota=[1,1]
        #RIGHT UP
        if self.matrix_state[self.j,self.i+1]==0.6 or self.matrix_state[self.j,self.i+2]==0.6 or self.matrix_state[self.j,self.i+3]==0.6:
            iota[1]=0
        if self.matrix_state[self.j-1,self.i+1]==0.6 or self.matrix_state[self.j-1,self.i+2]==0.6 or self.matrix_state[self.j-1,self.i+3]==0.6:
            iota[1]=0
        if self.matrix_state[self.j-1,self.i-1]==0.6 or self.matrix_state[self.j-1,self.i-2]==0.6:
            iota[1]=0
        #UP    
        if self.matrix_state[self.j-1,self.i]==0.6 or self.matrix_state[self.j-1,self.i]==0.6:
            iota[1]=0
        ##RIGHT DOWN
        if self.matrix_state[self.j,self.i+1]==0.4 or self.matrix_state[self.j,self.i+2]==0.4 or self.matrix_state[self.j,self.i+3]==0.4:
            iota[0]=0
        if self.matrix_state[self.j+1,self.i+1]==0.4 or self.matrix_state[self.j+1,self.i+2]==0.4 or self.matrix_state[self.j+1,self.i+3]==0.4:
            iota[0]=0
        if self.matrix_state[self.j+1,self.i-1]==0.4 or self.matrix_state[self.j+1,self.i-2]==0.4:
            iota[0]=0
        #DOWN
        if self.matrix_state[self.j+1,self.i]==0.4 or self.matrix_state[self.j+2,self.i]==0.4 or self.matrix_state[self.j+1,self.i]==0.1 or self.matrix_state[self.j+2,self.i]==0.1:
            iota[0]=0
        return iota

    def checkEvents(self):

        self.collitions()
        if self.bird.die:
            self.vidas-=1
            #print(self.vidas)
            #self.done=False
            #print("game over")
            self.done=True
            self.bird.die=False
            self.reward=-10
            self.last_reducer=0
        elif self.points()>self.score:
            self.score+=1
            self.reward=1
            if self.score>49:
                self.bird.finished_game=True
        elif self.bird.finished_game:
            #print("Finished")
            self.reward=20
            self.last_reducer=0
            self.bird.finished_game=False
            self.done=True
            #print(self.reward)
        else:
            self.reward=0
        if self.reward!=0:pass
            #print(self.reward)    
        return        

        
    def drawLandscape(self):pass
    def drawFloor(self):
        for i in floor_list:
            if (i-self.reducer)<display_width*1.5:
                self.win.blit(floor, (i-self.reducer,display_height-0.5*floor.get_height()))
    def drawFixedObjects(self):
        for j,k,obj,name,point in self.fixed_objects:
            if (j-self.reducer)<display_width*1.5:
                self.win.blit(obj, (j-self.reducer,k))
    def drawAnimatedObjects(self):pass
    def buildObjects(self,objlist,objlist2,objlist3):
        q_objects=[]
        brick_objects=[]
        slub_objects=[]
        return brick_objects,q_objects,slub_objects
    def collitions(self):
        colition=False
        birdy=pygame.Rect(self.bird.Image.get_rect(x=self.bird.position.x,y=self.bird.position.y))
        for j,k,obj,name,point in self.fixed_objects:
            if (j-self.reducer)<display_width*1.5:
                tubo=pygame.Rect(obj.get_rect(x=j-self.reducer,y=k))
                if birdy.colliderect(tubo):
                    #print("Colition")
                    self.bird.die=True
        return colition
    def points(self):
        idx=0
        for objt in self.fixed_objects:
            j=objt[0]
            k=objt[1]
            obj=objt[2]
            #point=objt[4]
            if (j-self.reducer+obj.get_width())<self.bird.position.x and (j-self.reducer)>0:
                self.fixed_objects[idx][4]=1
            idx+=1
        score=0
        for obj in self.fixed_objects:
            score+=obj[4]
        return score/2
    
def main():
    pygame.init()
    pygame.display.set_caption("Taco Bird")
    
    custom_callback=StopTrainingOnMaxEpisodes(max_episodes=1000000, verbose=1)
    env = Flappy_v1_0()
    env.visualize=True
    t=env.clock.tick(30)
    env.dt=t/1000.0
    
    print("Training started")
    model = DQN("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=200000000,log_interval=4,callback=custom_callback)
    model.save("deepq_flappy_1")

    with open(r'test_1.yaml', 'w') as outfile:
                           data={'avr_r_1':env.act_avg,
                                  'avr_r_2':env.avg_reward}
                           yaml.dump(data, outfile, default_flow_style=False)
    print("Training finshed")
    #del model # remove to demonstrate saving and loading
    
    model = DQN.load("deepq_flappy_!")
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
    
    
# =============================================================================
#     env=Flappy_v1_0()
#     run=True
#     while run:
#         t=env.clock.tick(30)
#         #t=0.033
#         #time.sleep(0.01)
#         env.dt=t/1000.0
#         #dt=0.033
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#         keys = pygame.key.get_pressed()
#            
#         if keys[pygame.K_SPACE]:
#             action=JUMP
#         else: 
#             action=0 
#         iota=env.iota()
#         #print(iota)
#         env.step(action)
#         env.render()
#         if env.done:
#             #time.sleep(1.5)
#             env.reset()
#     pygame.quit()
# =============================================================================
    
if __name__ == "__main__":
    main()