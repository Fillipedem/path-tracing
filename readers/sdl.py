"""
Implement class to read a SDL(Scene Description Language)
"""
from readers.helper import read_lines, to_int, to_float


class SDLReader():

    def __init__(self):
        self.lights = []
        self.objects = [] 

    def read(self, sdl_path: str):
        """read and parse sdl file

        Args:
            sdl_path (str): sdl file path
        """
        # read
        with open(sdl_path, 'r') as file:
            f = file.read()

        lines = read_lines(f)
        for line in lines:
            self.__process_command(line)
            
        self.__sanity_check()

    def __process_command(self, line: str):
        options = line.split(' ')
        command = options[0]

        if 'eye' == command:
            self.eye = to_float(options[1:])
        elif 'size'== command:
            self.size = to_int(options[1:])
        elif 'window_size' == command:
            self.window_size = to_float(options[1:])
        elif 'target' == command:
            self.target = to_float(options[1:])
        elif 'up' == command:
            self.up = to_float(options[1:])            
        elif 'background' == command:
            self.background = to_float(options[1:]) 
        elif 'ambient' == command:
            self.ambient = float(options[1])
        elif 'npaths' == command:
            self.npaths = int(options[1]) 
        elif 'tonemapping' == command:
            self.tonemapping = float(options[1])  
        elif 'seed' == command:
            self.seed = int(options[1])  
        elif 'object' == command:
            self.objects.append(
                (options[1], to_float(options[2:]))
            )
        elif 'light' == command:
            self.lights.append(
                (options[1], to_float(options[2:-1]), float(options[-1]))
            )
        elif 'output' == command:
            self.output = options[1]
        else:
            raise ValueError(f"Comando não encontrado: {command}!") 

    def __sanity_check(self):
        """Check for missing information after read sdl file...
        """
        # check attrs...
        attrs = ['eye', 'size', 'target', 'up', 'window_size', 'background', 'ambient']
        for attr in attrs:
            if not hasattr(self, attr):
                raise ValueError(f"Atributo {attr}, não repassado no arquivo SDL!")

        # check if objects exists...
        # TODO
