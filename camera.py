from __future__ import annotations
from typing import Optional

try:
    from .matrix import Matrix4, Vector3
except ImportError:
    from matrix import Matrix4, Vector3


class Camera:
    def __init__(
        self,
        fov: float,
        aspect: float,
        near: float,
        far: float,
        position: Vector3 | None = None,
        rotation: Vector3 | None = None
    ) -> None:
        self.position = position or Vector3(0.0, 0.0, 0.0)
        self.rotation = rotation or Vector3(0.0, 0.0, 0.0)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

    def get_view_matrix(self) -> Matrix4:
        return(
            Matrix4.rotation_z(-self.rotation.z)
            @ Matrix4.rotation_y(-self.rotation.y)
            @ Matrix4.rotation_x(-self.rotation.x)
            @ Matrix4.translation(
                -self.position.x,
                -self.position.y,
                -self.position.z
            )
        )
    def get_projection_matrix(self) -> Matrix4:
        return Matrix4.perspective(
            self.fov,
            self.aspect,
            self.near,
            self.far,
        )