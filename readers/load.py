from pathlib import Path

import numpy as np
from readers.sdl import SDLReader
from readers.obj import OBJReader
from scene.camera import Camera
from scene.objects import Light, Properties, SceneObject
from scene.triangles import Triangles

PATH = Path('./cornellroom/')
SDL_FILE = PATH / 'cornellroom.sdl'

class SceneLoader():

    def __init__(self):
        self.sdl = SDLReader()
        self.sdl.read(SDL_FILE)

    def get_objects(self):
        objects = []

        # objects
        for obj_file_name, obj_props in self.sdl.objects:
            # properties
            properties = Properties(
                color = obj_props[:3],
                ka = obj_props[3],
                kd = obj_props[4],
                ks = obj_props[5],
                kt = obj_props[6],
                n  = obj_props[7]
            )
            # object vertices/triangles
            obj = self.__get_object(obj_file_name, properties)
            objects.append(obj)

        # light object
        for obj_file_name, color, lp in self.sdl.lights:
            properties = Properties(color=np.array(color)*lp, is_light=True)
            obj_scene = self.__get_object(obj_file_name, properties=properties)
            objects.append(obj_scene)    

        return objects

    def get_camera(self):
        camera = Camera(
            eye=self.sdl.eye, 
            target=self.sdl.target, 
            up=self.sdl.up, 
            window_size=self.sdl.window_size, 
            pixels_size=self.sdl.size
        )
        return camera

    def get_size(self):
        return self.sdl.size[0], self.sdl.size[1]

    def get_light(self):
        lights = []
        for obj_file_name, color, lp in self.sdl.lights:
            objs = self.__get_object(obj_file_name)
            lights.append(
                Light(lp, color, objs)
            )
        return lights

    def get_tonemapping(self):
        return self.sdl.tonemapping

    def __get_object(self,obj_file_name, properties=None):
        vertices, faces = OBJReader().read(PATH / obj_file_name)
        triangles = []
        for face in faces:
            t = Triangles(
                    p1=vertices[face[0]], p2=vertices[face[1]], p3=vertices[face[2]]
                )
            triangles.append(t)
            # SceneObject
        obj = SceneObject(
                name=obj_file_name.split('.')[0],
                properties=properties,
                objects=triangles
            )
        
        return obj

    