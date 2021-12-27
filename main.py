import threading
import numpy as np
from readers.load import SceneLoader
from scene.ray import Ray


def ray_casting(ray, scene_objects, lights):
    ray_intersection = trace_ray(ray, scene_objects)

    # get color + shadow ray
    if ray_intersection:
        scene_obj, point, normal = ray_intersection
        I = shading(ray, scene_obj, point, normal, lights)
        I = shadow_ray(scene_objects, lights, point, I)

        return np.clip(I, 0, 1)

def trace_ray(ray, scene_objects):
    min_d = np.inf
    intersection = None
    for scene_obj in scene_objects:
        for obj in scene_obj.objects:
            point = obj.intersect(ray)
            if point is not None:
                distance = np.linalg.norm(ray.p - point)
                if distance < min_d:
                    intersection = (scene_obj, point, obj.normal)
                    min_d = distance
    return intersection

def shadow_ray(scene_objects, lights, point, I):
    for light in lights:
        shadow_ray = Ray(point, light.point - point)
        distance = np.linalg.norm(light.point - point)
        shadow_intersection = trace_ray(shadow_ray, scene_objects)
        if shadow_intersection:
            _, p, _ = shadow_intersection
            if np.linalg.norm(p - point) < distance:
                I = I*0.9
    return I

def shading(ray, obj, point, normal, lights):  
    V = point - ray.p
    V = V/np.linalg.norm(V)
    
    I = obj.properties.color*obj.properties.ka # Ambiental
    for light in lights:
        L = light.point - point
        L = L/np.linalg.norm(L)
        R = 2*normal*np.dot(normal, L) - L
        R = R/np.linalg.norm(R)

        difusa = light.lp*light.color*obj.properties.color*obj.properties.kd*np.dot(L, normal)
        especular = light.lp*light.color*obj.properties.ks*(np.dot(R, V)**obj.properties.n)
        I += np.clip(difusa, 0, 1) + np.clip(especular, 0, 1)

    return I


def parallel(rays, scene_objects, lights, img):
    for ray in rays:
        color = ray_casting(ray, scene_objects, lights)
        if color is not None:
            img[ray.pixel[1], ray.pixel[0]] = color

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

    parallel(rays, scene_objects, lights, img)

    from matplotlib import pyplot as plt

    plt.imshow(img, interpolation='nearest')
    plt.show()