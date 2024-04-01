import sys
import os

MAIN_PATH=os.path.dirname(os.path.abspath(__file__))

import gym
from gym import spaces
import yaml
import math

import pygame
from pygame.locals  import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pauser
from levels import LevelController
from text import TextGroup
from sprites import Spritesheet
from maze import Maze
import time
import numpy as np


class Pacman_v1_1(gym.Env):
    def __init__(self):
        self.visualize=False
        pygame.init()
        self.global_done=False
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.pelletsEaten = 0
        self.fruit = None
        self.pause = Pauser(True)
        self.level = LevelController()
        self.text = TextGroup()
        self.sheet = Spritesheet()
        self.maze = Maze(self.sheet)
        self.actions=[0,1,2,3]
        self.reward=0
        self.done=False
        self.state_matrix=np.zeros((NROWS,NCOLS))
        self.dummy_state_matrix=np.zeros((NROWS,NCOLS))
        self.test_1=0
        self.test_2=0
        self.test_3=0
        self.test_4=0
        self.vidas=5
        self.first=True
        self.action_space= spaces.Discrete(4)
        #self.matrix_state.reshape(13,11,1)
        self.observation_space=spaces.Box(low=0, high=1, shape=(9,26,1), dtype=np.float32)
        self.actual_reward_episode=[]
        self.actual_reward=0
        self.act_avg=[]
        self.avg_reward=[]
        self.actual_episode=0
        self.actual_step=0
        self.actual_epoch=0
    def step(self,action):
        for i in range(0,4):
            if not self.gameover:
                dt = 0.066
                if True:
                #if not self.pause.paused:
                    self.text.hideMessages()
                    self.pacman.update(dt,action)
                    self.ghosts.update(dt, self.pacman)
                    if self.fruit is not None:
                        self.fruit.update(dt)
                    if self.pause.pauseType != None:
                        self.pause.settlePause(self)
                    self.checkPelletEvents()
                    self.checkGhostEvents()
                    self.checkFruitEvents()

                self.pause.update(dt)
                self.pellets.update(dt)
                self.text.update(dt)
            self.checkEvents()
            self.text.updateScore(self.score)
            if self.visualize:
                self.render()
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
                try:
                    reward=(sum(self.act_avg)/len(self.act_avg))
                    print("Epoch:",epoch, "Reward: ",reward)
                except:
                    print("Epoch:",epoch)
                self.avg_reward.append(reward)
            return self.state(),self.reward,self.done,{} 
    def reset(self):
        self.reward=0
        self.done=False
        self.startGame()
        #self.global_done=False
        return self.state()
    def render(self):
        self.screen.blit(self.background, (0, 0))
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.pacman.renderLives(self.screen)
        self.text.render(self.screen)
        pygame.display.update()
    
        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.level.reset()
        levelmap = self.level.getLevel()
        self.maze.getMaze(levelmap["mazename"].split(".")[0])
        self.maze.constructMaze(self.background)
        self.nodes = NodeGroup(levelmap["mazename"])
        self.pellets = PelletGroup(levelmap["pelletname"])
        self.pacman = Pacman(self.nodes, self.sheet)
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.pelletsEaten = 0
        self.fruit = None
        self.pause.force(True)
        self.gameover = False
        self.score = 0
        #self.text.showReady()
        #self.text.updateLevel(self.level.level+)
        self.text.updateLevel(self.level.level)
        self.global_done=False
        
    def startLevel(self):
        levelmap = self.level.getLevel()
        self.setBackground()
        self.nodes = NodeGroup(levelmap["mazename"])
        self.pellets = PelletGroup(levelmap["pelletname"])
        self.pacman.nodes = self.nodes
        self.pacman.reset()
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.pelletsEaten = 0
        self.fruit = None
        self.pause.force(True)
        self.text.showReady()
        self.text.updateLevel(self.level.level+1)

    def restartLevel(self):
        self.pacman.reset()
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.fruit = None
        self.pause.force(True)
        self.text.showReady()
        
    def update(self):
        if not self.gameover:
            dt = self.clock.tick(30) / 1000.0
            if not self.pause.paused:
                self.pacman.update(dt)
                self.ghosts.update(dt, self.pacman)
                if self.fruit is not None:
                    pass
                    #self.fruit.update(dt)
                if self.pause.pauseType != None:
                    self.pause.settlePause(self)
                self.checkPelletEvents()
                self.checkGhostEvents()
                #self.checkFruitEvents()

            self.pause.update(dt)
            self.pellets.update(dt)
            self.text.update(dt)
        self.checkEvents()
        self.text.updateScore(self.score)
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.gameover:
                        self.startGame()
                    else:
                        self.pause.player()
                        if self.pause.paused:
                            self.text.showPause()
                        else:
                            self.text.hideMessages()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.reward=1
            self.pelletsEaten += 1
            self.score += pellet.points
            if (self.pelletsEaten == 70 or self.pelletsEaten == 140):
                if self.fruit is None:
                    pass
                    #self.fruit = Fruit(self.nodes, self.sheet)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghosts.resetPoints()
                self.ghosts.freightMode()
                self.reward=10
            if self.pellets.isEmpty():
                self.pacman.visible = False
                self.ghosts.hide()
                self.pause.startTimer(3, "clear")
                self.reward=20
            
        else:
            self.reward=0
                
    def checkGhostEvents(self):
        self.ghosts.release(self.pelletsEaten)
        ghost = self.pacman.eatGhost(self.ghosts)
        if ghost is not None:
            if ghost.mode.name == "FREIGHT":
                self.score += ghost.points
                self.text.createTemp(ghost.points, ghost.position)
                self.ghosts.updatePoints()
                ghost.spawnMode(speed=2)
                self.pause.startTimer(1)
                self.pacman.visible = False
                ghost.visible = False
                self.reward=10
            elif ghost.mode.name == "CHASE" or ghost.mode.name == "SCATTER":
                self.pacman.loseLife()
                self.ghosts.hide()
                self.pause.startTimer(3, "die")
                self.reward=-10
                self.vidas-=1
                if self.vidas==0:
                    self.vidas=5
                    self.global_done=True
                self.done=True

    def checkFruitEvents(self):
        if self.fruit is not None:
            if self.pacman.eatFruit(self.fruit):
                self.score += self.fruit.points
                self.text.createTemp(self.fruit.points, self.fruit.position)
                self.fruit = None
                self.reward=10
            elif self.fruit.destroy:
                self.fruit = None
            #if self.pacman.eatFruit(self.fruit) or self.fruit.destroy:
                #self.fruit = None

    def resolveDeath(self):
        if self.pacman.lives == 0:
            self.gameover = True
        else:
            self.restartLevel()
        self.pause.pauseType = None

    def resolveLevelClear(self):
        #self.level.nextLevel()
        self.startLevel()
        self.pause.pauseType = None
        self.reward=20
        self.vidas=3
        self.done=True
        self.global_done=True
    

    def iota(self):
        HALF_TILEWITDH=TILEWIDTH/2
        pacman_position_x=float(self.pacman.position.x)+6
        pacman_position_y=float(self.pacman.position.y)+8
        probabilities=[0,0,0,0]
        pacman_position_x_discrete=int((pacman_position_x)/TILEWIDTH)
        pacman_position_y_discrete=int((pacman_position_y)/TILEWIDTH)
        X_MAX=int((self.pacman.position.x)/TILEWIDTH)*TILEWIDTH+HALF_TILEWITDH+1
        X_MIN=int((self.pacman.position.x)/TILEWIDTH)*TILEWIDTH+HALF_TILEWITDH-1
        Y_MAX=(pacman_position_y_discrete)*TILEWIDTH+HALF_TILEWITDH+1
        Y_MIN=(pacman_position_y_discrete)*TILEWIDTH+HALF_TILEWITDH-1
        max_x=int(pacman_position_x_discrete)+1
        min_x=int(pacman_position_x_discrete)-1
        max_y=int(pacman_position_y_discrete)-1
        min_y=int(pacman_position_y_discrete)+1
        if self.state_matrix[max_y,int(pacman_position_x_discrete)]==0.1:
                    probabilities[0]=1
        elif self.state_matrix[max_y,int(pacman_position_x_discrete)]==0.5:
                    probabilities[0]=1
        if self.state_matrix[min_y,int(pacman_position_x_discrete)]==0.1:
                    probabilities[2]=1
        elif self.state_matrix[min_y,int(pacman_position_x_discrete)]==0.5:
                    probabilities[2]=1
        if self.state_matrix[int(pacman_position_y_discrete),max_x]==0.1:
                    probabilities[1]=1
        elif self.state_matrix[int(pacman_position_y_discrete),max_x]==0.5:
                    probabilities[1]=1
        if self.state_matrix[int(pacman_position_y_discrete),min_x]==0.1:
                    probabilities[3]=1
        elif self.state_matrix[int(pacman_position_y_discrete),min_x]==0.5:
                    probabilities[3]=1
        if probabilities[0]==0 and probabilities[1]==0 and probabilities[2]==0 and probabilities[3]==0:
            if self.state_matrix[max_y,int(pacman_position_x_discrete)]==0:
                        probabilities[0]=1
            if self.state_matrix[min_y,int(pacman_position_x_discrete)]==0:
                        probabilities[2]=1
            if self.state_matrix[int(pacman_position_y_discrete),max_x]==0:
                        probabilities[1]=1
            if self.state_matrix[int(pacman_position_y_discrete),min_x]==0:
                        probabilities[3]=1
        probabilities=[probabilities[0],probabilities[2],probabilities[3],probabilities[1]]
        return probabilities
    def dummy_state(self,action):
        HALF_TILEWITDH=TILEWIDTH/2
        pacman_position_x=float(self.pacman.position.x)+6
        pacman_position_y=float(self.pacman.position.y)+8
        pacman_position_x_discrete=int((pacman_position_x)/TILEWIDTH)
        pacman_position_y_discrete=int((pacman_position_y)/TILEWIDTH)  
        self.dummy_state_matrix=np.zeros((NROWS,NCOLS))
        #for i in self.pellets.pelletList:
            #pos=i.position/TILEWIDTH
            #self.state_matrix[int(pos.y),int(pos.x)]=0.1
            #self.state_matrix[int(pos.y)+1,int(pos.x)]=0.1
            #self.state_matrix[int(pos.y)-1,int(pos.x)]=0.1
            #self.state_matrix[int(pos.y),int(pos.x)+1]=0.1
            #self.state_matrix[int(pos.y),int(pos.x)-1]=0.1
        pac_pos=self.pacman.position/TILEWIDTH
        blinky_pos=self.ghosts.ghosts[0].position
        blinky_dir=self.ghosts.ghosts[0].state_dir/100.0
        inky_pos=self.ghosts.ghosts[1].position
        inky_dir=self.ghosts.ghosts[1].state_dir/100.0
        dif_x=int((float(pacman_position_x/TILEWIDTH)-int(pacman_position_x/TILEWIDTH))*9.0)/1000.0
        dif_y=int((float(pacman_position_y/TILEWIDTH)-int(pacman_position_y/TILEWIDTH))*9.0)/10000.0
        
        if self.ghosts.ghosts[0].mode_persue==True:
            blinky_position_x=float(blinky_pos.x)+6
            blinky_position_y=float(blinky_pos.y)+8
            blinky_position_x_discrete=int((blinky_position_x)/TILEWIDTH)
            blinky_position_y_discrete=int((blinky_position_y)/TILEWIDTH)
            self.dummy_state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)]=0.5
            self.dummy_state_matrix[int(blinky_position_y_discrete)+1,int(blinky_position_x_discrete)]=0.5
            self.dummy_state_matrix[int(blinky_position_y_discrete)-1,int(blinky_position_x_discrete)]=0.5
            self.dummy_state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)+1]=0.5
            self.dummy_state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)-1]=0.5
        else:
            blinky_position_x=float(blinky_pos.x)+6
            blinky_position_y=float(blinky_pos.y)+8
            blinky_position_x_discrete=int((blinky_position_x)/TILEWIDTH)
            blinky_position_y_discrete=int((blinky_position_y)/TILEWIDTH)
            self.dummy_state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)]=0.3+blinky_dir
            self.dummy_state_matrix[int(blinky_position_y_discrete)+1,int(blinky_position_x_discrete)]=0.3
            self.dummy_state_matrix[int(blinky_position_y_discrete)-1,int(blinky_position_x_discrete)]=0.3
            self.dummy_state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)+1]=0.3
            self.dummy_state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)-1]=0.3
        if self.ghosts.ghosts[1].mode_persue==True:
            inky_position_x=float(inky_pos.x)+6
            inky_position_y=float(inky_pos.y)+8
            inky_position_x_discrete=int((inky_position_x)/TILEWIDTH)
            inky_position_y_discrete=int((inky_position_y)/TILEWIDTH) 
            self.dummy_state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)]=0.5
            self.dummy_state_matrix[int(inky_position_y_discrete)+1,int(inky_position_x_discrete)]=0.5
            self.dummy_state_matrix[int(inky_position_y_discrete)-1,int(inky_position_x_discrete)]=0.5
            self.dummy_state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)+1]=0.5
            self.dummy_state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)-1]=0.5
        else:
            inky_position_x=float(inky_pos.x)+6
            inky_position_y=float(inky_pos.y)+8
            inky_position_x_discrete=int((inky_position_x)/TILEWIDTH)
            inky_position_y_discrete=int((inky_position_y)/TILEWIDTH)
            self.dummy_state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)]=0.3+inky_dir
            self.dummy_state_matrix[int(inky_position_y_discrete)+1,int(inky_position_x_discrete)]=0.3
            self.dummy_state_matrix[int(inky_position_y_discrete)-1,int(inky_position_x_discrete)]=0.3
            self.dummy_state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)+1]=0.3
            self.dummy_state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)-1]=0.3
        rows = len(self.maze.spriteInfo)
        cols = len(self.maze.spriteInfo[0])
        self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)]=0.2+self.pacman.state_dir/100.0+dif_x+dif_y
        self.test_1=self.pacman.state_dir/100.0
        self.test_2=dif_x
        self.test_3=dif_y
        self.test_4=0.2+self.pacman.state_dir/100.0+dif_x+dif_y
        for row in range(rows):
            for col in range(cols):
                val = self.maze.spriteInfo[row][col]
                if val != '.':
                    self.dummy_state_matrix[int(row),int(col)]=0.4
        #####stablish route
        #directions write 0.1 till you find (0.4 or 0.3 or 0.5)
        #int(pacman_position_y_discrete)
        #int(pacman_position_x_discrete)
        #####
        if action==0:#UP
            if self.dummy_state_matrix[int(pacman_position_y_discrete)-1,int(pacman_position_x_discrete)]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete)-1,int(pacman_position_x_discrete)]=0.1
            else:
                if self.dummy_state_matrix[int(pacman_position_y_discrete)+1,int(pacman_position_x_discrete)]==0:
                    self.dummy_state_matrix[int(pacman_position_y_discrete)+1,int(pacman_position_x_discrete)]=0.1
            if self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)+1]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)+1]=0.1
            if self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)-1]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)-1]=0.1
        elif action==1:#DOWN
            if self.dummy_state_matrix[int(pacman_position_y_discrete)+1,int(pacman_position_x_discrete)]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete)+1,int(pacman_position_x_discrete)]=0.1
            else:
                if self.dummy_state_matrix[int(pacman_position_y_discrete)-1,int(pacman_position_x_discrete)]==0:
                    self.dummy_state_matrix[int(pacman_position_y_discrete)-1,int(pacman_position_x_discrete)]=0.1
            if self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)+1]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)+1]=0.1
            if self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)-1]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)-1]=0.1
        elif action==2:#LEFT
            if self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)-1]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)-1]=0.1
            else:
                if self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)+1]==0:
                    self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)+1]=0.1
            if self.dummy_state_matrix[int(pacman_position_y_discrete)-1,int(pacman_position_x_discrete)]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete)-1,int(pacman_position_x_discrete)]=0.1
            if self.dummy_state_matrix[int(pacman_position_y_discrete)+1,int(pacman_position_x_discrete)]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete)+1,int(pacman_position_x_discrete)]=0.1
        else:#RIGHT
            if self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)+1]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)+1]=0.1
            else:
                if self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)-1]==0:
                    self.dummy_state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)-1]=0.1
            if self.dummy_state_matrix[int(pacman_position_y_discrete)-1,int(pacman_position_x_discrete)]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete)-1,int(pacman_position_x_discrete)]=0.1
            if self.dummy_state_matrix[int(pacman_position_y_discrete)+1,int(pacman_position_x_discrete)]==0:
                self.dummy_state_matrix[int(pacman_position_y_discrete)+1,int(pacman_position_x_discrete)]=0.1
        return  self.dummy_state_matrix.reshape(1,NCOLS,NROWS,1)
    def dummy_iota(self,action):
        self.dummy_state(action)
        HALF_TILEWITDH=TILEWIDTH/2
        pacman_position_x=float(self.pacman.position.x)+6
        pacman_position_y=float(self.pacman.position.y)+8
        probabilities=[0,0,0,0]
        pacman_position_x_discrete=int((pacman_position_x)/TILEWIDTH)
        pacman_position_y_discrete=int((pacman_position_y)/TILEWIDTH)
        X_MAX=int((self.pacman.position.x)/TILEWIDTH)*TILEWIDTH+HALF_TILEWITDH+1
        X_MIN=int((self.pacman.position.x)/TILEWIDTH)*TILEWIDTH+HALF_TILEWITDH-1
        Y_MAX=(pacman_position_y_discrete)*TILEWIDTH+HALF_TILEWITDH+1
        Y_MIN=(pacman_position_y_discrete)*TILEWIDTH+HALF_TILEWITDH-1
        max_x=int(pacman_position_x_discrete)+1
        min_x=int(pacman_position_x_discrete)-1
        max_y=int(pacman_position_y_discrete)-1
        min_y=int(pacman_position_y_discrete)+1
        if self.dummy_state_matrix[max_y,int(pacman_position_x_discrete)]==0.1:
                    probabilities[0]=1
        elif self.dummy_state_matrix[max_y,int(pacman_position_x_discrete)]==0.5:
                    probabilities[0]=1
        if self.dummy_state_matrix[min_y,int(pacman_position_x_discrete)]==0.1:
                    probabilities[2]=1
        elif self.dummy_state_matrix[min_y,int(pacman_position_x_discrete)]==0.5:
                    probabilities[2]=1
        if self.dummy_state_matrix[int(pacman_position_y_discrete),max_x]==0.1:
                    probabilities[1]=1
        elif self.dummy_state_matrix[int(pacman_position_y_discrete),max_x]==0.5:
                    probabilities[1]=1
        if self.dummy_state_matrix[int(pacman_position_y_discrete),min_x]==0.1:
                    probabilities[3]=1
        elif self.dummy_state_matrix[int(pacman_position_y_discrete),min_x]==0.5:
                    probabilities[3]=1
        if probabilities[0]==0 and probabilities[1]==0 and probabilities[2]==0 and probabilities[3]==0:
            if self.dummy_state_matrix[max_y,int(pacman_position_x_discrete)]==0:
                        probabilities[0]=1
            if self.dummy_state_matrix[min_y,int(pacman_position_x_discrete)]==0:
                        probabilities[2]=1
            if self.dummy_state_matrix[int(pacman_position_y_discrete),max_x]==0:
                        probabilities[1]=1
            if self.dummy_state_matrix[int(pacman_position_y_discrete),min_x]==0:
                        probabilities[3]=1
        probabilities=[probabilities[0],probabilities[2],probabilities[3],probabilities[1]]
        return probabilities
    def state(self):
        HALF_TILEWITDH=TILEWIDTH/2
        pacman_position_x=float(self.pacman.position.x)+6
        pacman_position_y=float(self.pacman.position.y)+8
        pacman_position_x_discrete=int((pacman_position_x)/TILEWIDTH)
        pacman_position_y_discrete=int((pacman_position_y)/TILEWIDTH)  
        self.state_matrix=np.zeros((NROWS,NCOLS))
        
        for i in self.pellets.pelletList:
            pos=i.position/TILEWIDTH
            self.state_matrix[int(pos.y),int(pos.x)]=0.1
            #self.state_matrix[int(pos.y)+1,int(pos.x)]=0.1
            #self.state_matrix[int(pos.y)-1,int(pos.x)]=0.1
            #self.state_matrix[int(pos.y),int(pos.x)+1]=0.1
            #self.state_matrix[int(pos.y),int(pos.x)-1]=0.1
        pac_pos=self.pacman.position/TILEWIDTH
        blinky_pos=self.ghosts.ghosts[0].position
        blinky_dir=self.ghosts.ghosts[0].state_dir/100.0
        inky_pos=self.ghosts.ghosts[1].position
        inky_dir=self.ghosts.ghosts[1].state_dir/100.0
        dif_x=int((float(pacman_position_x/TILEWIDTH)-int(pacman_position_x/TILEWIDTH))*9.0)/1000.0
        dif_y=int((float(pacman_position_y/TILEWIDTH)-int(pacman_position_y/TILEWIDTH))*9.0)/10000.0
        
        if self.ghosts.ghosts[0].mode_persue==True:
            blinky_position_x=float(blinky_pos.x)+6
            blinky_position_y=float(blinky_pos.y)+8
            blinky_position_x_discrete=int((blinky_position_x)/TILEWIDTH)
            blinky_position_y_discrete=int((blinky_position_y)/TILEWIDTH)
            self.state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)]=0.5
            self.state_matrix[int(blinky_position_y_discrete)+1,int(blinky_position_x_discrete)]=0.5
            self.state_matrix[int(blinky_position_y_discrete)-1,int(blinky_position_x_discrete)]=0.5
            self.state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)+1]=0.5
            self.state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)-1]=0.5
        else:
            blinky_position_x=float(blinky_pos.x)+6
            blinky_position_y=float(blinky_pos.y)+8
            blinky_position_x_discrete=int((blinky_position_x)/TILEWIDTH)
            blinky_position_y_discrete=int((blinky_position_y)/TILEWIDTH)
            self.state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)]=0.3+blinky_dir
            self.state_matrix[int(blinky_position_y_discrete)+1,int(blinky_position_x_discrete)]=0.3
            self.state_matrix[int(blinky_position_y_discrete)-1,int(blinky_position_x_discrete)]=0.3
            self.state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)+1]=0.3
            self.state_matrix[int(blinky_position_y_discrete),int(blinky_position_x_discrete)-1]=0.3
        if self.ghosts.ghosts[1].mode_persue==True:
            inky_position_x=float(inky_pos.x)+6
            inky_position_y=float(inky_pos.y)+8
            inky_position_x_discrete=int((inky_position_x)/TILEWIDTH)
            inky_position_y_discrete=int((inky_position_y)/TILEWIDTH) 
            self.state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)]=0.5
            self.state_matrix[int(inky_position_y_discrete)+1,int(inky_position_x_discrete)]=0.5
            self.state_matrix[int(inky_position_y_discrete)-1,int(inky_position_x_discrete)]=0.5
            self.state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)+1]=0.5
            self.state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)-1]=0.5
        else:
            inky_position_x=float(inky_pos.x)+6
            inky_position_y=float(inky_pos.y)+8
            inky_position_x_discrete=int((inky_position_x)/TILEWIDTH)
            inky_position_y_discrete=int((inky_position_y)/TILEWIDTH)
            self.state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)]=0.3+inky_dir
            self.state_matrix[int(inky_position_y_discrete)+1,int(inky_position_x_discrete)]=0.3
            self.state_matrix[int(inky_position_y_discrete)-1,int(inky_position_x_discrete)]=0.3
            self.state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)+1]=0.3
            self.state_matrix[int(inky_position_y_discrete),int(inky_position_x_discrete)-1]=0.3
        #self.state_matrix[0,0]=pacman_position_x/100.0
        #self.state_matrix[0,1]=pacman_position_y/100.0
        #self.state_matrix[0,2]=inky_position_x/100.0
        #self.state_matrix[0,3]=inky_position_y/100.0
        #self.state_matrix[0,4]=blinky_position_x/100.0
        #self.state_matrix[0,5]=blinky_position_y/100.0
        rows = len(self.maze.spriteInfo)
        cols = len(self.maze.spriteInfo[0])
        self.state_matrix[int(pacman_position_y_discrete),int(pacman_position_x_discrete)]=0.9+self.pacman.state_dir/100.0+dif_x+dif_y
        self.test_1=self.pacman.state_dir/100.0
        self.test_2=dif_x
        self.test_3=dif_y
        self.test_4=0.2+self.pacman.state_dir/100.0+dif_x+dif_y
        for row in range(rows):
            for col in range(cols):
                val = self.maze.spriteInfo[row][col]
                if val != '.':
                    self.state_matrix[int(row),int(col)]=0.4
        #return  self.state_matrix[6:-4,0:-2].reshape
        return  self.state_matrix[7:-6,0:-2].reshape(9,26,1)
    def state_size(self):
        return np.size(self.state())
    def action_size(self):
        return 4
    def action_set(self):
        pass
    def resizeState(self,state):
        #basewidth = 84
        #img = Image.fromarray(state, 'RGB')
        #wpercent = (basewidth/float(img.size[0]))
        #hsize = int((float(img.size[1])*float(wpercent)))
        #img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        #grays=img.convert('LA')
        #grays=img.convert('1')
        #newState = np.asarray(grays)
        #newState = tf.image.convert_image_dtype(newState, dtype=tf.float16, saturate=False)
        #newState = np.transpose(newState.flatten())
        #grays.save('my.png')
        #row, col = newState.shape
        newState=state.reshape(NROWS,NCOLS)
    
def main():
    pass
if __name__ == "__main__":
    main()


        
