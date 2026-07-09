"""
Math primitives: vectors and 4×4 matrices used by the renderer.

Математические примитивы: векторы и матрицы 4×4, используемые рендерером.
"""

from math import cos, isclose, sin, tan


class Vector3:
    """
    3-component float vector with the usual arithmetic operators.

    Трёхкомпонентный вектор с обычными арифметическими операторами.
    """

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
    ) -> None:
        """
        Store the x, y, z components.

        Сохраняет компоненты x, y, z.
        """
        self.x = x
        self.y = y
        self.z = z

    def length_squared(self) -> float:
        """
        Return the squared Euclidean length (faster than length()).

        Возвращает квадрат евклидовой длины (быстрее, чем length()).
        """
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def __getitem__(
        self,
        i: int,
    ) -> float:
        """
        Index by component: 0 → x, 1 → y, 2 → z.

        Доступ по индексу: 0 → x, 1 → y, 2 → z.
        """
        return (self.x, self.y, self.z)[i]

    def __iter__(self):
        """
        Iterate over (x, y, z) in order.

        Перебор (x, y, z) по порядку.
        """
        yield from (self.x, self.y, self.z)

    def __add__(
        self,
        other: "Vector3",
    ) -> "Vector3":
        """
        Component-wise addition: self + other.

        Покомпонентное сложение: self + other.
        """
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def copy(self) -> "Vector3":
        """
        Return an independent copy with the same components.

        Возвращает независимую копию с теми же компонентами.
        """
        return Vector3(self.x, self.y, self.z)

    def __sub__(
        self,
        other: "Vector3",
    ) -> "Vector3":
        """
        Component-wise subtraction: self − other.

        Покомпонентное вычитание: self − other.
        """
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(
        self,
        scalar: float,
    ) -> "Vector3":
        """
        Scalar multiplication: self * scalar.

        Умножение на скаляр: self * scalar.
        """
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    __rmul__ = __mul__

    def __truediv__(
        self,
        scalar: float,
    ) -> "Vector3":
        """
        Scalar division: self / scalar. Raises on zero.

        Деление на скаляр: self / scalar. Бросает исключение на ноль.
        """
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self) -> "Vector3":
        """
        Unary minus: -self.

        Унарный минус: -self.
        """
        return Vector3(-self.x, -self.y, -self.z)

    def dot(
        self,
        other: "Vector3",
    ) -> float:
        """
        Dot product of two 3D vectors.

        Скалярное произведение двух 3D-векторов.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(
        self,
        other: "Vector3",
    ) -> "Vector3":
        """
        Cross product of two 3D vectors.

        Векторное произведение двух 3D-векторов.
        """
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        """
        Euclidean length of the vector.

        Евклидова длина вектора.
        """
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Approximate equality using math.isclose on each component.

        Приблизительное равенство через math.isclose по каждой компоненте.
        """
        if not isinstance(other, Vector3):
            return False
        return (
            isclose(self.x, other.x)
            and isclose(self.y, other.y)
            and isclose(self.z, other.z)
        )

    def normalize(self) -> None:
        """
        Normalize the vector in place. Raises on a zero vector.

        Нормализует вектор на месте. Бросает исключение на нулевом векторе.
        """
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero vector")
        self.x /= length
        self.y /= length
        self.z /= length

    def normalized(self) -> "Vector3":
        """
        Return a unit-length copy of this vector. Raises on zero.

        Возвращает копию единичной длины. Бросает исключение на нулевом.
        """
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector3(self.x / length, self.y / length, self.z / length)

    def to_vector4(
        self,
        w: float = 1.0,
    ) -> "Vector4":
        """
        Promote to a homogeneous Vector4 with the given w.

        Приводит к однородному Vector4 с заданным w.
        """
        return Vector4(self.x, self.y, self.z, w)

    def __repr__(self) -> str:
        """
        Developer-friendly string form: Vector3(x, y, z).

        Удобная для отладки форма: Vector3(x, y, z).
        """
        return f"Vector3({self.x}, {self.y}, {self.z})"


