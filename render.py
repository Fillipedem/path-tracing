"""
PATH TRACING Python Implementation
"""
import random
import numpy as np

from scene.ray import Ray
from help import sampling_up_hemisphere, snell_law


class PathTracing():

    def __init__(self, camera, scene_objects, lights, ambient = 0.5, n_reflections=10):
        self.camera = camera 
        self.scene_objects = scene_objects 
        self.lights = lights
        self.ambient = ambient
        self.n_reflections = n_reflections

    def path_tracing(self, ray):
        """1 path for a given ray"""
        I = np.zeros(3)
        intersection = self.__send_ray(ray)

        if intersection:
            SP, SN, VP, obj_properties = intersection

            if obj_properties.is_light:
                return obj_properties.color

            I += self.__illumination(SP, SN, VP, obj_properties) 
            
            ###
            ### Secundary RAY
            ###
            snd_intersection = None
            new_ray, att = self.__secundary_ray(SP, SN, VP, obj_properties)
            snd_intersection = self.__send_ray(new_ray)

            for _ in range(self.n_reflections):
            
                if snd_intersection:
                    SP, SN, VP, obj_properties = snd_intersection
            
                    if obj_properties.is_light:
                        break
                    elif obj_properties.random() < obj_properties.kt:
                        # New Ray
                        V = VP-SP
                        V = V/np.linalg.norm(V)
                        new_ray = Ray(SP, snell_law(-V, SN))
                        # Find intersections
                        snd_intersection = self.__send_ray(new_ray)
                    else:
                        break
                else:
                    break
            
            if snd_intersection:
                SP, SN, VP, obj_properties = snd_intersection

                if obj_properties.is_light:
                    I += att*obj_properties.color
                else:
                    I += att*self.__illumination(SP, SN, VP, obj_properties)

        return I

    def __send_ray(self, ray):
        """
        return closest intersection for the given ray
        
        Args:
            ray ([scene.ray.Ray]): Ray

        Returns:
            surface_point, surface_normal, viewer_point, surface properties
        """
        min_distance = np.inf
        intersection = None

        for scene_obj in self.scene_objects: 
            for obj in scene_obj.objects:
                point = obj.intersect(ray)
                
                if point is not None:
                    distance = np.linalg.norm(ray.p - point)

                    if distance < min_distance:
                        intersection = point, obj.normal, ray.p, scene_obj.properties
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
            SP, _, _, obj_properties = intersection

            if obj_properties.is_light:
                return False
            if np.linalg.norm(SP - surface_point) < distance:
                return True

        return False


    def __secundary_ray(self, SP, SN, VP, properties):
        """return secundary ray(specular, transmission, diffuse)

        Args:
            SP (np.array): Surface point
            SN (np.array): Surface normal
            VP (np.array): Viewer point
            properties (scene.objects.Properties): Surface properties
        """
        att = None
        rand = random.uniform(0, properties.kd + properties.ks + properties.kt)

        V = VP-SP
        V = V/np.linalg.norm(V)

        if rand < properties.kd:                  
            direction = sampling_up_hemisphere(V, SN)
            att = properties.kd
                
        elif rand < properties.kd + properties.ks:     
            for light in self.lights:
                light_point = light.get_point()
                L = light_point - SP
                L = L/np.linalg.norm(L)
                R = 2*SN*np.dot(SN, L) - L
                R = R/np.linalg.norm(R)
                direction = R
            att = properties.ks

        else:
            # method expect the view vector pointing towards the surface...                    
            direction = snell_law(-V, SN)
            att = properties.kt

        return Ray(SP, direction), att
