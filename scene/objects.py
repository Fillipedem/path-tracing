"""
Scene Objects Classes

Properties - Hold ilumination info
SceneObject - One or more scene objects
Triangles - Triangle object
"""
from random import randint
import numpy as np


class SceneObject():
    """scene object, hold a list of objects that share a commum properties"""
    def __init__(self, name, properties, objects):
        self.name = name
        self.properties = properties
        self.objects = objects

class Properties():
    """hold scene object properties"""
    def __init__(self, color, ka=None, kd=None, ks=None, kt=None, n=None, is_light=False):
        self.color = np.array(color)
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kt = kt
        self.n = n
        self.is_light = is_light

class Light():

    def __init__(self, lp, color, scene_obj):
        self.lp = lp
        self.scene_obj = scene_obj
        self.color = np.array(color)   

    def get_point(self):
        idx = randint(0, len(self.scene_obj.objects) - 1)
        return self.scene_obj.objects[idx].get_point()
