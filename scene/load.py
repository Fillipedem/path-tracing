from pathlib import Path
from readers.sdl import SDLReader
from readers.obj import OBJReader
from scene.camera import Camera
from scene.objects import Properties, Triangles, SceneObject

PATH = Path('./cornellroom/')
SDL_FILE = PATH / 'cornellroom.sdl'

class SceneLoader():

    def __init__(self):
        self.sdl = SDLReader()
        self.sdl.read(SDL_FILE)

    def get_objects(self):
        objects = []
        obj_reader = OBJReader()
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
            vertices, faces = obj_reader.read(PATH / obj_file_name)
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
            objects.append(obj)
        
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