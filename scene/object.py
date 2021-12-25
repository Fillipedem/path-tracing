"""
Scene Objects Classes

Properties - Hold ilumination info
SceneObject - One or more scene objects
Triangles - Triangle object
"""
import numpy as np

class Properties():

    def __init__(self, color, ka, kd, ks, kt, n):
        self.color = color
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kt = kt
        self.n = n

class AbstractIntersect():

    def __init__(self):
        pass

    def intersect(self, ray):
        raise NotImplemented("Intersect not implemented")

class SceneObject(AbstractIntersect):
    
    def __init__(self, properties, objects):
        self.properties = properties
        self.objects = objects

    def intersect(self, ray):
        inter_list = []
        for obj in self.objects:
            point = obj.intersect(ray)
            if point:
                inter_list.append((point, obj.norm))

class Triangles(AbstractIntersect):
    
    def __init__(self, p1, p2, p3):
        self.p = (p1 + p2 + p3)/3
        self.norm = np.cross(p2-p1,p3-p2)

        max_d = np.linalg.norm(self.p - p1)
        max_d = max(p1, np.linalg.norm(self.p - p2))
        max_d = max(p2, np.linalg.norm(self.p - p3))
        self.max_d = max_d

    def intersect(self, ray):
        """Checks if the ray intersect"""
        # check if ray is parallel to the object
        denominator = np.dot(ray.v, self.norm)
        if denominator == 0: 
            return None

        # check if object is behind the ray starting point
        t = np.dot((self.p0 - ray.p), self.norm)/denominator
        if t < 0:             
            return None 

        # check if the point is inside the triangle
        plane_point = ray.p + ray.v*t
        if np.norm(self.p - plane_point) > self.max_d:
            return None

        return plane_point
            
        
