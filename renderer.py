
from mesh import Mesh
from matrix import Matrix4, Vector3, Vector4
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

    def draw(
    self,
    mesh: Mesh,
    model: Matrix4,
    camera: Camera,
) -> None:
        view = camera.get_view_matrix()
        projection = camera.get_projection_matrix()

        mvp = projection @ view @ model

        world_vertices: list[Vector3] = []
        projected_vertices: list[tuple[int, int]] = []

        # Трансформируем вершины
        for vertex in mesh.vertices:
            world = model @ vertex.to_vector4()
            world_vertices.append(world.xyz())

            clip = mvp @ vertex.to_vector4()
            ndc = clip.perspective_divide()
            projected_vertices.append(self.to_screen(ndc))

        for i0, i1, i2 in mesh.faces:
            v0 = world_vertices[i0]
            v1 = world_vertices[i1]
            v2 = world_vertices[i2]

            edge1 = v1 - v0
            edge2 = v2 - v0

            normal = edge1.cross(edge2).normalized()

            to_camera = (camera.position - v0).normalized()

            # Back-face culling
            if normal.dot(to_camera) > 0:
                continue

            x1, y1 = projected_vertices[i0]
            x2, y2 = projected_vertices[i1]
            x3, y3 = projected_vertices[i2]

            self.draw_triangle(x1, y1, x2, y2, x3, y3)

                        
    def draw_point(self, x: int, y: int, point_char: str = "*") -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.screen[y][x] = point_char
    @staticmethod
    def edge_function(x:int, y:int, x1: int, y1: int, x2: int, y2: int) -> int:
        return (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        

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
    
    def draw_triangle(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        x3: int,
        y3: int,
    ) -> None:
        self.draw_line(x1, y1, x2, y2)
        self.draw_line(x2, y2, x3, y3)
        self.draw_line(x3, y3, x1, y1)
        for x in range(len(self.screen[0])):
            for y in range(len(self.screen)):
                if self.edge_function(x, y, x1, y1, x2, y2) > 0 and self.edge_function(x, y, x2, y2, x3, y3) > 0 and self.edge_function(x, y, x3, y3, x1, y1) > 0:
                    self.draw_point(x, y, '.')

    def to_screen(
        self,
        vertex: Vector4,
    ) -> tuple[int, int]:
        x, y = vertex.x, vertex.y
        screen_x = (x + 1) * (self.width - 1) / 2
        screen_y = (1 - y) * (self.height - 1) / 2

        return round(screen_x), round(screen_y)

    def present(self) -> None:
        command = "cls" if os.name == "nt" else "clear"
        os.system(command)
        for row in self.screen:
            print(''.join(row))