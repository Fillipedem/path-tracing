"""Simplem class represeting an intersection"""


class Intersection():

    def __init__(self, point, normal, obj_properties, orig_ray):
        self.point = point
        self.normal = normal
        self.obj_properties = obj_properties
        self.orig_ray = orig_ray