from sdl import SDLReader
from camera import Camera


if __name__ == "__main__":
    # Read Scene
    scene = SDLReader()
    scene.read('./cornellroom/cornellroom.sdl')
    # Initialize Cam
    cam = Camera(
        eye=scene.eye, target=scene.target, up=scene.up, window_size=scene.window_size, pixels_size=scene.size
    )
    # Load Objects