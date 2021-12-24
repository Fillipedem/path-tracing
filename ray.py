import numpy as np 

class Ray():

    def __init__(self, p, v, pixel=None):
        self.p = p 
        self.v = v
        self.pixel = pixel