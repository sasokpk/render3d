from math import cos, sin, tan, isclose


class Vector3:
    def __init__(
        self,
        x: float,
        y: float,
        z: float,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z

    def length_squared(self) -> float:
        return self.x**2 + self.y**2 + self.z**2

    def __getitem__(
        self,
        i: int,
    ) -> float:
        return (self.x, self.y, self.z)[i]

    def __iter__(
        self,
    ):
        yield from (self.x, self.y, self.z)

    def __add__(
        self,
        other: "Vector3",
    ) -> "Vector3":
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def copy(self):
        return Vector3(self.x, self.y, self.z)

    def __sub__(
        self,
        other: "Vector3",
    ) -> "Vector3":
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(
        self,
        scalar: float,
    ) -> "Vector3":
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(
        self,
        scalar: float,
    ) -> "Vector3":
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(
        self,
    ) -> "Vector3":
        return Vector3(-self.x, -self.y, -self.z)

    def dot(
        self,
        other: "Vector3",
    ) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(
        self,
        other: "Vector3",
    ) -> "Vector3":
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(
        self,
    ) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5
    def __eq__(
        self,
        other: object,
    ) -> bool:
        if not isinstance(other, Vector3):
            return False
        return (isclose(self.x, other.x) and isclose(self.y, other.y) and isclose(self.z, other.z))

    def normalize(
        self,
    ) -> None:
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero vector")
        self.x /= length
        self.y /= length
        self.z /= length

    def normalized(
        self,
    ) -> "Vector3":
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector3(self.x / length, self.y / length, self.z / length)

    def to_vector4(
        self,
        w: float = 1.0,
    ) -> "Vector4":
        return Vector4(self.x, self.y, self.z, w)

    def __repr__(
        self,
    ) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"

class Vector4:
    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        w: float = 1.0,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def perspective_divide(
        self,
    ) -> "Vector4":
        if self.w == 0:
            raise ZeroDivisionError("Cannot perform perspective divide with w=0")
        return Vector4(self.x / self.w, self.y / self.w, self.z / self.w, 1.0)

    def xyz(
        self,
    ) -> Vector3:
        return Vector3(self.x, self.y, self.z)

    def __getitem__(
        self,
        i: int,
    ) -> float:
        return (self.x, self.y, self.z, self.w)[i]

    def __iter__(
        self,
    ):
        yield from (self.x, self.y, self.z, self.w)
    
    def copy(self):
        return Vector4(self.x, self.y, self.z, self.w)

    def __eq__(
        self,
        other: object,
    ) -> bool:
        if not isinstance(other, Vector4):
            return False
        return (isclose(self.x, other.x) and isclose(self.y, other.y) and isclose(self.z, other.z) and isclose(self.w, other.w))

    def __sub__(self, other: Vector4):
        return Vector4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __repr__(
        self,
    ) -> str:
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"


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
