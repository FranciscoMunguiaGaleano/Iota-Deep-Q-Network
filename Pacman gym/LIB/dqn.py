import tensorflow as tf

class DQN(tf.keras.Model):
    def __init__(self,n_actions=4,fc1_dims=600,fc2_dims=600):
        super().__init__()
        self.n_actions=n_actions
        self.fc1_dims=fc1_dims
        self.fc2_dims=fc2_dims
        self.d0 = tf.keras.layers.Flatten()
        self.d1 = tf.keras.layers.Dense(self.fc1_dims,activation='relu')
        self.d2 = tf.keras.layers.Dense(self.fc2_dims,activation='relu')
        self.q_values = tf.keras.layers.Dense(self.n_actions,activation='linear')
        
    def call(self, state):
        x = tf.convert_to_tensor(state)
        x = self.d0(x)
        x = self.d1(x)
        x = self.d2(x)
        x = self.q_values(x)
        return x
    
class DDDQN(tf.keras.Model):
    def __init__(self,n_actions=4,fc1_dims=600,fc2_dims=600):
      super(DDDQN, self).__init__()
      self.n_actions=n_actions
      self.fc1_dims=fc1_dims
      self.fc2_dims=fc2_dims
      self.d1 = tf.keras.layers.Dense(self.fc1_dims, activation='relu')
      self.d2 = tf.keras.layers.Dense(self.fc2_dims, activation='relu')
      self.v = tf.keras.layers.Dense(1, activation=None)
      self.a = tf.keras.layers.Dense(self.n_actions, activation=None)

    def call(self, state):
      x = tf.convert_to_tensor(state)
      x = self.d1(x)
      x = self.d2(x)
      v = self.v(x)
      a = self.a(x)
      Q = v +(a -tf.math.reduce_mean(a, axis=1, keepdims=True))
      return Q

    def advantage(self, state):
      x = tf.convert_to_tensor(state)
      x = self.d1(x)
      x = self.d2(x)
      a = self.a(x)
      return a