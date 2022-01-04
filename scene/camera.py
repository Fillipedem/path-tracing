from typing import List

import random
import numpy as np
from scene.ray import Ray

class Camera():

    def __init__(
            self, 
            eye: List[float], 
            target: List[float], 
            up: List[float], 
            window_size: List[float],
            pixels_size: List[int]
        ):
        self._eye = np.array(eye)
        self._target = np.array(target)
        self._up = np.array(up)
        self.window_size = window_size
        self.pixels_size = pixels_size

        self.__initialize()

    def __initialize(self):
        self.t = self._target - self._eye
        self.b = np.cross(self._up, self.t)

        self.t = self.t/np.linalg.norm(self.t)
        self.b = self.b/np.linalg.norm(self.b)
        self.v = np.cross(self.t, self.b)

        self.d = np.linalg.norm(self._target - self._eye)

    def get_rays(self):
        rays = []

        w = self.pixels_size[0]
        h = self.pixels_size[1]

        gx = self.window_size[0]/2
        gy = self.window_size[1]/2

        qx = ((2*gx)/(w - 1))*self.b
        qy = ((2*gy)/(h - 1))*self.v

        p11 = self._eye + self.t*self.d + gx*self.b + gy*self.v

        for i in range(w):
            for j in range(h):
                p = p11 - qx*i - qy*j + self.noise(qx, qy, gx/w, gy/h) # random part
                r = p - self._eye 
                R = r/np.linalg.norm(r)
                rays.append(
                    Ray(p=self._eye, v=R, pixel=(i, j))
                )

        return rays

    def noise(self, qx, qy, x, y):
        return qx*random.uniform(-x, x) + qy*random.uniform(-y, y) 