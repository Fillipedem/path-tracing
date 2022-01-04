import cv2

import pyglet
from pyglet import app 
from pyglet.window import Window

import random
from threading import Thread, Lock

import numpy as np
from readers.load import SceneLoader
from render import PathTracing

FRAMERATE = 1
THREADS = 1

def parallel(camera, scene_objects, lights, rays, img_buffer, img_count, update_lock, npaths=10):
    count = 0
    pt = PathTracing(camera, scene_objects, lights)
    random.shuffle(rays)
    for _ in range(npaths):
        for ray in rays:
            with update_lock:
                pass
            color = pt.path_tracing(ray)
            if color is not None:
                img_buffer[ray.pixel[0], ray.pixel[1]] += color
                img_count[ray.pixel[0], ray.pixel[1]] += 1
    
if __name__ == "__main__":
    print("Starting")
    scene = SceneLoader()
    camera = scene.get_camera()
    scene_objects = scene.get_objects()
    lights = scene.get_light()

    # Path Tracing...
    rays = camera.get_rays()
    w, h = scene.get_size()

    update_lock = Lock()
    img_buffer = np.zeros((w, h, 3))
    img_count = np.zeros((w, h, 3))

    print("Starting PT..")
    rays_list = []
    for i in range(THREADS):
        split = len(rays)//THREADS
        if i - 1 == THREADS:
            rays_list.append(rays[i*split:])
        else:
            rays_list.append(rays[i*split: i*split + split])

    # Start Path Tracining
    threads = []
    for i in range(THREADS):
        th = Thread(
            target = parallel, args = (scene.get_camera(), scene.get_objects(), scene.get_light(), rays_list[i], img_buffer, img_count, update_lock, 10)
        )
        threads.append(th)
    
    # Pyglet
    print("Initialize window")
    win = Window(width=w, height=h)

    @win.event
    def on_draw():
        with update_lock:
            rescaled_image = (img_buffer/(img_count + 1) * 255).astype('int')
            win.clear()
            for i in range(w):
                for j in range(h):
                    color = rescaled_image[(i), (h - j - 1)]
                    pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
                        ('v2i', (i, j)),
                        ('c3B', (color[0], color[1], color[2]))
                )
    pyglet.clock.schedule_interval(lambda dt: None, FRAMERATE) 

    for th in threads:
        th.start()

    app.run()
