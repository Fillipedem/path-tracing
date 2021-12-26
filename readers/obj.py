"""
Implement class to read a SDL(Scene Description Language)
"""
from readers.helper import read_lines, to_int, to_float

SPACE_REGEX = '[ ]+'

class OBJReader():

    def __init__(self):
        pass

    @classmethod
    def read(clf, obj_path: str):
        """read and instances objects from a obj file

        Args:
            obj_path (str): obj file path
        """
        # Read and load objects
        with open(obj_path, 'r') as file:
            f = file.read()

        vertices = []
        faces = []
        for line in read_lines(f):
            split = line.split(' ')
            command, data = split[0], split[1:]
            if command == 'v':
                vertices.append(to_float(data))
            elif command == 'f':
                data = [x - 1 for x in to_int(data)]
                faces.append(to_int(data))
            else:
                raise ValueError(f"Command not found {command}")

        return vertices, faces
