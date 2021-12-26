import numpy as np
from scene.load import SceneLoader

if __name__ == "__main__":
    # ## Load Scene
    scene = SceneLoader()
    # Initialize Cam
    camera = scene.get_camera()
    # Load Objects
    scene_objects = scene.get_objects()
    # Load Light
    # light_object = scene.get_light()

    # "RAY CASTING" #
    rays = camera.get_rays()
    w, h = scene.get_size()
    img = np.zeros((w, h, 3))
    for ray in rays:
        min_d = np.inf
        for scene_obj in scene_objects:
            for obj in scene_obj.objects:
                point = obj.intersect(ray)
                if point is not None:
                    distance = np.linalg.norm(ray.p - point)
                    if distance < min_d:
                        img[ray.pixel[1], ray.pixel[0]] = scene_obj.properties.color

    from matplotlib import pyplot as plt

    plt.imshow(img, interpolation='nearest')
    plt.show()