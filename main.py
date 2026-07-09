import math
import time

from camera import Camera
from matrix import Matrix4, Vector3
from mesh import Mesh
from renderer import Renderer

renderer = Renderer(
    width=220,
    height=70,
)

camera = Camera(
    fov=1.57,
    aspect=220 / 70,
    near=0.1,
    far=100.0,
    position=Vector3(0.0, 0.0, 8.0),
)

mesh = Mesh.cube()

angle = 0.0

while True:
    renderer.clear()

    scale = 3
    x = 2.0 * math.sin(angle)
    y = 1.0 * math.sin(angle * 0.7)

    model = (
        Matrix4.translation(x, y, 0.0)
        @ Matrix4.rotation_z(angle)
        @ Matrix4.rotation_y(angle)
        @ Matrix4.rotation_x(angle)
        @ Matrix4.uniform_scale(scale)

    )

    renderer.draw(
        mesh=mesh,
        model=model,
        camera=camera,
    )

    renderer.present()

    angle += 0.02
    time.sleep(0.016) 