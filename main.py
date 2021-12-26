from pathlib import Path
from readers.sdl import SDLReader
from readers.obj import OBJReader
from scene.camera import Camera
from scene.object import Properties, Triangles, SceneObject


PATH = Path('./cornellroom/')
SDL_FILE = PATH / 'cornellroom.sdl'

if __name__ == "__main__":
    # ## Load Scene
    # Read Scene
    sdl = SDLReader()
    sdl.read(SDL_FILE)
    # Initialize Cam
    camera = Camera(
        eye=sdl.eye, target=sdl.target, up=sdl.up, window_size=sdl.window_size, pixels_size=sdl.size
    )
    # Load Objects
    objects = []
    obj_reader = OBJReader()
    for obj_file_name, obj_props in sdl.objects:
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

    # Load Light

    # ## Path tracing
    # TODO