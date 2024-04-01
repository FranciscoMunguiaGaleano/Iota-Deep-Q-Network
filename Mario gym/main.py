"""
Created on Mon Jan  10  2022

@author: Francisco Munguia Galeano
"""
import sys
import os

MAIN_PATH=os.path.dirname(os.path.abspath(__file__))

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

from game import Mario_v1_0 as env
from constants import *
import yaml
import time
import numpy as np
from IPython.display import clear_output
import seaborn as sns
from matplotlib import pyplot as plt
import yaml
import sys
import os
import numpy as np
import tensorflow as tf
from dql import DQL
from ddql import DDQL
from dudql import DuDQL
from dddql import DDDQL
from idql import IDQL
from iddql import IDDQL
from idudql import IDuDQL
from idddql import IDDDQL


if __name__ == "__main__":
    #print("Training Mario envirnment with DQL")
    #env=DQL()
    #env.epoch_training()
    #env.episode_training("random")
    #env.episode_training("qdl")
    #pygame.quit()
    #print("Training Mario envirnment with DDQL")
    #env=DDQL()
    #env.epoch_training()
    #env.episode_training("ddqdl")
    #pygame.quit()
    #print("Training Mario envirnment with DuDQL")
    #env=DuDQL()
    #env.epoch_training()
    #env.episode_training("dudqdl")
    #pygame.quit()
    #print("Training Mario environment with DDDQL")
    #env=DDDQL()
    #env.epoch_training()
    #env.episode_training("dddqdl")
    #pygame.quit()
    print("Training Mario environment with IDQL")
    env=IDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    env.epoch_training()
    env=IDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    env.epoch_training()
    env=IDQL(lambda_1=1.0,lambda_2=0.5,lambda_3=0.0,lambda_="l1l2exp1")
    env.epoch_training()
    env=IDQL(lambda_1=1.0,lambda_2=5.0,lambda_3=0.0,lambda_="l1l2exp2")
    env.epoch_training()
    env=IDQL(lambda_1=1.0,lambda_2=10.0,lambda_3=0.0,lambda_="l1l2exp3")
    env.epoch_training()
    #env=IDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    #env.epoch_training()
    #env=IDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    #env.episode_training("iota")
    #env=IDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    #env.episode_training("iqdll1")
    #env=IDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    #env.episode_training("iqdll1l2")
    #env=IDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    #env.episode_training("iqdll1l2l3")
    pygame.quit()
    print("Training Mario environment with IDDQL")
    env=IDDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    env.epoch_training()
    env=IDDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    env.epoch_training()
    env=IDDQL(lambda_1=1.0,lambda_2=0.5,lambda_3=0.0,lambda_="l1l2exp1")
    env.epoch_training()
    env=IDDQL(lambda_1=1.0,lambda_2=5.0,lambda_3=0.0,lambda_="l1l2exp2")
    env.epoch_training()
    env=IDDQL(lambda_1=1.0,lambda_2=10.0,lambda_3=0.0,lambda_="l1l2exp3")
    env.epoch_training()
    #env=IDDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    #env.epoch_training()
    #env=IDDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    #env.episode_training("iddqdll1")
    #env=IDDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    #env.episode_training("iddqdll1l2")
    #env=IDDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    #env.episode_training("iddqdll1l2l3")
    pygame.quit()
    print("Training Mario environment with IDuDQL")
    env=IDuDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    env.epoch_training()
    env=IDuDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    env.epoch_training()
    env=IDuDQL(lambda_1=1.0,lambda_2=0.5,lambda_3=0.0,lambda_="l1l2exp1")
    env.epoch_training()
    env=IDuDQL(lambda_1=1.0,lambda_2=5.0,lambda_3=0.0,lambda_="l1l2exp2")
    env.epoch_training()
    env=IDuDQL(lambda_1=1.0,lambda_2=10.0,lambda_3=0.0,lambda_="l1l2exp3")
    env.epoch_training()
    #env=IDuDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    #env.epoch_training()
    #env=IDuDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    #env.episode_training("idudqdll1")
    #env=IDuDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    #env.episode_training("idudqdll1l2")
    #env=IDuDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    #env.episode_training("idddqdll1l2l3")
    pygame.quit()
    print("Training Mario environment with IDDDQL")
    env=IDDDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    env.epoch_training()
    env=IDDDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    env.epoch_training()
    env=IDDDQL(lambda_1=1.0,lambda_2=0.5,lambda_3=0.0,lambda_="l1l2exp1")
    env.epoch_training()
    env=IDDDQL(lambda_1=1.0,lambda_2=5.0,lambda_3=0.0,lambda_="l1l2exp2")
    env.epoch_training()
    env=IDDDQL(lambda_1=1.0,lambda_2=10.0,lambda_3=0.0,lambda_="l1l2exp3")
    env.epoch_training()
    #env=IDDDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    #env.epoch_training()
    #env=IDDDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    #env.episode_training("idddqdll1")
    #env=IDDDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    #env.episode_training("idddqdll1l2")
    #env=IDDDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    #env.episode_training("idddqdll1l2l3")
    pygame.quit()

