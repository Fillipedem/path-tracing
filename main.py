import numpy as np
from readers.load import SceneLoader

def get_color(ray, obj, point, normal, lights):  
    I = np.zeros(3)
    obj_color = obj.properties.color  
    V = point - ray.p
    V = V/np.linalg.norm(V)
    for l in lights:
        L = l.get_point() - point
        L = L/np.linalg.norm(L)

        R = 2*normal*np.dot(normal, L) - L

        ambiental = obj_color*obj.properties.ka
        difusa = l.color*obj_color*obj.properties.kd*np.dot(L, normal)
        especular = l.color*obj.properties.ks*(np.dot(R, V)**obj.properties.n)
        I += ambiental + difusa + especular

    return np.clip(I, 0, 1)

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
                        img[ray.pixel[1], ray.pixel[0]] = get_color(ray, scene_obj, point, obj.normal, lights)
                        min_d = distance

    from matplotlib import pyplot as plt

    plt.imshow(img, interpolation='nearest')
    plt.show()