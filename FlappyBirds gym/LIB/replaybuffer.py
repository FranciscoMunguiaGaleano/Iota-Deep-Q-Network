# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 10:33:47 2022

@author: C1982450
"""

import numpy as np

class ReplayBufferIota():
    def __init__(self, buffer_size= 50000,iota_sample=[0.0,0.0],input_shape=[0,0]):
        self.input_shape=input_shape
        self.buffer_size = buffer_size
        self.iota_sample=iota_sample
        self.state_mem = np.zeros((self.buffer_size,*(self.input_shape)), dtype=np.float32)
        self.action_mem = np.zeros((self.buffer_size), dtype=np.int32)
        self.reward_mem = np.zeros((self.buffer_size), dtype=np.float32)
        self.next_state_mem = np.zeros((self.buffer_size,*(self.input_shape)), dtype=np.float32)
        self.iota_mem=np.zeros((self.buffer_size,*(np.array([self.iota_sample]).shape)),dtype=np.float32)
        self.iota__mem=np.zeros((self.buffer_size,*(np.array([self.iota_sample]).shape)),dtype=np.float32)
        self.done_mem = np.zeros((self.buffer_size), dtype=np.bool)
        self.pointer = 0

    def add_exp(self, state, action, reward, next_state, done,iota,iota_):
        idx  = self.pointer % self.buffer_size 
        self.state_mem[idx] = state
        self.action_mem[idx] = action
        self.reward_mem[idx] = reward
        self.next_state_mem[idx] = next_state
        self.iota_mem[idx] = np.array([iota])
        self.iota__mem[idx] = np.array([iota_])
        self.done_mem[idx] = 1 - int(done)
        self.pointer += 1

    def sample_exp(self, batch_size= 64):
        max_mem = min(self.pointer, self.buffer_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)
        states = self.state_mem[batch]
        actions = self.action_mem[batch]
        rewards = self.reward_mem[batch]
        next_states = self.next_state_mem[batch]
        dones = self.done_mem[batch]
        iota=self.iota_mem[batch]
        iota_=self.iota__mem[batch]
        return states, actions, rewards, next_states, dones,iota,iota_
class ReplayBuffer():
    def __init__(self, buffer_size= 50000,input_shape=[0,0]):
        self.buffer_size = buffer_size
        self.input_shape=input_shape
        self.state_mem = np.zeros((self.buffer_size,*(self.input_shape)), dtype=np.float32)
        self.action_mem = np.zeros((self.buffer_size), dtype=np.int32)
        self.reward_mem = np.zeros((self.buffer_size), dtype=np.float32)
        self.next_state_mem = np.zeros((self.buffer_size,*(self.input_shape)), dtype=np.float32)
        self.done_mem = np.zeros((self.buffer_size), dtype=np.bool)
        self.pointer = 0

    def add_exp(self, state, action, reward, next_state, done):
        idx  = self.pointer % self.buffer_size 
        self.state_mem[idx] = state
        self.action_mem[idx] = action
        self.reward_mem[idx] = reward
        self.next_state_mem[idx] = next_state
        self.done_mem[idx] = 1 - int(done)
        self.pointer += 1

    def sample_exp(self, batch_size= 64):
        max_mem = min(self.pointer, self.buffer_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)
        states = self.state_mem[batch]
        actions = self.action_mem[batch]
        rewards = self.reward_mem[batch]
        next_states = self.next_state_mem[batch]
        dones = self.done_mem[batch]
        return states, actions, rewards, next_states, dones