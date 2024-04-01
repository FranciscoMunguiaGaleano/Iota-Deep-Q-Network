# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:13:33 2021

@author: Francisco Munguia
"""
import pygame
from pygame.locals import *
#from vector import Vector2D
import random

print("Getting paths")
main_path='C:/Users/Francisco/Desktop/IEEE TNNLS/FlappyBirds gym/IMG/'


#Bird animations###########
bird_1_path=main_path+'bird_1.png'
bird_2_path=main_path+'bird_2.png'
bird_3_path=main_path+'bird_4.png'
#
######Landscape objects#####
background_image_path=main_path+'background.png'
floor_image_path=main_path+'base.png'
######Fixed Objects#####
pipe_image_path=main_path+'pipe.png'
########################
display_width=288
display_height=500
#####
ROWS=21
COLS=11
####
NOTHING=0
JUMP=1
###

#####
#STOP=Vector2D(0,0)
#RIGHT=Vector2D(1,0)
#RIGHT_UP=Vector2D(1,-1)
#RIGHT_DOWN=Vector2D(1,1)
#LEFT=Vector2D(-1,0)
#LEFT_UP=Vector2D(-1,-1)
#LEFT_DOWN=Vector2D(-1,1)
#UP=Vector2D(0,-1)
#DOWN=Vector2D(0,1)
#####################
def set_height(factor):
    return int(display_height-1.5*agent.get_height()-factor*agent.get_height())
def set_width(factor):
    return int(factor*agent.get_width())
#####################

win = pygame.display.set_mode((display_width,display_height),0,32)

#####################

agent=pygame.image.load(bird_1_path).convert_alpha()
#hill=pygame.image.load(hill_image_path).convert_alpha()
#castle=pygame.image.load(castle_image_path).convert_alpha()
#cloud=pygame.image.load(cloud_image_path).convert_alpha()
#double_cloud=pygame.image.load(double_cloud_image_path).convert_alpha()
#bush=pygame.image.load(bush_image_path).convert_alpha()
pipe=pygame.image.load(pipe_image_path).convert_alpha()
#bigpipe=pygame.image.load(big_pipe_image_path).convert_alpha()
#block=pygame.image.load(block_image_path).convert_alpha()

#brick=pygame.image.load(brick_image_path).convert_alpha()
#q1=pygame.image.load(q1_image_path).convert_alpha()
#q2=pygame.image.load(q2_image_path).convert_alpha()
#q3=pygame.image.load(q3_image_path).convert_alpha()
#q4=pygame.image.load(q4_image_path).convert_alpha()
#flag=pygame.image.load(flag_image_path).convert_alpha()
#exp1=pygame.image.load(exp_1_path).convert_alpha()
#exp2=pygame.image.load(exp_21_path).convert_alpha()
#exp3=pygame.image.load(exp_22_path).convert_alpha()
#exp4=pygame.image.load(exp_23_path).convert_alpha()
#exp5=pygame.image.load(exp_3_path).convert_alpha()

#slub1=pygame.image.load(slub1_path).convert_alpha()
#slub2=pygame.image.load(slub2_path).convert_alpha()
#slub3=pygame.image.load(slub3_path).convert_alpha()

floor=pygame.image.load(floor_image_path)
#not_floor=[68,69,85,86,87,151,152]
#not_floor=[68,69,85,86,87]
#floor_list=floor_constructor(not_floor)
bg = pygame.image.load(background_image_path).convert_alpha()
#not_floor=[[0,0],[10,10]]

lista=range(4, 12)
level=[]
random.seed(6)
for i in range(0,50):
    level.append(random.sample(lista, 1)[0])
#################################
index=0 
fixed_objects=[]   
for pipes in level:
    fixed_objects.append([set_width(10+(5*index)),set_height(pipes),pipe,"pipe",0])
    fixed_objects.append([set_width(10+(5*index)),set_height(pipes)-450,pygame.transform.rotate(pipe, 180),"invpipe",0])
    index+=1
floor_list=[]
for i in range(0,40):
    floor_list.append(i*display_width)
#fixed_objects=[[set_width(10),set_height(5),pipe,"pipe"],
#               [set_width(16),set_height(6),pipe,"pipe"],]
