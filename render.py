"""
PATH TRACING Python Implementation
"""
import random
import numpy as np
from scene.ray import Ray

class PathTracing():

    def __init__(self, camera, scene_objects, lights, ambient = 0.5):
        self.camera = camera 
        self.scene_objects = scene_objects 
        self.lights = lights
        self.ambient = ambient

    def path_tracing(self, ray):
        I = np.zeros(3)
        ray_intersection = self.find_intersection(ray)

        # get color + shadow ray
        if ray_intersection:
            obj, point, normal = ray_intersection

            if obj.is_light:
                return obj.light_color

            I += self.phong(ray, obj, point, normal)

            # send secundary rays        
            I += self.secundary_ray(point, normal, ray, obj)

        return I

    def secundary_ray(self, point, normal, orig_ray, obj):
        """Cast secundary ray(diffuse/specular/transparent)"""
        I = np.zeros(3)
        ktot = obj.properties.kd + obj.properties.ks + obj.properties.kt
        rand = random.uniform(0, ktot)
    
        if rand < obj.properties.kd:                         # DIFFUSE
            V = orig_ray.p-point
            V = V/np.linalg.norm(V)
            vec = self.get_diffuse_vector(normal, V)
            ray = Ray(point, vec)

            I = self.get_color(ray)*obj.properties.kd
    
        elif rand < obj.properties.ks:                       # SPECULAR
            for light in self.lights:
                light_point = light.get_point()
                L = light_point - point
                L = L/np.linalg.norm(L)
                R = 2*normal*np.dot(normal, L) - L
                R = R/np.linalg.norm(R)
        
                ray = Ray(point, R)
        
                I = self.get_color(ray)*obj.properties.ks
        else:                                                       # Transparent
            pass 

        return I

    def get_diffuse_vector(self, normal , V):
        """Return a difuse vector given a normal V vector"""
        e1, e2 = random.random(), random.random()
        a, b = np.arccos(np.sqrt(e1)), 2*np.pi*e2

        normal = normal/np.linalg.norm(normal)
        S = np.cross(normal, V)
        S = S/np.linalg.norm(S)
        V = np.cross(S, normal)
        V = V/np.linalg.norm(V)

        matrix = np.array([S, V, normal])

        new_vector = np.array((
            np.sin(a)*np.cos(b),
            np.sin(a)*np.sin(b),
            np.cos(a)
            )
        )

        return matrix.transpose()@new_vector

    def find_intersection(self, ray):
        """Return the closest intersection given a ray object
        
        Returns:
            (intersected_obj, point, normal)
        """
        min_d = np.inf
        intersection = None
        for scene_obj in self.scene_objects:
            for obj in scene_obj.objects:
                point = obj.intersect(ray)
                if point is not None:
                    distance = np.linalg.norm(ray.p - point)
                    if distance < min_d:
                        intersection = (scene_obj, point, obj.normal)
                        min_d = distance
        return intersection


    def phong(self, ray, obj, point, normal):
        """Return object color, given observer ray, intersected object"""
        I = obj.properties.color*obj.properties.ka*self.ambient
        
        V = ray.p - point
        V = V/np.linalg.norm(V)
        
        for light in self.lights:
            light_point = light.get_point()
            if self.is_shadowed(point, light_point):
                continue

            L = light_point - point 
            L = L/np.linalg.norm(L)
            R = 2*normal*np.dot(normal, L) - L
            R = R/np.linalg.norm(R)

            diffuse = light.lp*obj.properties.kd*np.dot(L, normal)*obj.properties.color
            specular = light.lp*obj.properties.ks*(np.dot(R, V)**obj.properties.n)*np.ones(3)
            I += diffuse + specular

        return I

    def is_shadowed(self, point, light_point):
        """return True if there is a object between the point and the light, false otherwise"""
        shadow_ray = Ray(point, light_point - point)
        distance = np.linalg.norm(light_point - point)
        shadow_intersection = self.find_intersection(shadow_ray)
        if shadow_intersection:
            obj, p, _ = shadow_intersection
            if obj.is_light:
                return False
            if np.linalg.norm(p - point) < distance:
                return True

        return False

    def get_color(self, ray):
        """return the color(phong) of the first intersected object"""
        I = np.zeros(3)
        ray_intersection = self.find_intersection(ray)
                
        if ray_intersection:
            obj, point, normal = ray_intersection 

            if obj.is_light:
                return obj.light_color

            I = self.phong(ray, obj, point, normal)

        return I