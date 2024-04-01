# Iota-Deep-Q-Network


Although reinforcement learning (RL) has demonstrated remarkable prowess in tackling intricate computational challenges, most RL algorithms lack a specific mechanism for incorporating contextual cues into learning. Conversely, humans frequently leverage context to discern patterns and relationships among environmental elements, as well as to steer clear of erroneous actions. Yet, what might appear as an evidently flawed decision from a human standpoint could entail numerous steps for an RL agent to grasp and rectify. This article introduces a framework tailored for discrete environments, termed Iota Explicit Context Representation (IECR). This framework entails the depiction of each state using contextual key frames (CKFs), which can subsequently be utilized to derive a function representing the state's affordances. Additionally, two loss functions are introduced concerning the affordances of the state. The IECR framework's innovation lies in its ability to extract contextual insights from the environment and learn from the representation of CKFs. We substantiate the framework by devising four novel algorithms that incorporate contextual learning: Iota Deep Q-Network (IDQN), Iota Double Deep Q-Network (IDDQN), Iota Dueling Deep Q-Network (IDuDQN), and Iota Dueling Double Deep Q-Network (IDDDQN). Furthermore, we assess the framework and the new algorithms across five discrete environments. We demonstrate that all algorithms leveraging contextual information converge within approximately 40,000 training steps of the neural networks, vastly surpassing their state-of-the-art counterparts.

[![Alt Text](https://img.youtube.com/vi/raVeVjPv_Rc/0.jpg)](https://www.youtube.com/watch?v=raVeVjPv_Rc)

# Aknowledgment

F. Munguia-Galeano, S. Veeramani, J. D. Hernández, Q. Wen and Z. Ji, "Affordance-based human-robot interaction with reinforcement learning," in IEEE Access, doi: 10.1109/ACCESS.2023.3262450.
