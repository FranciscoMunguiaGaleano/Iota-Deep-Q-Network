import sys
import os

LOCAL_PATH=os.path.dirname(os.path.abspath(__file__))
MAIN_PATH=LOCAL_PATH+'/../..'


ENV_PATH=MAIN_PATH+"/LIB/GAME"
LIB_PATH=MAIN_PATH+"/LIB"
TRN_PATH=MAIN_PATH+"/LIB/TRAINING"

sys.path.insert(1, ENV_PATH)
sys.path.insert(1, TRN_PATH)
sys.path.insert(1, LIB_PATH)

from game import Flappy_v1_0 as envi
from agents import *
from constants import *
import yaml


CONF_PATH=MAIN_PATH+"/CONF"
DEMO_PATH=MAIN_PATH+"/DEMO"
DOC_PATH=MAIN_PATH+"/DOC"
ENV_PATH=MAIN_PATH+"/LIB/GAME"
LIB_PATH=MAIN_PATH+"/LIB"
LOG_PATH=MAIN_PATH+"/LOG"
IMG_PATH=MAIN_PATH+"/IMG"
POLICIES_PATH=MAIN_PATH+"/BIN"
TEMP_PATH=MAIN_PATH+"/TEMP"
TRN_PATH=MAIN_PATH+"/LIB/TRAINING"


