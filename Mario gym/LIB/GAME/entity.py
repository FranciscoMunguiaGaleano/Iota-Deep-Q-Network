# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:41:17 2021

@author: Francisco Munguia
"""
from constants import *

class Entity(object):
    def __init__(self,spritesheet,x,y):
        self.name=""
        self.direction=STOP
        self.speed=100#0.033 10 pixels= 600 pixels in one second
        self.radius = 10
        self.collideRadius=5
        self.target=Vector2D(0,0)
        self.visible=True
        self.spritesheet=spritesheet
        self.position=Vector2D(x,y)
        self.image=None
        self.last=0
        self.altura=12
    def setPosition(self,x,y):
        self.position=Vector2D(x,y)
    def update(self,dt):
        self.position += self.direction*self.speed*dt
    def moveBySelf(self):
        pass
    def reverseDirection(self):
        if self.direction is UP: self.direction=DOWN
        elif self.direction is DOWN: self.direction=UP
        elif self.direction is LEFT: self.direction=RIGHT
        elif self.direction is RIGHT: self.direction=LEFT
    def render(self,win):
        if self.visible:
            if self.image is not None:
                win.blit(self.image,(self.position.x,self.position.y))
    def getImage(self,image_path):
        return pygame.image.load(image_path).convert_alpha()
    def flipImage(self,image_path):
        return pygame.transform.flip(self.getImage(image_path), True, False)