
from matrix import Vector3


class Mesh:
    def __init__(
        self,
        vertices: list[Vector3],
        faces: list[tuple[int, int, int]],
    ) -> None:
        self.vertices = vertices
        self.faces = faces

    @staticmethod
    def cube(
        size: float = 1.0,
    ) -> "Mesh":
        return Mesh([
            Vector3(-size, size, size),
            Vector3(-size, -size, size),
            Vector3(size, -size, size),
            Vector3(size, size, size),
            Vector3(-size, size, -size),
            Vector3(-size, -size, -size),
            Vector3(size, -size, -size),
            Vector3(size, size, -size)
        ],
            faces = [
    # Передняя (+Z)
    (0, 2, 1),
    (0, 3, 2),

    # Задняя (-Z)
    (4, 5, 6),
    (4, 6, 7),

    # Левая (-X)
    (4, 1, 5),
    (4, 0, 1),

    # Правая (+X)
    (3, 6, 2),
    (3, 7, 6),

    # Верхняя (+Y)
    (4, 3, 0),
    (4, 7, 3),

    # Нижняя (-Y)
    (1, 2, 6),
    (1, 6, 5),
])

    @staticmethod
    def pyramid(
        size: float = 1.0,
    ) -> "Mesh":
        return Mesh([
            Vector3(-size, -size, -size),
            Vector3(size, -size, -size),
            Vector3(size, -size, size),
            Vector3(-size, -size, size),
            Vector3(0, size, 0),
        ],
        [
            (0, 1, 2), (0, 2, 3),
            (0, 1, 4), (1, 2, 4),
            (2, 3, 4), (3, 0, 4)
        ])