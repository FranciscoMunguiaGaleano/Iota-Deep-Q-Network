# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:34:05 2021

@author: Francisco Munguia
"""
from entity import Entity
from constants import *
from animation import Animation

class Brick(Entity):
    def __init__(self,x,y,spritesheet):
        Entity.__init__(self,spritesheet,x,y)
        self.name="Bricks"
        self.spritesheets=spritesheet
        self.startImage=spritesheet[0]
        self.Image=self.startImage
        self.animation=None
        self.animations={}
        self.defineAnimations()
        self.action=0
        self.vel=10
        self.subir=False
        self.bajar=False
        self.aceleration=9.84
        self.behavior=0
        self.gift=None
        self.x=x
        self.y=y
        self.animtime=10
    def reset(self):
        self.setStartPosition()
        self.Image=self.startImage
    def update(self,dt,reducer):
        #self.visible=True
        self.updateAnimation(dt)
        if self.behavior==1:
            self.position.x=self.x-reducer
            if self.animtime>5:
                self.position.y=self.y-0.1
                self.animtime-=1
            elif self.animtime>0 and self.animtime<6:
                self.position.y=self.y+0.1
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
    def defineAnimations(self):
        #WALK RIGHT
        animation= Animation("loop")
        animation.speed=7.5
        animation.addFrame(self.spritesheets[0])
        self.animations["changing"]=animation
        animation=Animation("once")
        animation.speed=10
        animation.addFrame(self.spritesheets[1])
        animation.addFrame(self.spritesheets[2])
        animation.addFrame(self.spritesheets[3])
        animation.addFrame(self.spritesheets[4])
        animation.addFrame(self.spritesheets[5])
        self.animations["explode"]=animation
    def updateAnimation(self,dt):
        #print(self.behavior)
        if self.behavior == 0 or self.behavior == 1:
            self.animation =self.animations["changing"]
        elif self.behavior == 2:
            self.animation =self.animations["explode"]
        else:
            self.visible=False
        self.image=self.animation.update(dt)