class IDuDQL:
    def __init__(self ,lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1"):
        print("Iota Dueling Deep Q-Learning FlappyBirds environment training")
        pygame.init()
        pygame.display.set_caption("FlappyBirds")
        self.lambda_1=lambda_1
        self.lambda_2=lambda_2
        self.lambda_3=lambda_3
        self.experiment_name="idudql"+lambda_
        self.experiment_name_="idudql"
        self.n_actions,self.max_epochs,self.max_episodes,self.max_steps,self.max_e,self.min_e,self.e_decay,self.w_updates,self.t_updates,self.t_steps,self.mini_batch_size,self.max_queue_length=self.load_params(CONF_PATH)
        self.environment=envi()
        s=self.environment.reset()
        self.agente=IotaDuelingAgent(n_actions=self.n_actions,input_shape=s.flatten().shape,buffer_size=self.max_queue_length,batch_size=self.mini_batch_size,lambda_1=self.lambda_1,lambda_2=self.lambda_2,lambda_3=self.lambda_3)
        self.state=tf.convert_to_tensor([s.flatten()],dtype=tf.float32)
        self.agente.q_net(self.state)
        self.agente.target_net(self.state)
        self.rtrn=[]
        self.avg_r=[]
        self.loss=[]
        self.loss_avg=[]
        self.max_q_net=[]
        self.max_q_net_avg=[]
        #self.actions={0:JUMP_STRONG,1:RIGHT_R}
        self.environment.dt=30.0/1000.0
    def epoch_training(self):
        print("Epoch training")
        epoch=0
        weight_updates=0
        step_num=0
        rwd=0
        rwd_nn=0
        avg_r_nn=[]
        avg_r=[]
        avg_maxq=[]
        avg_loss=[]
        eoe_avg_r=[]
        eoe_avg_r_nn=[]
        eoe_avg_maxq=[]
        eoe_avg_loss=[]
        Rtrn=[]
        eoe_Rtrn=[]
        Rtrn_nn=[]
        eoe_Rtrn_nn=[]
        loss=[]
        eoe_loss=[]
        maxq=[]
        eoe_maxq=[]
        while epoch<self.max_epochs:
            d=False
            expert_action=False
            s=self.environment.reset()
            action=self.agente.act(s)
            Rtrn.append(rwd)
            eoe_Rtrn.append(rwd)
            Rtrn_nn.append(rwd_nn)
            eoe_Rtrn_nn.append(rwd_nn)
            rwd=0
            rwd_nn=0
            while not d:
                step_num+=1
                if step_num==self.max_steps:
                    break
                for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                      pygame.quit()
                self.agente.epsilon= self.min_e + (self.max_e - self.min_e) * np.exp(-self.e_decay*(epoch))
                iota=self.environment.iota()
                #action,nn=self.agente.act(s)
                action,nn=self.agente.epsilon_policy(self.agente.epsilon,s,iota)
                s_,r,d,_=self.environment.step(action)
                self.environment.render()
                iota_=self.environment.iota()
                rwd+=r
                if nn:
                    rwd_nn+=r
                state=tf.convert_to_tensor([s.flatten()],dtype=tf.float32)
                state_=tf.convert_to_tensor([s_.flatten()],dtype=tf.float32)
                self.agente.update_mem(state, action, r, state_, d,iota,iota_)
                if step_num%self.t_steps==0 and step_num>1:
                      q_max,loss_t=self.agente.train_simple()
                      weight_updates+=1
                      loss.append(float(loss_t))
                      maxq.append(float(q_max))
                      eoe_loss.append(float(loss_t))
                      eoe_maxq.append(float(q_max))
                      if weight_updates%self.w_updates==0 and weight_updates>0:
                          epoch+=1
                          print("[",self.experiment_name,"]Training Epoch ",epoch," of ",self.max_epochs, "Weigth updates: ",weight_updates)
                          self.agente.q_net.save(POLICIES_PATH+"/"+self.experiment_name)
                          avg_r.append(sum(Rtrn)/len(Rtrn))
                          avg_r_nn.append(sum(Rtrn_nn)/len(Rtrn_nn))
                          avg_maxq.append(sum(maxq)/len(maxq)) 
                          avg_loss.append(sum(loss)/len(loss)) 
                          eoe_avg_r.append(sum(eoe_Rtrn)/len(eoe_Rtrn))
                          eoe_avg_r_nn.append(sum(eoe_Rtrn_nn)/len(eoe_Rtrn_nn))
                          eoe_avg_maxq.append(sum(eoe_maxq)/len(eoe_maxq)) 
                          eoe_avg_loss.append(sum(eoe_loss)/len(eoe_loss))
                          self.save_data(TEMP_PATH,self.experiment_name,avg_r,avg_maxq,avg_loss,eoe_avg_r,avg_r_nn,eoe_avg_maxq,eoe_avg_loss,eoe_avg_r_nn)
                          eoe_Rtrn=[]
                          eoe_loss=[]
                          eoe_maxq=[]
                          break
                s=s_
                if weight_updates%self.t_updates==0 and  weight_updates>0:
                    self.agente.target_net.set_weights(self.agente.q_net.get_weights())
                if self.environment.done:
                    break
                if self.environment.done:
                    d=True 
    def episode_training(self,mode):
        normal=False
        if mode=="iota":
            print("Episode training random")
            name="iota_episodes"
            epsilon=1.0
        else:
            print("Episode training ",self.experiment_name)
            name=self.experiment_name+"_episodes"
            normal=True
        episode=0
        weight_updates=0
        step_num=0
        rwd=0
        rwd_nn=0
        avg_r_nn=[0]
        avg_r=[0]
        avg_maxq=[0]
        avg_loss=[0]
        eoe_avg_r=[0]
        eoe_avg_r_nn=[0]
        eoe_avg_maxq=[0]
        eoe_avg_loss=[0]
        Rtrn=[0]
        eoe_Rtrn=[0]
        Rtrn_nn=[0]
        eoe_Rtrn_nn=[0]
        loss=[0]
        eoe_loss=[0]
        maxq=[0]
        eoe_maxq=[0]
        while episode<self.max_episodes:
            episode+=1
            d=False
            expert_action=False
            s=self.environment.reset()
            action=self.agente.act(s)
            Rtrn.append(rwd)
            eoe_Rtrn.append(rwd)
            Rtrn_nn.append(rwd_nn)
            eoe_Rtrn_nn.append(rwd_nn)
            rwd=0
            rwd_nn=0
            while not d:
                step_num+=1
                if step_num==self.max_steps:
                    break
                for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                      pygame.quit()
                iota=self.environment.iota()
                if normal:
                    self.agente.epsilon= self.min_e + (self.max_e - self.min_e) * np.exp(-self.e_decay*(episode))
                    action,nn=self.agente.epsilon_policy(self.agente.epsilon,s,iota)
                else:
                    self.agente.epsilon=1.0
                    action,nn=self.agente.epsilon_policy(self.agente.epsilon,s,iota)                
                s_,r,d,_=self.environment.step(action)
                self.environment.render()
                iota_=self.environment.iota()
                rwd+=r
                if nn:
                    rwd_nn+=r
                state=tf.convert_to_tensor([s.flatten()],dtype=tf.float32)
                state_=tf.convert_to_tensor([s_.flatten()],dtype=tf.float32)
                self.agente.update_mem(state, action, r, state_, d,iota,iota_)
                if step_num%self.t_steps==0 and step_num>1:
                    if normal:
                        q_max,loss_t=self.agente.train_simple()
                        weight_updates+=1
                        loss.append(float(loss_t))
                        maxq.append(float(q_max))
                        eoe_loss.append(float(loss_t))
                        eoe_maxq.append(float(q_max))

                s=s_
                if normal:
                    if weight_updates%self.t_updates==0 and  weight_updates>0:
                        self.agente.target_net.set_weights(self.agente.q_net.get_weights())
                if self.environment.done:
                    break
                if self.environment.done:
                    d=True
            print("[",name,"]Training Episode ",episode," of ",self.max_episodes)
            if normal:
                self.agente.q_net.save(POLICIES_PATH+"/"+name)
                avg_r_nn.append(sum(Rtrn_nn)/len(Rtrn_nn))
                avg_maxq.append(sum(maxq)/len(maxq)) 
                avg_loss.append(sum(loss)/len(loss)) 
                
                eoe_avg_r_nn.append(sum(eoe_Rtrn_nn)/len(eoe_Rtrn_nn))
                eoe_avg_maxq.append(sum(eoe_maxq)/len(eoe_maxq)) 
                eoe_avg_loss.append(sum(eoe_loss)/len(eoe_loss))
            eoe_avg_r.append(sum(eoe_Rtrn)/len(eoe_Rtrn))
            avg_r.append(sum(Rtrn)/len(Rtrn))
            self.save_data(TEMP_PATH,name,avg_r,avg_maxq,avg_loss,eoe_avg_r,avg_r_nn,eoe_avg_maxq,eoe_avg_loss,eoe_avg_r_nn)
            eoe_Rtrn=[0]
            eoe_loss=[0]
            eoe_maxq=[0]
    def load_params(self,path):
        with open(r''+path+"/"+self.experiment_name_+"_conf.yaml") as parameters:
            config_list = yaml.safe_load(parameters)
        #HYPERPARAMETERS
        mini_batch_size=config_list['training']['mini_batch_size']##
        n_actions=config_list['training']['num_actions']##
        learning_rate=config_list['training']['learning_rate']
        max_episodes=config_list['training']['num_episodes']##
        max_epochs=config_list['training']['num_epochs']##
        max_e=config_list['epsilon']['max_epsilon']
        max_steps=config_list['rl']['max_steps_per_episode']##
        max_queue_length=config_list['rl']['max_queue_length']##
        min_e=config_list['epsilon']['min_epsilon']
        e_decay=config_list['epsilon']['decay_epsilon']
        w_updates=config_list['training']['weight_updates']##
        t_steps=config_list['training']['train_steps']##
        t_updates=config_list['rl']['target_update_episodes']##
        return n_actions,max_epochs,max_episodes,max_steps,max_e,min_e,e_decay,w_updates,t_updates,t_steps,mini_batch_size,max_queue_length       
    def save_data(self,path,name,avg_r,avg_maxq,avg_loss,eoe_avg_r,avg_r_nn,eoe_avg_maxq,eoe_avg_loss,eoe_avg_r_nn):
        with open(r''+path+"/"+name+'.yaml', 'w') as outfile:
                           data={'avr_r':avg_r,
                                 'avr_maxq':avg_maxq,
                                 'avr_loss':avg_loss,
                                 'avg_r_nn':avg_r_nn,
                                 'eoe_avr_r':eoe_avg_r,
                                 'eoe_avr_maxq':eoe_avg_maxq,
                                 'eoe_avr_loss':eoe_avg_loss,
                                 'eoe_avg_r_nn':eoe_avg_r_nn,}
                           yaml.dump(data, outfile, default_flow_style=False)
        return

if __name__ == "__main__":
    print("Training FlappyBirds environment with IDuDQL")
    env=IDuDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    env.epoch_training()
    env=IDuDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    env.epoch_training()
    env=IDuDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    env.epoch_training()
    env=IDuDQL(lambda_1=1.0,lambda_2=0.0,lambda_3=0.0,lambda_="l1")
    env.episode_training("idudqdll1")
    env=IDuDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=0.0,lambda_="l1l2")
    env.episode_training("idudqdll1l2")
    env=IDuDQL(lambda_1=1.0,lambda_2=1.0,lambda_3=1.0,lambda_="l1l2l3")
    env.episode_training("idudqdll1l2l3")
    pygame.quit()