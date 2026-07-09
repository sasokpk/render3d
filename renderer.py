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
        try:
            view = camera.get_view_matrix()
            projection = camera.get_projection_matrix()
            projected_vertices = []
            view_vertices = []
            for vertex in mesh.vertices:
                world4 = model @ vertex
                view4 = view @ world4
                view_vertices.append(Vector3(view4.x, view4.y, view4.z))
                clip = projection @ view4
                ndc = clip.perspective_divide()
                projected_vertices.append(self.to_screen(ndc))
            for face in mesh.faces:
                try:
                    A = view_vertices[face[0]]
                    B = view_vertices[face[1]]
                    C = view_vertices[face[2]]
                except Exception:
                    print(f"Error accessing face indices: {face}")
                    return
                AB = B - A
                AC = C - A
                normal = Vector3(
                    AB.y * AC.z - AB.z * AC.y,
                    AB.z * AC.x - AB.x * AC.z,
                    AB.x * AC.y - AB.y * AC.x,
                )
                normal.normalize()
                x1, y1 = projected_vertices[face[0]]
                x2, y2 = projected_vertices[face[1]]
                x3, y3 = projected_vertices[face[2]]
                self.draw_line(x1, y1, x2, y2)
                self.draw_line(x2, y2, x3, y3)
                self.draw_line(x3, y3, x1, y1)
        except Exception:
            print("Exception in Renderer.draw")
            return


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
        screen_x = (x + 1) * (self.width - 1) / 2
        screen_y = (1 - y) * (self.height - 1) / 2

        return round(screen_x), round(screen_y)

    def present(self) -> None:
        os.system("clear")
        for row in self.screen:
            print(''.join(row))