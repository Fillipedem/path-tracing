import random
import numpy as np
from readers.load import SceneLoader
from scene.ray import Ray

def path_tracing(ray, scene_objects, lights):
    ray_intersection = trace_ray(ray, scene_objects)

    # get color + shadow ray
    if ray_intersection:
        scene_obj, point, normal = ray_intersection
        I = shading(ray, scene_obj, point, normal, lights)
        I = shadow_ray(scene_objects, lights, point, I)

        # send secundary rays        
        I = I + secundary_ray(point, normal, ray, scene_obj, scene_objects, lights)

        return np.clip(I, 0, 1)

def secundary_ray(point, normal, orig_ray, scene_obj, scene_objects, lights):
    Is = np.zeros(3)
    ktot = scene_obj.properties.kd + scene_obj.properties.ks + scene_obj.properties.kt
    rand = random.uniform(0, ktot)

    if rand < scene_obj.properties.kd:
        V = orig_ray.p-point
        V = V/np.linalg.norm(V)
        vec = get_difuse_vector(normal, V)
        ray = Ray(point, vec)
        ray_intersection = send_ray(scene_objects, lights, ray)
        if ray_intersection:
            I, _, _, _ = ray_intersection
            Is += I*scene_obj.properties.kd

    elif rand < scene_obj.properties.ks:
        for light in lights:
            L = light.point - point
            L = L/np.linalg.norm(L)
            R = 2*normal*np.dot(normal, L) - L
            R = R/np.linalg.norm(R)
    
            ray = Ray(point, R)
    
            ray_intersection = send_ray(scene_objects, lights, ray)
            if ray_intersection:
                I, _, _, _ = ray_intersection
                Is += I*scene_obj.properties.ks
    
    return Is

def get_difuse_vector(normal, V):
    e1, e2 = random.random(), random.random()
    a, b = np.arccos(np.sqrt(e1)), 2*np.pi*e2

    normal = normal/np.linalg.norm(normal)
    S = np.cross(normal, V)
    S = S/np.linalg.norm(S)
    V = np.cross(S, normal)
    V = V/np.linalg.norm(V)

    matrix = np.array([V, S, normal])

    new_vector = np.array((
        np.sin(a)*np.cos(b),
        np.sin(a)*np.sin(b),
        np.cos(a)
        )
    )

    return matrix.transpose()@new_vector


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

def send_ray(scene_objects, lights, ray):
    I = np.zeros(3)
    ray_intersection = trace_ray(ray, scene_objects)
            
    if ray_intersection:
        scene_obj, point, normal = ray_intersection
                
        I = shading(ray, scene_obj, point, normal, lights)
        I = shadow_ray(scene_objects, lights, point, I)

        return I, scene_obj, point, normal

def shadow_ray(scene_objects, lights, point, I):
    for light in lights:
        shadow_ray = Ray(point, light.point - point)
        distance = np.linalg.norm(light.point - point)
        shadow_intersection = trace_ray(shadow_ray, scene_objects)
        if shadow_intersection:
            _, p, _ = shadow_intersection
            if np.linalg.norm(p - point) < distance:
                I = I*0.5
    return I

def shading(ray, obj, point, normal, lights, only_ambient=False):
    I = obj.properties.color*obj.properties.ka*0.5

    if only_ambient:
        return I

    V = point - ray.p
    V = V/np.linalg.norm(V)
    
    for light in lights:
        L = light.point - point
        L = L/np.linalg.norm(L)
        R = 2*normal*np.dot(normal, L) - L
        R = R/np.linalg.norm(R)

        difusa = light.lp*light.color*obj.properties.color*obj.properties.kd*np.dot(L, normal)
        especular = light.lp*light.color*obj.properties.ks*(np.dot(R, V)**obj.properties.n)
        I += np.clip(difusa, 0, 1) + np.clip(especular, 0, 1)

    return I

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

    from matplotlib import pyplot as plt
    for i in range(10):
        for ray in rays:
            color = path_tracing(ray, scene_objects, lights)
            if color is not None:
                img[ray.pixel[1], ray.pixel[0]] += color

        
        print(f"{i}")
        plt.imshow(img/(i + 1), interpolation='nearest')
        