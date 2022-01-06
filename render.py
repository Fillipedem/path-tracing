"""
PATH TRACING Python Implementation
"""
import random
import numpy as np

from scene.ray import Ray
from scene.intersection import Intersection

from help import sampling_up_hemisphere, snell_law


class PathTracing():

    def __init__(self, camera, scene_objects, lights, ambient = 0.5):
        self.camera = camera 
        self.scene_objects = scene_objects 
        self.lights = lights
        self.ambient = ambient

    def path_tracing(self, ray):
        """1 path for a given ray"""
        I = np.zeros(3)
        intersection = self.__send_ray(ray)

        if intersection:
            obj_properties = intersection.obj_properties

            if obj_properties.is_light:
                return obj_properties.color

            I += self.__illumination(intersection.point ,intersection.normal, intersection.orig_ray.p, obj_properties) 
 
            ## send secundary ray
            #ktot = obj_properties.kd + obj_properties.ks + obj_properties.kt
            #rand = random.uniform(0, ktot)
            #
            #if rand < obj_properties.kd:                           
            #    V = ray.p-point
            #    V = V/np.linalg.norm(V)
            #    vec = sampling_up_hemisphere()(V, normal)
            #    ray = Ray(point, vec)
            #
            #    I = self.__get_color(ray)*obj_properties.kd
            #
            #elif rand < obj_properties.kd + obj_properties.ks:     
            #    for light in self.lights:
            #        light_point = light.get_point()
            #        L = light_point - point
            #        L = L/np.linalg.norm(L)
            #        R = 2*normal*np.dot(normal, L) - L
            #        R = R/np.linalg.norm(R)
            #        
            #        ray = Ray(point, R)
            #        
            #        I = self.__get_color(ray)*obj_properties.ks
            #else:                                                  
            #    T = snell_law(ray.v, normal)
            #    ray = Ray(point, T)
            #    I = self.__get_color(ray)*obj_properties.kt

        return I

    def __send_ray(self, ray):
        """
        return closest intersection for a given ray
        
        Args:
            ray ([scene.ray.Ray]): Ray

        Returns:
            [scene.intersection.Intersection]: Intersection object
        """
        min_distance = np.inf
        intersection = None

        for scene_obj in self.scene_objects: 
            for obj in scene_obj.objects:
                point = obj.intersect(ray)
                
                if point is not None:
                    distance = np.linalg.norm(ray.p - point)

                    if distance < min_distance:
                        intersection = Intersection(
                            point=point, normal=obj.normal, obj_properties=scene_obj.properties, orig_ray=ray
                        )
                        min_distance = distance

        return intersection

    
    def __illumination(self, SP, SN, VP, obj_properties):
        """returns point color(Phong Illumination)

        Args:
            SP (np.float): Surface Point
            SN (np.float): Surface Normal
            VP (np.float): Viewer Point
            obj_properties (scene.objects.Properties): Point/obj properties

        Returns:
            [np.float]: point color
        """
        ambient = obj_properties.color*obj_properties.ka*self.ambient
        diffuse = np.zeros(3)
        specular = np.zeros(3)

        # to viewer vector
        V = VP - SP
        V = V/np.linalg.norm(V)
        
        for light in self.lights:
            light_point = light.get_point()

            if self.__is_shadowed(SP, light_point):
                continue

            L = light_point - SP 
            L = L/np.linalg.norm(L)
            R = 2*SN*np.dot(SN, L) - L
            R = R/np.linalg.norm(R)

            diffuse += light.lp*obj_properties.kd*np.dot(L, SN)*obj_properties.color
            specular += light.lp*obj_properties.ks*(np.dot(R, V)**obj_properties.n)*np.ones(3)

        return ambient + diffuse + specular

    def __is_shadowed(self, surface_point, light_point):
        """return True if there is a object between the point and the light, false otherwise"""
        shadow_ray = Ray(surface_point, light_point - surface_point)
        distance = np.linalg.norm(light_point - surface_point)

        intersection = self.__send_ray(shadow_ray)
        if intersection:

            if intersection.obj_properties.is_light:
                return False
            if np.linalg.norm(intersection.point - surface_point) < distance:
                return True

        return False

    #def __get_color(self, ray):
    #    """return the color(phong) of the first intersected object"""
    #    I = np.zeros(3)
    #    ray_intersection = self.__send_ray(ray)
    #
    #    if ray_intersection:
    #        obj, point, normal = ray_intersection 
    #
    #        if obj.is_light:
    #            return obj.light_color
    #
    #        I = self.__illumination(ray, obj, point, normal)
    #
    #    return I