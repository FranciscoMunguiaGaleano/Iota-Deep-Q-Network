# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 16:48:28 2021

@author: C1982450
"""

from entity import Entity
from constants import *
from animation import Animation
import time

class Bird(Entity):
    def __init__(self,spritesheet,x,y):
        Entity.__init__(self,spritesheet,x,y)
        self.name="Taco"
        self.startImage=self.getImage(bird_1_path)
        self.Image=self.startImage
        self.animation=None
        self.animations={}
        self.defineAnimations()
        self.action=NOTHING
        self.altura=0
        self.strong_jump=7
        self.strong_vel=200
        self.weak_jump=7
        self.salto=False
        self.suelo=True
        self.bajar=False
        self.aceleration=20.0
        self.q_objects=[]
        self.brick_objects=[]
        self.slub_objects=[]
        self.colideListDown=[]
        self.colideListUp=[]
        self.colideListA=[]
        self.colideListB=[]
        self.colideListHorR=[]
        self.colideListHorL=[]
        self.h=1
        self.reducer=0
        self.animated_objects_list=[]
        self.colideListC=[]
        self.die=False
        self.finished_game=False
        self.hit_slub=False
        self.hit_block=False
        self.reward=0
        self.hit_bricks=False

    def reset(self):
        self.setStartPosition()
        self.Image=self.startImage
        self.finished_game=False
    ###
    def getDownObjects(self,x_i,x_f,y):
        objs=[]
        for j,k,obj,name,ponit in fixed_objects:
            if (self.position.x>(j-self.reducer) and self.position.x<(j-self.reducer+obj.get_width())) or (x_f>(j-self.reducer) and x_f<(j-self.reducer+obj.get_width())):
                objs.append([j-self.reducer,k,obj]) 
        for j,k,obj,name in self.animated_objects_list:
            if (j-self.reducer)>=x_i and (j-self.reducer)<=x_f and k>y:
                objs.append([j-self.reducer,k,obj])
        return objs
    def getUpObjects(self,x_i,x_f,y):
        objs=[]  
        return objs
    def getDownObjectsA(self,x_i,x_f,y):
        objs=[]
        objs1=[]  
        index=0
        for obj,active in self.slub_objects:
            j=obj.x
            k=obj.y
            if (j-self.reducer)>=x_i and (j-self.reducer)<=x_f and k+4>=y:
                #print(index)
                objs.append(index)
            index+=1
        return objs
    def getUpObjectsA(self,x_i,x_f,y):
        objs=[]
        objs1=[]  
        index=0
        for obj,active in self.q_objects:
            j=obj.x
            k=obj.y
            if (j-self.reducer)>=x_i and (j-self.reducer)<=x_f and k<y:
                objs.append(index)
            index+=1
        index=0
        for obj,active in self.brick_objects:
            j=obj.x
            k=obj.y
            if (j-self.reducer)>=x_i and (j-self.reducer)<=x_f and k<y:
                if obj.visible:
                    objs1.append(index)
            index+=1
        return objs,objs1
    def listLatObj(self):
        self.animated_objects_list=[]
        for objlist in [self.q_objects,self.brick_objects,self.slub_objects]:
            for obj,active in objlist:
                if obj.visible:
                    self.animated_objects_list.append([obj.x,obj.y,obj.Image,obj.name])
    def getLatObjects(self):
        objsr=[]
        objsl=[]
        x_max=self.position.x+self.Image.get_width()
        x_rlim=x_max+20
        x_min=self.position.x
        x_llim=x_min-20
        y_min=self.position.y-self.Image.get_height()
        y_max=y_min+self.Image.get_height()
        for objects in fixed_objects,self.animated_objects_list:
            x_max=self.position.x+self.Image.get_width()
            x_rlim=x_max+20
            x_min=self.position.x
            x_llim=x_min-20
            y_min=self.position.y
            y_max=y_min+self.Image.get_height()
            for j,k,obj,name,point in objects:
                obj_x=j-self.reducer
                obj_h_max=k+obj.get_height()
                obj_h_min=k
                if obj_x>=x_max and obj_x<=x_rlim and obj_h_min+1<y_max and obj_h_max-1>y_min:
                    objsr.append([j,k,obj,name])
                #if obj_x<=x_min-self.Image.get_width() and obj_x>=x_llim and obj_h_min+1<y_max and obj_h_max-1>y_min:
                obj_x+=obj.get_width()
                if obj_x<=x_min and obj_x>=x_llim and obj_h_min+1<y_max and obj_h_max-1>y_min:
                    objsl.append([j,k,obj,name])
        return objsl,objsr
    ###
    def letfLimit(self,dt):
        if self.position.x-self.speed*dt<0:
            return True
        return False
    def rightLimit(self,dt):
        if self.position.x+self.speed*dt>2*(display_width/3)-10:
            return True
        return False
    ###
    def update(self,dt,reducer):
        self.reducer=reducer
        self.listLatObj()
        self.colideListDown=self.getDownObjects(self.position.x-self.Image.get_width(),self.position.x+self.Image.get_width(),self.position.y)
        self.colideListUp=self.getUpObjects(self.position.x-self.Image.get_width(),self.position.x+self.Image.get_width(),self.position.y)
        self.colideListUpA,self.colideListUpB=self.getUpObjectsA(self.position.x-self.Image.get_width(),self.position.x+self.Image.get_width(),self.position.y)
        self.colideListDownA=self.getDownObjectsA(self.position.x-self.Image.get_width(),self.position.x+self.Image.get_width(),self.position.y+self.Image.get_height())
        self.colideListHorL,self.colideListHorR=self.getLatObjects()
        self.visible=True
        self.hitBottom()
        

        if self.direction==UP:
            self.salto=True
            self.altura=0
        else:
            self.direction=STOP
        

        if self.salto:
            if self.altura<self.strong_jump and not self.hitUp():
                t=self.strong_jump-self.altura
                vel=t*self.aceleration
                self.position.y+=-vel*dt
                colitionr,x=self.colitionR(dt,reducer)
                colitionl,x=self.colitionL(dt,reducer)
                if not colitionr or not colitionl:
                    self.position+= self.direction*self.speed*dt
                self.altura+=1
            else:
                self.salto=False
                self.direction.y=0
                self.altura=0
            
        #colition,y=self.colideD(dt)    
        else:
                #self.h+=1
                vel=250
                self.position.y+=vel*dt
                #colition,x=self.colitionR(dt,reducer)
                #colition_l,x=self.colitionL(dt,reducer)
                #if not colition and not colition_l:
                #    self.position+= self.direction*self.speed*dt
        #elif colition and not self.salto:
        #    self.position.y=y
        #    self.h=1
        if self.position.y<20:
            self.position.y=20
        self.updateAnimation(dt)
        colition,x=self.colitionR(dt,reducer)
        colition,x=self.colitionL(dt,reducer)
        if self.die:
            for i in range(0,10):
                self.updateAnimation(dt)
        if self.rightLimit(dt):
            self.finished_game=True
        
        
    def move(self,action):
        if action == JUMP:
            self.direction=UP
        else:
            self.direction=STOP
    def colideD(self,dt):
        #self.rect = self.Image.get_rect(x=self.position.x, y=self.position.y)
        if len(self.colideListDownA)>0:     
            for index in self.colideListDownA:
                target,active=self.slub_objects[index]
                j=target.x
                k=target.z
                #if self.rect.colliderect(target.Image.get_rect(x=j-self.reducer, y=k)):
                if self.position.y+self.Image.get_height() + 5.0*dt> k:
                    self.slub_objects[index][0].move(1)
                    self.salto=True
                    self.hit_slub=True
                    #self.colideListDown.pop(i)
        if len(self.colideListDown)>0:
            for j,k,target in self.colideListDown:
                if self.position.y+self.Image.get_height() + 1.0*dt> k:
                    return True,k-self.Image.get_height()
        
        else:
            colition=False
        return False,0
    def colitionR(self,dt,reducer):
        if len(self.colideListHorR)>0:
            for j,k,target,name in self.colideListHorR:
                if j+2-reducer<self.position.x+self.Image.get_width() + self.speed*dt:
                    if name=="Slub":
                        self.die=True
                    return True,(j-reducer)-self.Image.get_width()
        return False,0
    def colitionL(self,dt,reducer):
        if len(self.colideListHorL)>0:
            for j,k,target,name in self.colideListHorL:
                if (self.position.x - self.speed*dt) < j-reducer+target.get_width(): 
                    if name=="Slub":
                        self.die=True
                    return True,(j-reducer+target.get_width())
        return False,0

    def hitUp(self):
        self.rect = self.Image.get_rect(x=self.position.x, y=self.position.y)
        colition=False
        if len(self.colideListUpA)>0:     
            for index in self.colideListUpA:
                target,active=self.q_objects[index]
                j=target.x
                k=target.y
                if self.rect.colliderect(target.Image.get_rect(x=j-self.reducer, y=k)):
                    self.q_objects[index][0].move(1)
                    self.reward=self.q_objects[index][0].reward
                    colition= True
                    self.hit_block=True
        else:
            colition=False
        colition1=False
        if len(self.colideListUpB)>0:     
            for index in self.colideListUpB:
                target,active=self.brick_objects[index]
                j=target.x
                k=target.y
                if self.rect.colliderect(target.Image.get_rect(x=j-self.reducer, y=k)):
                    self.brick_objects[index][0].move(1)
                    colition1= True
                    self.hit_bricks=True
        else:
            colition1=False
        if colition or colition1:
            colition=True
        else:
            colition=False
        return colition
    def hitTop(self):
        if self.position.y < 5:
            return True
        else:
            return False
        return False
    def hitBottom(self):
        if self.position.y +self.Image.get_height()>= display_height-60:
            self.die=True
        return 
    def setStartPosition(self):
        self.direction=STOP
        self.setPosition(set_width(2),set_height(10))
    def defineAnimations(self):
        #Fly
        animation= Animation("loop")
        animation.speed=30
        animation.addFrame(self.getImage(bird_1_path))
        animation.addFrame(self.getImage(bird_2_path))
        animation.addFrame(self.getImage(bird_3_path))
        self.animations["fly"]=animation
        #Fall
        animation= Animation("static")
        animation.speed=10
        animation.addFrame(self.getImage(bird_2_path))
        self.animations["fall"]=animation
    def updateAnimation(self,dt):
        #colide,_=self.colideD(dt)
        if self.salto:
            self.animation =self.animations["fly"]
        else:
            self.animation =self.animations["fall"]
        self.image=self.animation.update(dt)