# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 10:48:39 2022

@author: C1982450
"""

import sys
import os

LOCAL_PATH=os.path.dirname(os.path.abspath(__file__))
MAIN_PATH=LOCAL_PATH+'/..'

CONF_PATH=MAIN_PATH+"/CONF"
DEMO_PATH=MAIN_PATH+"/DEMO"
DOC_PATH=MAIN_PATH+"/DOC"
ENV_PATH=MAIN_PATH+"/LIB/GAME"
LIB_PATH=MAIN_PATH+"/LIB"
LOG_PATH=MAIN_PATH+"/LOG"
IMG_PATH=MAIN_PATH+"/Images"
POLICIES_PATH=MAIN_PATH+"/TEMP/POLICIES"
TEMP_PATH=MAIN_PATH+"/TEMP"
TRN_PATH=MAIN_PATH+"/LIB/TRAINING"

sys.path.insert(1, ENV_PATH)
sys.path.insert(1, TRN_PATH)
sys.path.insert(1, LIB_PATH)

from dqn import DQN,DDDQN 
from replaybuffer import ReplayBuffer,ReplayBufferIota
import tensorflow as tf
import numpy as np
import random
import time

class SimpleDuelingAgent():
      def __init__(self, gamma=0.99, replace=100, lr=0.001,n_actions=2,input_shape=[0,0],buffer_size= 50000,batch_size=64):
          self.batch_size=batch_size
          self.buffer_size = buffer_size
          self.n_actions=n_actions
          self.input_shape=input_shape
          self.gamma = gamma
          self.epsilon = 1.0
          self.min_epsilon = 0.01
          self.epsilon_decay = 1e-3
          self.replace = replace
          self.trainstep = 0
          self.memory = ReplayBuffer(input_shape=self.input_shape,buffer_size=self.buffer_size)
          self.q_net = DDDQN()
          self.target_net = DDDQN()
          opt = tf.keras.optimizers.Adam(learning_rate=lr)
          self.q_net.compile(loss='mse', optimizer=opt)
          self.target_net.compile(loss='mse', optimizer=opt)
      def act(self, state):
          if np.random.rand() <= self.epsilon:
              return np.random.choice([i for i in range(self.n_actions)], p=[0.9, 0.1]),False
          else:
              state=tf.convert_to_tensor([state.flatten()],dtype=tf.float32)
              actions = self.q_net.advantage(state)
              action = np.argmax(actions)
              return action,True      
      def update_mem(self, state, action, reward, next_state, done):
          self.memory.add_exp(state, action, reward, next_state, done)
      def update_target(self):
          self.target_net.set_weights(self.q_net.get_weights())     
      def update_epsilon(self):
          self.epsilon = self.epsilon - self.epsilon_decay if self.epsilon > self.min_epsilon else self.min_epsilon
          return self.epsilon
      def train_simple(self):
          if self.memory.pointer < self.batch_size:
             return 0,0
          with tf.GradientTape() as tape:
              states, actions, rewards, next_states, dones = self.memory.sample_exp(self.batch_size)
              target = self.q_net(states)
              q_next = tf.math.reduce_max(self.target_net(next_states), axis=1,keepdims=True).numpy()
              q_target = np.copy(target)  #optional  
              maxq=tf.reduce_mean(tf.math.reduce_max(target, axis=1,keepdims=True).numpy())
              for idx, terminal in enumerate(dones):
                  if terminal:
                      q_next[idx]=0.0
                  q_target[idx,actions[idx]]=rewards[idx]+self.gamma*q_next[idx]
              loss=tf.reduce_mean((q_target-target)**2)
              #print(loss)
          gradient= tape.gradient(loss,self.q_net.trainable_variables)
          self.q_net.optimizer.apply_gradients(zip(gradient,self.q_net.trainable_variables))
          self.trainstep += 1
          return float(maxq.numpy()),float(loss.numpy())
      def train_double(self):
          if self.memory.pointer < self.batch_size:
             return 0,0
          with tf.GradientTape() as tape:
              states, actions, rewards, next_states, dones = self.memory.sample_exp(self.batch_size)
              target = self.q_net(states)
              q_next = self.target_net(next_states)
              max_action = np.argmax(self.q_net(next_states),axis=1)
              q_target = np.copy(target)
              maxq=tf.reduce_mean(tf.math.reduce_max(target, axis=1,keepdims=True).numpy())
              for idx, terminal in enumerate(dones):
                  if terminal:
                      q_target[idx][actions[idx]]=rewards[idx]
                  else:
                      q_target[idx][actions[idx]]=rewards[idx]+self.gamma*q_next[idx,max_action[idx]]
              loss=tf.reduce_mean((q_target-target)**2)
              #print(loss)
          gradient= tape.gradient(loss,self.q_net.trainable_variables)
          self.q_net.optimizer.apply_gradients(zip(gradient,self.q_net.trainable_variables))
          self.trainstep += 1
          return float(maxq.numpy()),float(loss.numpy())
class IotaDuelingAgent():
      def __init__(self, gamma=0.99, replace=100, lr=0.001,n_actions=2,input_shape=[0,0],buffer_size= 50000,batch_size=64,lambda_1=1.0,lambda_2=0.0,lambda_3=0.0):
          self.buffer_size = buffer_size
          self.input_shape=input_shape
          self.lambda_1=lambda_1
          self.lambda_2=lambda_2
          self.lambda_3=lambda_3
          self.n_actions=n_actions
          self.gamma = gamma
          self.epsilon = 1.0
          self.min_epsilon = 0.01
          self.epsilon_decay = 1e-3
          self.replace = replace
          self.trainstep = 0
          self.memory = ReplayBufferIota(input_shape=self.input_shape,buffer_size=self.buffer_size)
          self.batch_size = 64
          self.q_net = DDDQN()
          self.target_net = DDDQN()
          opt = tf.keras.optimizers.Adam(learning_rate=lr)
          self.q_net.compile(loss='mse', optimizer=opt)
          self.target_net.compile(loss='mse', optimizer=opt)
      def act(self, state):
          if np.random.rand() <= self.epsilon:
              return np.random.choice([i for i in range(self.n_actions)], p=[0.9, 0.1])
          else:
              state=tf.convert_to_tensor([state.flatten()],dtype=tf.float32)
              actions = self.q_net.advantage(state)
              action = np.argmax(actions)
              return action
      def epsilon_policy(self,epsilon,observation,iota):
          choice=[]
          amax=False
          if np.random.uniform(0,1)<epsilon:
            for i in range(0,len(iota)):
              if iota[i]>0:
                choice.append(i)
            if len(choice)>0:
              action=np.random.choice(np.array(choice))
            else:
              action=np.random.choice([i for i in range(self.n_actions)])
          else:
            action,amax=self.choose_action(observation,iota)
            #print(iota,action)
            amax=True
          return action,amax 
      def choose_action(self,observation,iota):
         state=tf.convert_to_tensor([observation.flatten()],dtype=tf.float32)
         probs=self.q_net.advantage(state)[0]
         #print(probs)
         probabilities=[]
         choices=[]
         for i in range(0,len(iota)):
           if iota[i]>0:
             probabilities.append(probs[i])
             choices.append(i)
           if len(probabilities)>0:
             action=choices[np.argmax(np.array(probabilities))]
             argmax=np.amax(np.array(probabilities))
           else:
             action=0
             argmax=None
         return action,argmax
      def update_mem(self, state, action, reward, next_state, done,iota,iota_):
          self.memory.add_exp(state, action, reward, next_state, done,iota,iota_)
      def update_target(self):
          self.target_net.set_weights(self.q_net.get_weights())     

      def update_epsilon(self):
          self.epsilon = self.epsilon - self.epsilon_decay if self.epsilon > self.min_epsilon else self.min_epsilon
          return self.epsilon
      def train_simple(self):
          if self.memory.pointer < self.batch_size:
             return 0,0
          with tf.GradientTape() as tape:
              states, actions, rewards, next_states, dones,iota, iota_= self.memory.sample_exp(self.batch_size)
              target = self.q_net(states)
              min_arg=tf.math.reduce_min(target, axis=1,keepdims=True).numpy()
              target_iota=target+abs(min_arg)
              max_iota=tf.math.reduce_max((target_iota*iota)[0], axis=1,keepdims=True).numpy()-abs(min_arg)
              max_real=tf.math.reduce_max(target, axis=1,keepdims=True).numpy()
              loss_iota=(max_iota-max_real)
              loss_iota[loss_iota>=0.]=0.
              ####
              q_next=self.target_net(next_states)
              min_arg=tf.math.reduce_min(q_next, axis=1,keepdims=True).numpy()
              q_next_iota_=target+abs(min_arg)
              max_iota_=tf.math.reduce_max((q_next_iota_*iota_)[0], axis=1,keepdims=True).numpy()-abs(min_arg)
              max_real_=tf.math.reduce_max(q_next, axis=1,keepdims=True).numpy()
              loss_iota_=(max_iota_-max_real_)
              q_target = np.copy(target)  #optional  
              maxq=tf.reduce_mean(tf.math.reduce_max(target, axis=1,keepdims=True).numpy())
              for idx, terminal in enumerate(dones):
                  if terminal:
                      max_iota_[idx]=0.0
                  q_target[idx,actions[idx]]=rewards[idx]+self.gamma*max_iota_[idx]
              loss=tf.reduce_mean(self.lambda_1*(q_target-target)**2)+tf.reduce_mean(self.lambda_2*loss_iota**2)+tf.reduce_mean(self.lambda_3*loss_iota_**2)
              #print(loss)
          gradient= tape.gradient(loss,self.q_net.trainable_variables)
          self.q_net.optimizer.apply_gradients(zip(gradient,self.q_net.trainable_variables))
          self.trainstep += 1
          return float(maxq.numpy()),float(loss.numpy())
      def train_double(self):
          if self.memory.pointer < self.batch_size:
             return 0,0
          with tf.GradientTape() as tape:
              states, actions, rewards, next_states, dones,iota, iota_= self.memory.sample_exp(self.batch_size)
              
              target = self.q_net(states)#
              q_next_main=self.q_net(next_states)
              #####
              min_arg=tf.math.reduce_min(target, axis=1,keepdims=True).numpy()
              target_iota=target+abs(min_arg)
              max_iota=tf.math.reduce_max((target_iota*iota)[0], axis=1,keepdims=True).numpy()-abs(min_arg)
              max_real=tf.math.reduce_max(target, axis=1,keepdims=True).numpy()
              loss_iota=(max_iota-max_real)
              loss_iota[loss_iota>=0.]=0.
              #####
              q_next=self.target_net(next_states)#Hay que agarrar este valor en la loss
              ###
              min_arg=tf.math.reduce_min(q_next_main, axis=1,keepdims=True).numpy()
              q_next_iota_=target+abs(min_arg)
              max_iota_=tf.math.reduce_max((q_next_iota_*iota_)[0], axis=1,keepdims=True).numpy()-abs(min_arg)
              max_action = np.argmax(max_iota_,axis=1)
              max_real_=tf.math.reduce_max(q_next_main, axis=1,keepdims=True).numpy()
              loss_iota_=(max_iota_-max_real_)
              q_target = np.copy(target)  #optional  
              ######
              maxq=tf.reduce_mean(tf.math.reduce_max(target, axis=1,keepdims=True).numpy())
              for idx, terminal in enumerate(dones):
                  if terminal:
                      q_target[idx][actions[idx]]=rewards[idx]
                  else:
                      q_target[idx][actions[idx]]=rewards[idx]+self.gamma*q_next[idx,max_action[idx]]  
              loss=tf.reduce_mean(self.lambda_1*(q_target-target)**2)+tf.reduce_mean(self.lambda_2*loss_iota**2)+tf.reduce_mean(self.lambda_3*loss_iota_**2)
              #print(loss)
          gradient= tape.gradient(loss,self.q_net.trainable_variables)
          self.q_net.optimizer.apply_gradients(zip(gradient,self.q_net.trainable_variables))
          self.trainstep += 1
          return float(maxq.numpy()),float(loss.numpy())
class SimpleQAgent():
      def __init__(self, gamma=0.99, replace=100, lr=0.001,n_actions=2,input_shape=[0,0],buffer_size= 50000,batch_size=64):
          self.buffer_size = buffer_size
          self.input_shape=input_shape
          self.n_actions=n_actions
          self.gamma = gamma
          self.epsilon = 1.0
          self.min_epsilon = 0.01
          self.epsilon_decay = 1e-3
          self.replace = replace
          self.trainstep = 0
          self.memory = ReplayBuffer(input_shape=self.input_shape,buffer_size=self.buffer_size)
          self.batch_size = batch_size
          self.q_net = DQN()
          self.target_net = DQN()
          opt = tf.keras.optimizers.Adam(learning_rate=lr)
          self.q_net.compile(loss='mse', optimizer=opt)
          self.target_net.compile(loss='mse', optimizer=opt)
      def act(self, state):
          if np.random.rand() <= self.epsilon:
              return np.random.choice([i for i in range(self.n_actions)], p=[0.9, 0.1]),False
          else:
              state=tf.convert_to_tensor([state.flatten()],dtype=tf.float32)
              actions = self.q_net(state)
              action = np.argmax(actions)
              return action,True
      def update_mem(self, state, action, reward, next_state, done):
          self.memory.add_exp(state, action, reward, next_state, done)
      def update_target(self):
          self.target_net.set_weights(self.q_net.get_weights())     
      def update_epsilon(self):
          self.epsilon = self.epsilon - self.epsilon_decay if self.epsilon > self.min_epsilon else self.min_epsilon
          return self.epsilon
      def train_simple(self):
          if self.memory.pointer < self.batch_size:
             return 0,0
          with tf.GradientTape() as tape:
              states, actions, rewards, next_states, dones = self.memory.sample_exp(self.batch_size)
              target = self.q_net(states)
              q_next = tf.math.reduce_max(self.target_net(next_states), axis=1,keepdims=True).numpy()
              q_target = np.copy(target)  #optional  
              maxq=tf.reduce_mean(tf.math.reduce_max(target, axis=1,keepdims=True).numpy())
              for idx, terminal in enumerate(dones):
                  if terminal:
                      q_next[idx]=0.0
                  q_target[idx,actions[idx]]=rewards[idx]+self.gamma*q_next[idx]
              loss=tf.reduce_mean((q_target-target)**2)
              #print(loss)
          gradient= tape.gradient(loss,self.q_net.trainable_variables)
          self.q_net.optimizer.apply_gradients(zip(gradient,self.q_net.trainable_variables))
          self.trainstep += 1
          return float(maxq.numpy()),float(loss.numpy())
      def train_double(self):
          if self.memory.pointer < self.batch_size:
             return 0,0
          with tf.GradientTape() as tape:
              states, actions, rewards, next_states, dones = self.memory.sample_exp(self.batch_size)
              target = self.q_net(states)
              q_next = self.target_net(next_states)
              max_action = np.argmax(self.q_net(next_states),axis=1)
              q_target = np.copy(target)
              maxq=tf.reduce_mean(tf.math.reduce_max(target, axis=1,keepdims=True).numpy())
              for idx, terminal in enumerate(dones):
                  if terminal:
                      q_target[idx][actions[idx]]=rewards[idx]
                  else:
                      q_target[idx][actions[idx]]=rewards[idx]+self.gamma*q_next[idx,max_action[idx]]
              loss=tf.reduce_mean((q_target-target)**2)
              #print(loss)
          gradient= tape.gradient(loss,self.q_net.trainable_variables)
          self.q_net.optimizer.apply_gradients(zip(gradient,self.q_net.trainable_variables))
          self.trainstep += 1
          return float(maxq.numpy()),float(loss.numpy())
class IotaQAgent():
      def __init__(self, gamma=0.99, replace=100, lr=0.001,n_actions=2,input_shape=[0,0],buffer_size= 50000,batch_size=64,lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,bacth_size=64):
          self.buffer_size = buffer_size
          self.batch_size = bacth_size
          self.input_shape=input_shape
          self.lambda_1=lambda_1
          self.lambda_2=lambda_2
          self.lambda_3=lambda_3
          self.n_actions=n_actions
          self.gamma = gamma
          self.epsilon = 1.0
          self.min_epsilon = 0.01
          self.epsilon_decay = 1e-3
          self.replace = replace
          self.trainstep = 0
          self.memory = ReplayBufferIota(input_shape=self.input_shape,buffer_size=self.buffer_size)
          
          self.q_net = DQN()
          self.target_net = DQN()
          opt = tf.keras.optimizers.Adam(learning_rate=lr)
          self.q_net.compile(loss='mse', optimizer=opt)
          self.target_net.compile(loss='mse', optimizer=opt)
      def act(self, state):
          if np.random.rand() <= self.epsilon:
              return np.random.choice([i for i in range(self.n_actions)], p=[0.9, 0.1]), False
          else:
              state=tf.convert_to_tensor([state.flatten()],dtype=tf.float32)
              actions = self.q_net(state)
              action = np.argmax(actions)
              return action,True
      def epsilon_policy(self,epsilon,observation,iota):
          choice=[]
          amax=False
          if np.random.uniform(0,1)<epsilon:
            for i in range(0,len(iota)):
              if iota[i]>0:
                choice.append(i)
            if len(choice)>0:
              action=np.random.choice(np.array(choice))
            else:
              action=np.random.choice([i for i in range(self.n_actions)], p=[0.9, 0.1])
          else:
            action,amax=self.choose_action(observation,iota)
            amax=True
            #print(iota,action)
          return action,amax 
      def choose_action(self,observation,iota):
         state=tf.convert_to_tensor([observation.flatten()],dtype=tf.float32)
         probs=self.q_net(state)[0]
         #print(probs)
         probabilities=[]
         choices=[]
         for i in range(0,len(iota)):
           if iota[i]>0:
             probabilities.append(probs[i])
             choices.append(i)
           if len(probabilities)>0:
             action=choices[np.argmax(np.array(probabilities))]
             argmax=np.amax(np.array(probabilities))
           else:
             action=0
             argmax=None
         return action,argmax
      def update_mem(self, state, action, reward, next_state, done,iota,iota_):
          self.memory.add_exp(state, action, reward, next_state, done,iota,iota_)
      def update_target(self):
          self.target_net.set_weights(self.q_net.get_weights())     

      def update_epsilon(self):
          self.epsilon = self.epsilon - self.epsilon_decay if self.epsilon > self.min_epsilon else self.min_epsilon
          return self.epsilon
      def train_simple(self):
          if self.memory.pointer < self.batch_size:
             return 0,0
          with tf.GradientTape() as tape:
              states, actions, rewards, next_states, dones,iota, iota_= self.memory.sample_exp(self.batch_size)
              target = self.q_net(states)
              min_arg=tf.math.reduce_min(target, axis=1,keepdims=True).numpy()
              target_iota=target+abs(min_arg)
              max_iota=tf.math.reduce_max((target_iota*iota)[0], axis=1,keepdims=True).numpy()-abs(min_arg)
              max_real=tf.math.reduce_max(target, axis=1,keepdims=True).numpy()
              loss_iota=(max_iota-max_real)
              loss_iota[loss_iota>=0.]=0.
              ####
              q_next=self.target_net(next_states)
              min_arg=tf.math.reduce_min(q_next, axis=1,keepdims=True).numpy()
              q_next_iota_=target+abs(min_arg)
              max_iota_=tf.math.reduce_max((q_next_iota_*iota_)[0], axis=1,keepdims=True).numpy()-abs(min_arg)
              max_real_=tf.math.reduce_max(q_next, axis=1,keepdims=True).numpy()
              loss_iota_=(max_iota_-max_real_)
              q_target = np.copy(target)  #optional  
              maxq=tf.reduce_mean(tf.math.reduce_max(target, axis=1,keepdims=True).numpy())
              for idx, terminal in enumerate(dones):
                  if terminal:
                      max_iota_[idx]=0.0
                  q_target[idx,actions[idx]]=rewards[idx]+self.gamma*max_iota_[idx]
              loss=tf.reduce_mean(self.lambda_1*(q_target-target)**2)+tf.reduce_mean(self.lambda_2*loss_iota**2)+tf.reduce_mean(self.lambda_3*loss_iota_**2)
              #print(loss)
          gradient= tape.gradient(loss,self.q_net.trainable_variables)
          self.q_net.optimizer.apply_gradients(zip(gradient,self.q_net.trainable_variables))
          self.trainstep += 1
          return float(maxq.numpy()),float(loss.numpy())
      def train_double(self):
          if self.memory.pointer < self.batch_size:
             return 0,0
          with tf.GradientTape() as tape:
              states, actions, rewards, next_states, dones,iota, iota_= self.memory.sample_exp(self.batch_size)
              
              target = self.q_net(states)#
              q_next_main=self.q_net(next_states)
              #####
              min_arg=tf.math.reduce_min(target, axis=1,keepdims=True).numpy()
              target_iota=target+abs(min_arg)
              max_iota=tf.math.reduce_max((target_iota*iota)[0], axis=1,keepdims=True).numpy()-abs(min_arg)
              max_real=tf.math.reduce_max(target, axis=1,keepdims=True).numpy()
              loss_iota=(max_iota-max_real)
              loss_iota[loss_iota>=0.]=0.
              #####
              q_next=self.target_net(next_states)#Hay que agarrar este valor en la loss
              ###
              min_arg=tf.math.reduce_min(q_next_main, axis=1,keepdims=True).numpy()
              q_next_iota_=target+abs(min_arg)
              max_iota_=tf.math.reduce_max((q_next_iota_*iota_)[0], axis=1,keepdims=True).numpy()-abs(min_arg)
              max_action = np.argmax(max_iota_,axis=1)
              max_real_=tf.math.reduce_max(q_next_main, axis=1,keepdims=True).numpy()
              loss_iota_=(max_iota_-max_real_)
              q_target = np.copy(target)  #optional  
              maxq=tf.reduce_mean(tf.math.reduce_max(target, axis=1,keepdims=True).numpy())
              ######
              for idx, terminal in enumerate(dones):
                  if terminal:
                      q_target[idx][actions[idx]]=rewards[idx]
                  else:
                      q_target[idx][actions[idx]]=rewards[idx]+self.gamma*q_next[idx,max_action[idx]]  
              loss=tf.reduce_mean(self.lambda_1*(q_target-target)**2)+tf.reduce_mean(self.lambda_2*loss_iota**2)+tf.reduce_mean(self.lambda_3*loss_iota_**2)
              #print(loss)
          gradient= tape.gradient(loss,self.q_net.trainable_variables)
          self.q_net.optimizer.apply_gradients(zip(gradient,self.q_net.trainable_variables))
          self.trainstep += 1
          return float(maxq.numpy()),float(loss.numpy())