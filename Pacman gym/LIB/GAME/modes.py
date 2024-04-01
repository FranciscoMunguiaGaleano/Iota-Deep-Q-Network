import sys
import os

MAIN_PATH=os.path.dirname(os.path.abspath(__file__))

class Mode(object):
    def __init__(self, name="", time=None, speedMult=1, direction=None):
        self.name = name
        self.time = time
        self.speedMult = speedMult
        self.direction = direction