class Vector4:
    """
    4-component homogeneous vector used during MVP transforms.

    Однородный 4-компонентный вектор, используемый в MVP-преобразованиях.
    """

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        w: float = 1.0,
    ) -> None:
        """
        Store the x, y, z, w components.

        Сохраняет компоненты x, y, z, w.
        """
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def perspective_divide(self) -> "Vector4":
        """
        Divide x, y, z by w to produce a normalized-device-coordinate vector.

        Делит x, y, z на w, получая вектор в нормализованных координатах устройства.
        """
        if self.w == 0:
            raise ZeroDivisionError("Cannot perform perspective divide with w=0")
        return Vector4(self.x / self.w, self.y / self.w, self.z / self.w, 1.0)

    def xyz(self) -> Vector3:
        """
        Drop w and return a Vector3.

        Отбрасывает w и возвращает Vector3.
        """
        return Vector3(self.x, self.y, self.z)

    def __getitem__(
        self,
        i: int,
    ) -> float:
        """
        Index by component: 0 → x, 1 → y, 2 → z, 3 → w.

        Доступ по индексу: 0 → x, 1 → y, 2 → z, 3 → w.
        """
        return (self.x, self.y, self.z, self.w)[i]

    def __iter__(self):
        """
        Iterate over (x, y, z, w) in order.

        Перебор (x, y, z, w) по порядку.
        """
        yield from (self.x, self.y, self.z, self.w)

    def copy(self) -> "Vector4":
        """
        Return an independent copy with the same components.

        Возвращает независимую копию с теми же компонентами.
        """
        return Vector4(self.x, self.y, self.z, self.w)

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Approximate equality using math.isclose on each component.

        Приблизительное равенство через math.isclose по каждой компоненте.
        """
        if not isinstance(other, Vector4):
            return False
        return (
            isclose(self.x, other.x)
            and isclose(self.y, other.y)
            and isclose(self.z, other.z)
            and isclose(self.w, other.w)
        )

    def __sub__(self, other: "Vector4") -> "Vector4":
        """
        Component-wise subtraction: self − other.

        Покомпонентное вычитание: self − other.
        """
        return Vector4(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w,
        )

    def __repr__(self) -> str:
        """
        Developer-friendly string form: Vector4(x, y, z, w).

        Удобная для отладки форма: Vector4(x, y, z, w).
        """
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"


class Matrix4:
    """
    Row-major 4×4 matrix and the factory methods that build them.

    Матрица 4×4 (построчно) и фабричные методы для её создания.
    """

    def __init__(self, values: list[list[float]]) -> None:
        """
        Wrap a 4×4 list of lists. Validates dimensions.

        Оборачивает список списков 4×4. Проверяет размерность.

        Args:
            values: A 4×4 matrix as nested lists / Матрица 4×4 в виде
                вложенных списков.
        """
        if len(values) != 4 or any(len(row) != 4 for row in values):
            raise ValueError("Matrix4 must be 4x4")
        self.matrix = values

    @staticmethod
    def identity() -> "Matrix4":
        """
        Return the identity matrix.

        Возвращает единичную матрицу.
        """
        return Matrix4([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    @staticmethod
    def rotation_x(angle: float) -> "Matrix4":
        """
        Rotation around the X axis by `angle` radians.

        Вращение вокруг оси X на `angle` радиан.
        """
        return Matrix4([
            [1.0,       0.0,        0.0, 0.0],
            [0.0,  cos(angle), -sin(angle), 0.0],
            [0.0,  sin(angle),  cos(angle), 0.0],
            [0.0,       0.0,        0.0, 1.0],
        ])

    @staticmethod
    def rotation_y(angle: float) -> "Matrix4":
        """
        Rotation around the Y axis by `angle` radians.

        Вращение вокруг оси Y на `angle` радиан.
        """
        return Matrix4([
            [ cos(angle), 0.0, sin(angle), 0.0],
            [      0.0,   1.0,      0.0,   0.0],
            [-sin(angle), 0.0, cos(angle), 0.0],
            [      0.0,   0.0,      0.0,   1.0],
        ])

    @staticmethod
    def rotation_z(angle: float) -> "Matrix4":
        """
        Rotation around the Z axis by `angle` radians.

        Вращение вокруг оси Z на `angle` радиан.
        """
        return Matrix4([
            [cos(angle), -sin(angle), 0.0, 0.0],
            [sin(angle),  cos(angle), 0.0, 0.0],
            [     0.0,        0.0,    1.0, 0.0],
            [     0.0,        0.0,    0.0, 1.0],
        ])

    @staticmethod
    def translation(x: float, y: float, z: float) -> "Matrix4":
        """
        Translation by (x, y, z).

        Перенос на (x, y, z).
        """
        return Matrix4([
            [1.0, 0.0, 0.0,    x],
            [0.0, 1.0, 0.0,    y],
            [0.0, 0.0, 1.0,    z],
            [0.0, 0.0, 0.0, 1.0],
        ])

    @staticmethod
    def scale(x: float, y: float, z: float) -> "Matrix4":
        """
        Non-uniform scale by (x, y, z).

        Неравномерное масштабирование по (x, y, z).
        """
        return Matrix4([
            [  x, 0.0, 0.0, 0.0],
            [0.0,   y, 0.0, 0.0],
            [0.0, 0.0,   z, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])

    @staticmethod
    def uniform_scale(scale: float) -> "Matrix4":
        """
        Uniform scale by a single factor.

        Равномерное масштабирование с одним коэффициентом.
        """
        return Matrix4([
            [scale, 0.0,   0.0,   0.0],
            [  0.0, scale, 0.0,   0.0],
            [  0.0, 0.0,   scale, 0.0],
            [  0.0, 0.0,   0.0,   1.0],
        ])

    @staticmethod
    def look_at(eye: Vector3, target: Vector3, up: Vector3) -> "Matrix4":
        """
        Build a right-handed view matrix.

        Создаёт правостороннюю view matrix. Камера смотрит из `eye` в `target`.
        """
        forward = (target - eye).normalized()
        right = forward.cross(up).normalized()
        true_up = right.cross(forward)

        return Matrix4([
            [right.x,       right.y,       right.z,       -right.dot(eye)],
            [true_up.x,     true_up.y,     true_up.z,     -true_up.dot(eye)],
            [-forward.x,   -forward.y,    -forward.z,     forward.dot(eye)],
            [0.0,           0.0,           0.0,            1.0],
        ])

    @staticmethod
    def perspective(fov: float, aspect: float, near: float, far: float) -> "Matrix4":
        """
        Standard right-handed perspective projection matrix.

        Стандартная правосторонняя матрица перспективной проекции.

        Args:
            fov: Vertical field of view in radians / Вертикальный
                угол обзора в радианах.
            aspect: Viewport width / height / Соотношение сторон
                окна (ширина / высота).
            near: Near plane distance / Расстояние до ближней плоскости.
            far: Far plane distance / Расстояние до дальней плоскости.
        """
        return Matrix4([
            [1.0 / (aspect * tan(fov / 2)), 0.0,                   0.0,                          0.0],
            [                            0.0, 1.0 / tan(fov / 2),  0.0,                          0.0],
            [                            0.0, 0.0, -(far + near) / (far - near), -2 * far * near / (far - near)],
            [                            0.0, 0.0,                -1.0,                          0.0],
        ])

    def transpose(self) -> "Matrix4":
        """
        Return the transposed matrix.

        Возвращает транспонированную матрицу.
        """
        return Matrix4([[self.matrix[j][i] for j in range(4)] for i in range(4)])

    def inverse(self) -> "Matrix4":
        """
        Return the inverse matrix using the cofactor expansion.

        Возвращает обратную матрицу через разложение по кофакторам.

        Raises:
            ValueError: If the determinant is zero (singular matrix).
                Если определитель равен нулю (вырожденная матрица).
        """
        m = [val for row in self.matrix for val in row]
        inv = [0.0] * 16

        # Compute cofactors for each output cell.
        # Вычисляем кофакторы для каждой ячейки результата.
        inv[0] = (
            m[5]  * m[10] * m[15] - m[5]  * m[11] * m[14]
            - m[9] * m[6]  * m[15] + m[9] * m[7]  * m[14]
            + m[13] * m[6] * m[11] - m[13] * m[7] * m[10]
        )
        inv[4] = (
            -m[4]  * m[10] * m[15] + m[4]  * m[11] * m[14]
            + m[8]  * m[6]  * m[15] - m[8]  * m[7]  * m[14]
            - m[12] * m[6]  * m[11] + m[12] * m[7]  * m[10]
        )
        inv[8] = (
            m[4]  * m[9] * m[15] - m[4]  * m[11] * m[13]
            - m[8] * m[5] * m[15] + m[8]  * m[7]  * m[13]
            + m[12] * m[5] * m[11] - m[12] * m[7] * m[9]
        )
        inv[12] = (
            -m[4]  * m[9] * m[14] + m[4]  * m[10] * m[13]
            + m[8]  * m[5] * m[14] - m[8]  * m[6]  * m[13]
            - m[12] * m[5] * m[10] + m[12] * m[6] * m[9]
        )

        inv[1] = (
            -m[1]  * m[10] * m[15] + m[1]  * m[11] * m[14]
            + m[9]  * m[2]  * m[15] - m[9]  * m[3]  * m[14]
            - m[13] * m[2]  * m[11] + m[13] * m[3]  * m[10]
        )
        inv[5] = (
            m[0]  * m[10] * m[15] - m[0]  * m[11] * m[14]
            - m[8] * m[2]  * m[15] + m[8]  * m[3]  * m[14]
            + m[12] * m[2] * m[11] - m[12] * m[3] * m[10]
        )
        inv[9] = (
            -m[0]  * m[9] * m[15] + m[0]  * m[11] * m[13]
            + m[8]  * m[1] * m[15] - m[8]  * m[3]  * m[13]
            - m[12] * m[1] * m[11] + m[12] * m[3] * m[9]
        )
        inv[13] = (
            m[0]  * m[9] * m[14] - m[0]  * m[10] * m[13]
            - m[8] * m[1] * m[14] + m[8]  * m[2]  * m[13]
            + m[12] * m[1] * m[10] - m[12] * m[2] * m[9]
        )

        inv[2] = (
            m[1]  * m[6] * m[15] - m[1]  * m[7] * m[14]
            - m[5] * m[2] * m[15] + m[5]  * m[3] * m[14]
            + m[13] * m[2] * m[7] - m[13] * m[3] * m[6]
        )
        inv[6] = (
            -m[0]  * m[6] * m[15] + m[0]  * m[7] * m[14]
            + m[4]  * m[2] * m[15] - m[4]  * m[3] * m[14]
            - m[12] * m[2] * m[7]  + m[12] * m[3] * m[6]
        )
        inv[10] = (
            m[0]  * m[5] * m[15] - m[0]  * m[7] * m[13]
            - m[4] * m[1] * m[15] + m[4]  * m[3] * m[13]
            + m[12] * m[1] * m[7] - m[12] * m[3] * m[5]
        )
        inv[14] = (
            -m[0]  * m[5] * m[14] + m[0]  * m[6] * m[13]
            + m[4]  * m[1] * m[14] - m[4]  * m[2] * m[13]
            - m[12] * m[1] * m[6]  + m[12] * m[2] * m[5]
        )

        inv[3] = (
            -m[1] * m[6] * m[11] + m[1] * m[7] * m[10]
            + m[5] * m[2] * m[11] - m[5] * m[3] * m[10]
            - m[9] * m[2] * m[7]  + m[9] * m[3] * m[6]
        )
        inv[7] = (
            m[0] * m[6] * m[11] - m[0] * m[7] * m[10]
            - m[4] * m[2] * m[11] + m[4] * m[3] * m[10]
            + m[8] * m[2] * m[7]  - m[8] * m[3] * m[6]
        )
        inv[11] = (
            -m[0] * m[5] * m[11] + m[0] * m[7] * m[9]
            + m[4] * m[1] * m[11] - m[4] * m[3] * m[9]
            - m[8] * m[1] * m[7]  + m[8] * m[3] * m[5]
        )
        inv[15] = (
            m[0] * m[5] * m[10] - m[0] * m[6] * m[9]
            - m[4] * m[1] * m[10] + m[4] * m[2] * m[9]
            + m[8] * m[1] * m[6]  - m[8] * m[2] * m[5]
        )

        det = m[0] * inv[0] + m[1] * inv[4] + m[2] * inv[8] + m[3] * inv[12]

        if det == 0.0:
            raise ValueError("det = 0, matrix is not invertible")

        inv_det = 1.0 / det
        for i in range(16):
            inv[i] *= inv_det

        return Matrix4([inv[i:i + 4] for i in range(0, 16, 4)])

    def __matmul__(self, other: "Matrix4 | Vector4 | Vector3") -> "Matrix4 | Vector4":
        """
        Matrix multiplication. Also works on Vector4 and Vector3 (promoted).

        Умножение матриц. Также работает с Vector4 и Vector3 (с приведением).
        """
        if isinstance(other, Vector4):
            c = [0.0, 0.0, 0.0, 0.0]
            for i in range(4):
                for j in range(4):
                    c[i] += self.matrix[i][j] * other[j]
            return Vector4(c[0], c[1], c[2], c[3])

        if isinstance(other, Vector3):
            return self @ other.to_vector4()

        c = [[0.0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    c[i][j] += self.matrix[i][k] * other.matrix[k][j]
        return Matrix4(c)
