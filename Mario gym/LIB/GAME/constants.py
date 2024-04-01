# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:13:33 2021

@author: Francisco Munguia
"""
import pygame
from pygame.locals import *
from vector import Vector2D

import os

main_path='C:/Users/Francisco/Desktop/IEEE TNNLS/Mario gym/Images/'

#Mario animations###########
mario_1_path=main_path+'mario1.png'
mario_2_path=main_path+'mario2.png'
mario_3_path=main_path+'mario3.png'
mario_4_path=main_path+'mario4.png'
mario_jump  =main_path+'mario5.png'
mario_die  =main_path+'mariodie.png'
######Landscape objects#####
background_image_path=main_path+'background-2.png'
agent_image_path=main_path+'mario1.png'
cloud_image_path=main_path+'cloud.png'
double_cloud_image_path=main_path+'doubleclouds.png'
hill_image_path=main_path+'hill.png'
bush_image_path=main_path+'bush-1.png'
castle_image_path=main_path+'castle.png'

######Fixed Objects#####
big_pipe_image_path=main_path+'pipe-big.png'
pipe_image_path=main_path+'pipe.png'
block_image_path=main_path+'platform-air.png'
floor_image_path=main_path+'platform-top.png'
######Animated fixed objects#######
brick_image_path=main_path+'platform-brick.png'
q1_image_path=main_path+'platform-q.png'
q2_image_path=main_path+'platform-q1.png'
q3_image_path=main_path+'platform-q2.png'
q4_image_path=main_path+'platform-q3.png'
flag_image_path=main_path+'flagpole.png'
exp_1_path=main_path+'exp1.png'
exp_21_path=main_path+'exp2-1.png'
exp_22_path=main_path+'exp2-2.png'
exp_23_path=main_path+'exp2-3.png'
exp_3_path=main_path+'exp3.png'
######Enemies##########
slub1_path=main_path+'slub1.png'
slub2_path=main_path+'slub2.png'
slub3_path=main_path+'slub3.png'
########################
display_width=320
display_height=240
#####

####
NOTHING=0
JUMP_WEAK=1
JUMP_STRONG=2
RIGHT_R=3
LEFT_R=4
###

#####
STOP=Vector2D(0,0)
RIGHT=Vector2D(1,0)
RIGHT_UP=Vector2D(1,-1)
RIGHT_DOWN=Vector2D(1,1)
LEFT=Vector2D(-1,0)
LEFT_UP=Vector2D(-1,-1)
LEFT_DOWN=Vector2D(-1,1)
UP=Vector2D(0,-1)
DOWN=Vector2D(0,1)
#####################
def floor_constructor(not_floor):
    floor=[]
    for i in range(0,215):
        floor.append(int(i* set_width(1)))
    for item in not_floor:
        floor.remove(item*set_width(1))
    return floor
def set_height(factor):
    return int(display_height-1.5*floor.get_height()-factor*floor.get_height())
def set_width(factor):
    return int(factor*floor.get_width())
#####################

win = pygame.display.set_mode((display_width,display_height),0,32)

#####################

agent=pygame.image.load(agent_image_path).convert_alpha()
hill=pygame.image.load(hill_image_path).convert_alpha()
castle=pygame.image.load(castle_image_path).convert_alpha()
cloud=pygame.image.load(cloud_image_path).convert_alpha()
double_cloud=pygame.image.load(double_cloud_image_path).convert_alpha()
bush=pygame.image.load(bush_image_path).convert_alpha()
pipe=pygame.image.load(pipe_image_path).convert_alpha()
bigpipe=pygame.image.load(big_pipe_image_path).convert_alpha()
block=pygame.image.load(block_image_path).convert_alpha()

brick=pygame.image.load(brick_image_path).convert_alpha()
q1=pygame.image.load(q1_image_path).convert_alpha()
q2=pygame.image.load(q2_image_path).convert_alpha()
q3=pygame.image.load(q3_image_path).convert_alpha()
q4=pygame.image.load(q4_image_path).convert_alpha()
flag=pygame.image.load(flag_image_path).convert_alpha()
exp1=pygame.image.load(exp_1_path).convert_alpha()
exp2=pygame.image.load(exp_21_path).convert_alpha()
exp3=pygame.image.load(exp_22_path).convert_alpha()
exp4=pygame.image.load(exp_23_path).convert_alpha()
exp5=pygame.image.load(exp_3_path).convert_alpha()

slub1=pygame.image.load(slub1_path).convert_alpha()
slub2=pygame.image.load(slub2_path).convert_alpha()
slub3=pygame.image.load(slub3_path).convert_alpha()

floor=pygame.image.load(floor_image_path)
#not_floor=[68,69,85,86,87,151,152]
not_floor=[68,69,85,86,87]
floor_list=floor_constructor(not_floor)
bg = pygame.image.load(background_image_path).convert_alpha()
not_floor=[[0,0],[10,10]]

#################################

landscape=[[set_width(0),set_height(2),hill],
           [set_width(10),set_height(10),cloud],
           [set_width(12),set_height(1),bush],
           [set_width(15),set_height(1),hill],
           [set_width(20),set_height(11),cloud],
           [set_width(22),set_height(1),bush],
           [set_width(28),set_height(10),double_cloud],
           [set_width(37),set_height(11),cloud],
           [set_width(42),set_height(1),bush],
           [set_width(49),set_height(2),hill],
           [set_width(58),set_height(1),bush],
           [set_width(61),set_height(1),hill],
           [set_width(70),set_height(1),bush],
           [set_width(55),set_height(10),cloud],
           [set_width(67),set_height(10),cloud],
           [set_width(75),set_height(10),cloud],
           [set_width(82),set_height(11),cloud],
           [set_width(88),set_height(1),bush],
           [set_width(95),set_height(2),hill],
           [set_width(104),set_height(10),cloud],
           [set_width(106),set_height(1),bush],
           [set_width(134),set_height(1),bush],
           [set_width(114),set_height(11),cloud],
           [set_width(130),set_height(11),cloud],
           [set_width(120),set_height(10),double_cloud],
           [set_width(141),set_height(2),hill],
           [set_width(154),set_height(1),bush],
           [set_width(157),set_height(1),hill],
           [set_width(163),set_height(1),bush],
           [set_width(177),set_height(1),bush],
           [set_width(190),set_height(2),hill],
           [set_width(200),set_height(5),castle],
           [set_width(206),set_height(1),hill],
           [set_width(178),set_height(11),cloud],
           [set_width(199),set_height(10),cloud],]
fixed_objects=[[set_width(27),set_height(2),pipe,"pipe"],
               [set_width(38),set_height(3),pipe,"pipe"],
               [set_width(47),set_height(4),bigpipe,"bigpipe"],
               [set_width(56),set_height(4),bigpipe,"bigpipe"],
               [set_width(132),set_height(1),block,"block"],
               [set_width(133),set_height(1),block,"block"],
               [set_width(134),set_height(1),block,"block"],
               [set_width(135),set_height(1),block,"block"],
               [set_width(133),set_height(2),block,"block"],
               [set_width(134),set_height(2),block,"block"],
               [set_width(135),set_height(2),block,"block"],
               [set_width(134),set_height(3),block,"block"],
               [set_width(135),set_height(3),block,"block"],
               [set_width(135),set_height(4),block,"block"],
               [set_width(138),set_height(1),block,"block"],
               [set_width(139),set_height(1),block,"block"],
               [set_width(140),set_height(1),block,"block"],
               [set_width(141),set_height(1),block,"block"],
               [set_width(138),set_height(2),block,"block"],
               [set_width(139),set_height(2),block,"block"],
               [set_width(140),set_height(2),block,"block"],
               [set_width(138),set_height(3),block,"block"],
               [set_width(139),set_height(3),block,"block"],
               [set_width(138),set_height(4),block,"block"],
               [set_width(146),set_height(1),block,"block"],
               [set_width(147),set_height(1),block,"block"],
               [set_width(148),set_height(1),block,"block"],
               [set_width(149),set_height(1),block,"block"],
               [set_width(150),set_height(1),block,"block"],
               [set_width(147),set_height(2),block,"block"],
               [set_width(148),set_height(2),block,"block"],
               [set_width(149),set_height(2),block,"block"],
               [set_width(150),set_height(2),block,"block"],
               [set_width(148),set_height(3),block,"block"],
               [set_width(149),set_height(3),block,"block"],
               [set_width(150),set_height(3),block,"block"],
               [set_width(149),set_height(4),block,"block"],
               [set_width(150),set_height(4),block,"block"],
               [set_width(153),set_height(1),block,"block"],
               [set_width(154),set_height(1),block,"block"],
               [set_width(155),set_height(1),block,"block"],
               [set_width(156),set_height(1),block,"block"],
               [set_width(153),set_height(2),block,"block"],
               [set_width(154),set_height(2),block,"block"],
               [set_width(155),set_height(2),block,"block"],
               [set_width(153),set_height(3),block,"block"],
               [set_width(154),set_height(3),block,"block"],
               [set_width(153),set_height(4),block,"block"],
               [set_width(161),set_height(2),pipe,"pipe"],
               [set_width(176),set_height(2),pipe,"pipe"],
               [set_width(178),set_height(1),block,"block"],
               [set_width(179),set_height(1),block,"block"],
               [set_width(180),set_height(1),block,"block"],
               [set_width(181),set_height(1),block,"block"],
               [set_width(182),set_height(1),block,"block"],
               [set_width(183),set_height(1),block,"block"],
               [set_width(184),set_height(1),block,"block"],
               [set_width(185),set_height(1),block,"block"],
               [set_width(186),set_height(1),block,"block"],
               [set_width(187),set_height(1),block,"block"],
               [set_width(179),set_height(2),block,"block"],
               [set_width(180),set_height(2),block,"block"],
               [set_width(181),set_height(2),block,"block"],
               [set_width(182),set_height(2),block,"block"],
               [set_width(183),set_height(2),block,"block"],
               [set_width(184),set_height(2),block,"block"],
               [set_width(185),set_height(2),block,"block"],
               [set_width(186),set_height(2),block,"block"],
               [set_width(187),set_height(2),block,"block"],
               [set_width(180),set_height(3),block,"block"],
               [set_width(181),set_height(3),block,"block"],
               [set_width(182),set_height(3),block,"block"],
               [set_width(183),set_height(3),block,"block"],
               [set_width(184),set_height(3),block,"block"],
               [set_width(185),set_height(3),block,"block"],
               [set_width(186),set_height(3),block,"block"],
               [set_width(187),set_height(3),block,"block"],
               [set_width(181),set_height(4),block,"block"],
               [set_width(182),set_height(4),block,"block"],
               [set_width(183),set_height(4),block,"block"],
               [set_width(184),set_height(4),block,"block"],
               [set_width(185),set_height(4),block,"block"],
               [set_width(186),set_height(4),block,"block"],
               [set_width(187),set_height(4),block,"block"],
               [set_width(182),set_height(5),block,"block"],
               [set_width(183),set_height(5),block,"block"],
               [set_width(184),set_height(5),block,"block"],
               [set_width(185),set_height(5),block,"block"],
               [set_width(186),set_height(5),block,"block"],
               [set_width(187),set_height(5),block,"block"],
               [set_width(183),set_height(6),block,"block"],
               [set_width(184),set_height(6),block,"block"],
               [set_width(185),set_height(6),block,"block"],
               [set_width(186),set_height(6),block,"block"],
               [set_width(187),set_height(6),block,"block"],
               [set_width(184),set_height(7),block,"block"],
               [set_width(185),set_height(7),block,"block"],
               [set_width(186),set_height(7),block,"block"],
               [set_width(187),set_height(7),block,"block"],
               [set_width(185),set_height(8),block,"block"],
               [set_width(186),set_height(8),block,"block"],
               [set_width(187),set_height(8),block,"block"],
               [set_width(186),set_height(9),block,"block"],
               [set_width(187),set_height(9),block,"block"],
               [set_width(196),set_height(1),block,"block"],]
animated_objects=[[set_width(196)-set_width(1)//2,set_height(10)-8,flag],]
q_objects=[[set_width(15),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(20),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(22),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(21),set_height(7),[q1,q2,q3,q4,block],0],
                  [set_width(62),set_height(5),[q1,q2,q3,q4,block],0],
                  [set_width(77),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(93),set_height(8),[q1,q2,q3,q4,block],0],
                  [set_width(93),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(100),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(105),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(108),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(111),set_height(4),[q1,q2,q3,q4,block],0],
                  [set_width(108),set_height(8),[q1,q2,q3,q4,block],0],
                  [set_width(127),set_height(8),[q1,q2,q3,q4,block],0],
                  [set_width(128),set_height(8),[q1,q2,q3,q4,block],0],
                  [set_width(168),set_height(4),[q1,q2,q3,q4,block],0]]
brick_objects=[[set_width(19),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(21),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(23),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(76),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(78),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(79),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(80),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(81),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(82),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(83),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(84),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(85),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(86),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(90),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(91),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(92),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(99),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(116),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(119),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(120),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(121),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(126),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(129),set_height(8),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(127),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(128),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(166),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(167),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],
                  [set_width(169),set_height(4),[brick,exp1,exp2,exp3,exp4,exp5]],]
slub_objects=[[set_width(20),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(34),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(51),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(52),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(74),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(80),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(95),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(108),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(110),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(125),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              [set_width(168),set_height(1),[slub1,slub2,slub3,exp1,exp2,exp3,exp4,exp5]],
              ]