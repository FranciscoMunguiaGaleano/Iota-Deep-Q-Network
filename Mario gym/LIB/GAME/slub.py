# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 13:50:31 2021

@author: Francisco Munguia
"""
from entity import Entity
from constants import *
from animation import Animation

class Slub(Entity):
    def __init__(self,x,y,spritesheet):
        Entity.__init__(self,spritesheet,x,y)
        self.name="Slub"
        self.spritesheets=spritesheet
        self.startImage=spritesheet[0]
        self.Image=self.startImage
        self.animation=None
        self.animations={}
        self.defineAnimations()
        self.action=0
        self.vel=20
        self.subir=False
        self.bajar=False
        self.aceleration=9.84
        self.behavior=0
        self.gift=None
        self.x=x
        self.y=y
        self.animtime=10
        self.max=self.x+35
        self.min=self.x-35
        self.dir=0
        self.z=y
    def reset(self):
        self.setStartPosition()
        self.Image=self.startImage
    def update(self,dt,reducer):
        #self.visible=True
        self.updateAnimation(dt)
        if self.behavior==0:
            if self.dir==0 and self.x>self.min:
                self.x-=self.vel*dt
            else:
                self.dir=1
                if self.x<self.max:
                    self.x+=self.vel*dt
                else:
                    self.dir=0
        if self.behavior==1:
            self.position.x=self.x-reducer
            if self.animtime>5:
                self.position.y=self.y+10
                self.animtime-=1
            elif self.animtime>0 and self.animtime<6:
                self.position.y=self.y+10
                self.animtime-=1
            else:
                self.behavior=2
        else:
            self.position.x=self.x-reducer
            self.position.y=self.y
        if self.animations["explode"].Finished:
            #print("Finished")
            self.behavior=3
    def move(self,action):
        if self.animtime>0:
            self.behavior=action
            self.z=500
    def defineAnimations(self):
        #WALK RIGHT
        animation= Animation("loop")
        animation.speed=7.5
        animation.addFrame(self.spritesheets[0])
        animation.addFrame(self.spritesheets[1])
        self.animations["walking"]=animation
        animation=Animation("once")
        animation.speed=10
        animation.addFrame(self.spritesheets[3])
        animation.addFrame(self.spritesheets[4])
        animation.addFrame(self.spritesheets[5])
        animation.addFrame(self.spritesheets[6])
        animation.addFrame(self.spritesheets[7])
        self.animations["explode"]=animation
        animation= Animation("once")
        animation.speed=7.5
        animation.addFrame(self.spritesheets[2])
        self.animations["pushed"]=animation
    def updateAnimation(self,dt):
        #print(self.behavior)
        if self.behavior == 0:
            self.animation =self.animations["walking"]
        elif self.behavior == 1:
            self.animation =self.animations["pushed"]
            #self.y+=30
        elif self.behavior == 2:
            self.animation =self.animations["explode"]
        else:
            self.visible=False
        self.image=self.animation.update(dt)
