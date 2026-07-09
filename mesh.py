"""
Mesh — geometric primitives for the renderer.

Mesh — геометрические примитивы для рендерера.
"""

from matrix import Vector3


class Mesh:
    """
    A polygon mesh defined by a list of vertices and triangular faces.

    Полигональная сетка, заданная списком вершин и треугольных граней.

    Attributes:
        vertices (list[Vector3]): Mesh vertices / Вершины сетки.
        faces (list[tuple[int, int, int]]): Triangular faces as vertex
            indices / Треугольные грани как индексы вершин.
    """

    def __init__(
        self,
        vertices: list[Vector3],
        faces: list[tuple[int, int, int]],
    ) -> None:
        """
        Store vertices and faces that describe the mesh.

        Сохраняет вершины и грани, описывающие сетку.

        Args:
            vertices: Vertex positions / Позиции вершин.
            faces: Triangles as triples of vertex indices / Треугольники
                в виде троек индексов вершин.
        """
        self.vertices = vertices
        self.faces = faces

    @staticmethod
    def cube(
        size: float = 1.0,
    ) -> "Mesh":
        """
        Build a unit cube centered at the origin.

        Создаёт единичный куб с центром в начале координат.

        Face winding is counter-clockwise when viewed from outside,
        so back-face culling works correctly.

        Обход граней — против часовой стрелки при взгляде снаружи,
        поэтому отсечение нелицевых граней работает корректно.

        Args:
            size: Half-side of the cube / Половина длины ребра куба.

        Returns:
            A new Mesh shaped like a cube / Новая сетка в форме куба.
        """
        vertices = [
            # Front face (+Z) / Передняя грань (+Z)
            Vector3(-size,  size,  size),
            Vector3(-size, -size,  size),
            Vector3( size, -size,  size),
            Vector3( size,  size,  size),
            # Back face (-Z) / Задняя грань (-Z)
            Vector3(-size,  size, -size),
            Vector3(-size, -size, -size),
            Vector3( size, -size, -size),
            Vector3( size,  size, -size),
        ]
        faces = [
            # Front (+Z) / Передняя (+Z)
            (0, 2, 1), (0, 3, 2),
            # Back (-Z) / Задняя (-Z)
            (4, 5, 6), (4, 6, 7),
            # Left (-X) / Левая (-X)
            (4, 1, 5), (4, 0, 1),
            # Right (+X) / Правая (+X)
            (3, 6, 2), (3, 7, 6),
            # Top (+Y) / Верхняя (+Y)
            (4, 3, 0), (4, 7, 3),
            # Bottom (-Y) / Нижняя (-Y)
            (1, 2, 6), (1, 6, 5),
        ]
        return Mesh(vertices, faces)

    @staticmethod
    def pyramid(
        size: float = 1.0,
    ) -> "Mesh":
        """
        Build a square pyramid whose base lies on the XZ plane.

        Создаёт квадратную пирамиду с основанием в плоскости XZ.

        Args:
            size: Half-side of the base / Половина стороны основания.

        Returns:
            A new Mesh shaped like a pyramid / Новая сетка в форме пирамиды.
        """
        vertices = [
            Vector3(-size, -size, -size),
            Vector3( size, -size, -size),
            Vector3( size, -size,  size),
            Vector3(-size, -size,  size),
            Vector3(   0.0,   size,    0.0),
        ]
        faces = [
            (0, 1, 2), (0, 2, 3),  # Base / Основание
            (0, 1, 4), (1, 2, 4),  # Sides / Боковые грани
            (2, 3, 4), (3, 0, 4),
        ]
        return Mesh(vertices, faces)
