"""
Scene Objects Classes

Properties - Hold ilumination info
SceneObject - One or more scene objects
Triangles - Triangle object
"""
import numpy as np

class Properties():

    def __init__(self, color, ka, kd, ks, kt, n):
        self.color = np.array(color)
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kt = kt
        self.n = n

class Light():

    def __init__(self, point, color, lp):
        self.lp = lp
        self.point = np.array(point)
        self.color = np.array(color)   


class AbstractIntersect():

    def __init__(self):
        pass

    def intersect(self, ray):
        raise NotImplemented("Intersect not implemented")


class SceneObject():
    
    def __init__(self, name, properties, objects):
        self.name = name
        self.properties = properties
        self.objects = objects


class Triangles(AbstractIntersect):
    
    def __init__(self, p1, p2, p3):
        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)

        self.p = (p1 + p2 + p3)/3
        self.normal = np.cross(p2-p1,p3-p2)
        self.normal = self.normal/np.linalg.norm(self.normal)
        self.p1 = p1 
        self.p2 = p2 
        self.p3 = p3
        self.edge1 = p2 - p1
        self.edge2 = p3 - p2
        self.edge3 = p1 - p3
    

    def intersect(self, ray):
        """Checks if the ray intersect"""
        # check if ray is parallel to the object
        denominator = np.dot(ray.v, self.normal)
        if denominator == 0: 
            return None

        # check if object is behind the ray starting point
        t = np.dot((self.p - ray.p), self.normal)/denominator
        if t < 0.01:             
            return None 

        # check if the point is inside the triangle
        point = ray.p + ray.v*t

        if self.__inside_outside(point):
            return point
        else:
            return None
            
        
    def __inside_outside(self, point):
        c1 = point - self.p1
        c2 = point - self.p2
        c3 = point - self.p3

        inside = (
            np.dot(self.normal, np.cross(self.edge1, c1)) > 0 and 
            np.dot(self.normal, np.cross(self.edge2, c2)) > 0 and 
            np.dot(self.normal, np.cross(self.edge3, c3)) > 0
        )

        return inside

