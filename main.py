from matplotlib.image import imsave
import numpy as np
from readers.load import SceneLoader
from render import PathTracing

if __name__ == "__main__":
    # ## Load Scene
    scene = SceneLoader()
    # Initialize Cam
    camera = scene.get_camera()
    # Load Objects
    scene_objects = scene.get_objects()
    # Load Light
    lights = scene.get_light()
    # light_object = scene.get_light()

    # Path Tracing...
    pt = PathTracing(camera, scene_objects, lights)
    rays = camera.get_rays()
    w, h = scene.get_size()
    img = np.zeros((w, h, 3))

    from matplotlib import pyplot as plt
    for i in range(100):
        for ray in rays:
            color = pt.path_tracing(ray)
            if color is not None:
                img[ray.pixel[1], ray.pixel[0]] += color

        kimg = img/(i + 1)
        kimg = kimg/(kimg + scene.get_tonemapping())
        imsave(f"images/pt_1_{i}.png", np.clip(kimg, 0, 1))
        imsave(f"images/pt_2_{i}.png", np.clip(img/(img + scene.get_tonemapping()), 0, 1))
