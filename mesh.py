from matrix import Vector4


class Mesh:
    def __init__(
        self,
        vertices: list[Vector4],
        edges: list[tuple[int, int]],
    ) -> None:
        self.vertices = vertices
        self.edges = edges

    @staticmethod
    def cube(
        size: float = 1.0,
    ) -> "Mesh":
        return Mesh([
            Vector4(-size, size, size),
            Vector4(-size, -size, size),
            Vector4(size, -size, size),
            Vector4(size, size, size),
            Vector4(-size, size, -size),
            Vector4(-size, -size, -size),
            Vector4(size, -size, -size),
            Vector4(size, size, -size)
        ],
            [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ])

    @staticmethod
    def pyramid(
        size: float = 1.0,
    ) -> "Mesh":
        return Mesh([
            Vector4(-size,-size,-size),
            Vector4(size,-size,-size),
            Vector4(size,-size,size),
            Vector4(-size,-size,size),
            Vector4(0,size,0),
        ],
        [    
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4)
        ])