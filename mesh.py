from matrix import Vector4


class Mesh:
    def __init__(
        self,
        vertices: list[Vector4],
        faces: list[tuple[int, int, int]],
    ) -> None:
        self.vertices = vertices
        self.faces = faces

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
            (0, 1, 2), (0, 2, 3),
            (4, 5, 6), (4, 6, 7),
            (0, 1, 5), (0, 5, 4),
            (2, 3, 7), (2, 7, 6),
            (0, 3, 7), (0, 7, 4),
            (1, 2, 6), (1, 6, 5)
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
        (0, 1, 2), (0, 2, 3),
        (0, 1, 4), (1, 2, 4),
        (2, 3, 4), (3, 0, 4)
        ])