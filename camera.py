"""FPS-style camera used by the software renderer."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import cos, pi, sin, tau

from matrix import Matrix4, Vector3

WORLD_UP = Vector3(0.0, 1.0, 0.0)


@dataclass(slots=True)
class Camera:
    """A right-handed camera looking along -Z when yaw=pitch=0."""

    fov: float
    aspect: float
    near: float
    far: float
    position: Vector3 = field(default_factory=lambda: Vector3(0.0, 0.0, 0.0))
    rotation: Vector3 = field(default_factory=lambda: Vector3(0.0, 0.0, 0.0))

    def get_view_matrix(self) -> Matrix4:
        """Build the view matrix from the same basis used for movement."""
        return Matrix4.look_at(
            eye=self.position,
            target=self.position + self.forward(),
            up=WORLD_UP,
        )

    def get_projection_matrix(self) -> Matrix4:
        """Return the perspective projection matrix."""
        return Matrix4.perspective(self.fov, self.aspect, self.near, self.far)

    def forward(self) -> Vector3:
        """Return the world-space direction where the camera is looking."""
        pitch = self.rotation.x
        yaw = self.rotation.y

        return Vector3(
            -sin(yaw) * cos(pitch),
            sin(pitch),
            -cos(yaw) * cos(pitch),
        ).normalized()

    def right(self) -> Vector3:
        """Return camera-right in world space."""
        return self.forward().cross(WORLD_UP).normalized()

    def up(self) -> Vector3:
        """Return world-up. Good for classic FPS-style vertical movement."""
        return WORLD_UP

    def move_local(
        self,
        forward_amount: float,
        right_amount: float,
        up_amount: float,
    ) -> None:
        """Move relative to the camera orientation."""
        self.position = (
            self.position
            + self.forward() * forward_amount
            + self.right() * right_amount
            + self.up() * up_amount
        )

    def rotate(self, yaw_delta: float, pitch_delta: float) -> None:
        """Rotate by yaw/pitch deltas in radians."""
        self.rotation.y = (self.rotation.y + yaw_delta) % tau
        self.rotation.x += pitch_delta

        pitch_limit = pi / 2 - 0.01
        self.rotation.x = max(-pitch_limit, min(pitch_limit, self.rotation.x))
