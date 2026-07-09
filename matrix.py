from math import cos, sin, tan


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, i):
        return (self.x, self.y, self.z)[i]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

class Vector4:
    def __init__(self, x: float, y: float, z: float, w: float = 1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def perspective_divide(self):
        if self.w == 0:
            raise ZeroDivisionError()

        return Vector4(self.x / self.w, self.y / self.w, self.z / self.w, 1.0)

    def __getitem__(self, i):
        return (self.x, self.y, self.z, self.w)[i]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
        yield self.w


class Matrix4:
    def __init__(self, values: list[list[float]]):
        if len(values) != 4 or any(len(row) != 4 for row in values):
            raise ValueError("Matrix4 must be 4x4")
        self.matrix = values

    @staticmethod
    def identity() -> "Matrix4":
        return Matrix4(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    @staticmethod
    def rotation_x(angle: float) -> "Matrix4":
        rot_x_matrix = Matrix4(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, cos(angle), -1 * sin(angle), 0.0],
                [0.0, sin(angle), cos(angle), 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

        return rot_x_matrix

    @staticmethod
    def rotation_y(angle: float) -> "Matrix4":
        return Matrix4(
            [
                [cos(angle), 0.0, sin(angle), 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [-1 * sin(angle), 0.0, cos(angle), 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    @staticmethod
    def rotation_z(angle: float) -> "Matrix4":
        return Matrix4(
            [
                [cos(angle), -sin(angle), 0.0, 0.0],
                [sin(angle), cos(angle), 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    @staticmethod
    def translation(x: float, y: float, z: float) -> "Matrix4":
        return Matrix4(
            [
                [1.0, 0.0, 0.0, x],
                [0.0, 1.0, 0.0, y],
                [0.0, 0.0, 1.0, z],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    @staticmethod
    def scale(x: float, y: float, z: float) -> "Matrix4":
        return Matrix4(
            [
                [x, 0.0, 0.0, 0.0],
                [0.0, y, 0.0, 0.0],
                [0.0, 0.0, z, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    @staticmethod
    def uniform_scale(scale: float) -> "Matrix4":
        return Matrix4(
            [
                [scale, 0.0, 0.0, 0.0],
                [0.0, scale, 0.0, 0.0],
                [0.0, 0.0, scale, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

    @staticmethod
    def perspective(fov: float, aspect: float, near: float, far: float) -> "Matrix4":
        return Matrix4(
            [
                [1 / (aspect * tan(fov / 2)), 0.0, 0.0, 0.0],
                [0.0, 1 / (tan(fov / 2)), 0.0, 0.0],
                [
                    0.0,
                    0.0,
                    -((far + near) / (far - near)),
                    -((2 * far * near) / (far - near)),
                ],
                [0.0, 0.0, -1.0, 0.0],
            ]
        )

    def transpose(self) -> "Matrix4":
        return Matrix4([[self.matrix[j][i] for j in range(4)] for i in range(4)])

    def inverse(self) -> "Matrix4":
        """
        TODO:
            РАЗОБРАТЬСЯ САМОМУ БЫ
        """
        m = [val for row in self.matrix for val in row]
        inv = [0.0] * 16

        inv[0] = (
            m[5] * m[10] * m[15]
            - m[5] * m[11] * m[14]
            - m[9] * m[6] * m[15]
            + m[9] * m[7] * m[14]
            + m[13] * m[6] * m[11]
            - m[13] * m[7] * m[10]
        )
        inv[4] = (
            -m[4] * m[10] * m[15]
            + m[4] * m[11] * m[14]
            + m[8] * m[6] * m[15]
            - m[8] * m[7] * m[14]
            - m[12] * m[6] * m[11]
            + m[12] * m[7] * m[10]
        )
        inv[8] = (
            m[4] * m[9] * m[15]
            - m[4] * m[11] * m[13]
            - m[8] * m[5] * m[15]
            + m[8] * m[7] * m[13]
            + m[12] * m[5] * m[11]
            - m[12] * m[7] * m[9]
        )
        inv[12] = (
            -m[4] * m[9] * m[14]
            + m[4] * m[10] * m[13]
            + m[8] * m[5] * m[14]
            - m[8] * m[6] * m[13]
            - m[12] * m[5] * m[10]
            + m[12] * m[6] * m[9]
        )

        inv[1] = (
            -m[1] * m[10] * m[15]
            + m[1] * m[11] * m[14]
            + m[9] * m[2] * m[15]
            - m[9] * m[3] * m[14]
            - m[13] * m[2] * m[11]
            + m[13] * m[3] * m[10]
        )
        inv[5] = (
            m[0] * m[10] * m[15]
            - m[0] * m[11] * m[14]
            - m[8] * m[2] * m[15]
            + m[8] * m[3] * m[14]
            + m[12] * m[2] * m[11]
            - m[12] * m[3] * m[10]
        )
        inv[9] = (
            -m[0] * m[9] * m[15]
            + m[0] * m[11] * m[13]
            + m[8] * m[1] * m[15]
            - m[8] * m[3] * m[13]
            - m[12] * m[1] * m[11]
            + m[12] * m[3] * m[9]
        )
        inv[13] = (
            m[0] * m[9] * m[14]
            - m[0] * m[10] * m[13]
            - m[8] * m[1] * m[14]
            + m[8] * m[2] * m[13]
            + m[12] * m[1] * m[10]
            - m[12] * m[2] * m[9]
        )

        inv[2] = (
            m[1] * m[6] * m[15]
            - m[1] * m[7] * m[14]
            - m[5] * m[2] * m[15]
            + m[5] * m[3] * m[14]
            + m[13] * m[2] * m[7]
            - m[13] * m[3] * m[6]
        )
        inv[6] = (
            -m[0] * m[6] * m[15]
            + m[0] * m[7] * m[14]
            + m[4] * m[2] * m[15]
            - m[4] * m[3] * m[14]
            - m[12] * m[2] * m[7]
            + m[12] * m[3] * m[6]
        )
        inv[10] = (
            m[0] * m[5] * m[15]
            - m[0] * m[7] * m[13]
            - m[4] * m[1] * m[15]
            + m[4] * m[3] * m[13]
            + m[12] * m[1] * m[7]
            - m[12] * m[3] * m[5]
        )
        inv[14] = (
            -m[0] * m[5] * m[14]
            + m[0] * m[6] * m[13]
            + m[4] * m[1] * m[14]
            - m[4] * m[2] * m[13]
            - m[12] * m[1] * m[6]
            + m[12] * m[2] * m[5]
        )

        inv[3] = (
            -m[1] * m[6] * m[11]
            + m[1] * m[7] * m[10]
            + m[5] * m[2] * m[11]
            - m[5] * m[3] * m[10]
            - m[9] * m[2] * m[7]
            + m[9] * m[3] * m[6]
        )
        inv[7] = (
            m[0] * m[6] * m[11]
            - m[0] * m[7] * m[10]
            - m[4] * m[2] * m[11]
            + m[4] * m[3] * m[10]
            + m[8] * m[2] * m[7]
            - m[8] * m[3] * m[6]
        )
        inv[11] = (
            -m[0] * m[5] * m[11]
            + m[0] * m[7] * m[9]
            + m[4] * m[1] * m[11]
            - m[4] * m[3] * m[9]
            - m[8] * m[1] * m[7]
            + m[8] * m[3] * m[5]
        )
        inv[15] = (
            m[0] * m[5] * m[10]
            - m[0] * m[6] * m[9]
            - m[4] * m[1] * m[10]
            + m[4] * m[2] * m[9]
            + m[8] * m[1] * m[6]
            - m[8] * m[2] * m[5]
        )

        det = m[0] * inv[0] + m[1] * inv[4] + m[2] * inv[8] + m[3] * inv[12]

        if det == 0.0:
            raise ValueError("det = 0, matrix is uninverseble")

        inv_det = 1.0 / det
        for i in range(16):
            inv[i] *= inv_det

        return Matrix4([inv[i : i + 4] for i in range(0, 16, 4)])

    def __matmul__(self, other: "Matrix4 | Vector4"):
        if isinstance(other, Vector4):
            C = [0.0, 0.0, 0.0, 0.0]
            for i in range(4):
                for j in range(4):
                    C[i] += self.matrix[i][j] * other[j]
            return Vector4(C[0], C[1], C[2], C[3])
        elif isinstance(other, Matrix4):
            C = [[0.0] * 4 for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        C[i][j] += self.matrix[i][k] * other.matrix[k][j]
            return Matrix4(C)
