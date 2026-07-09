from mesh import Mesh
from matrix import Matrix4, Vector4
from camera import Camera
import os

class Renderer:
    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:
        self.width = width
        self.height = height
        self.screen = [[' '] * self.width for _ in range(self.height)]

    def clear(self):
        self.screen = [[' '] * self.width for _ in range(self.height)]
        return os.system("clear")

    def draw(
        self,
        mesh: Mesh,
        model: Matrix4,
        camera: Camera,
    ) -> None:
        mvp = camera.get_projection_matrix() @ camera.get_view_matrix() @ model
        projected = []
        for vertex in mesh.vertices:
            clip = mvp @ vertex
            ndc = clip.perspective_divide()
            screen = self.to_screen(ndc)
            projected.append(screen)
        for edge in mesh.edges:
            st, en = edge
            x1, y1 = projected[st]
            x2, y2 = projected[en]
            self.draw_line(x1,y1,x2,y2)


    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> None:
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        err = dx - dy

        while True:
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                self.screen[y1][x1] = "*"

            if x1 == x2 and y1 == y2:
                break

            e2 = err * 2

            if e2 > -dy:
                err -= dy
                x1 += sx

            if e2 < dx:
                err += dx
                y1 += sy

    def to_screen(
        self,
        vertex: Vector4,
    ) -> tuple[int, int]:
        x, y = vertex.x, vertex.y
        screen_x = (x + 1) / 2 * self.width
        screen_y = (-y + 1) / 2 * self.height

        return round(screen_x), round(screen_y)

    def present(self) -> None:
        for row in self.screen:
            print(''.join(row))