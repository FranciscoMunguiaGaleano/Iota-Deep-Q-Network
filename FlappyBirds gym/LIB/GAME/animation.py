# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:39:55 2021

@author: Francisco Munguia
"""

class Animation(object):
    def __init__(self,animType):
        self.animType= animType
        self.frames=[]
        self.current_frame=0
        self.Finished=False
        self.speed=0
        self.dt=0
    def reset(self):
        self.current_frame=0
        self.Finished=False
    def addFrame(self,frame):
        self.frames.append(frame)
    def update(self,dt):
        if self.animType =="loop":
            self.loop(dt)
        elif self.animType == "once":
            self.once(dt)
        elif self.animType == "static":
            self.current_frame=0
        #print(self.current_frame)
        return self.frames[self.current_frame]
    def nextFrame(self,dt):
        self.dt += dt
        if self.dt >=(1.0/self.speed):
            self.current_frame+=1
            self.dt =0
    def loop(self,dt):
        self.nextFrame(dt)
        if self.current_frame == len(self.frames):
            self.current_frame=0
    def once(self,dt):
        if not self.Finished:
            if self.current_frame < len(self.frames) - 1:
                self.nextFrame(dt)
            else:
                self.Finished=True