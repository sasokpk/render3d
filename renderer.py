"""Software renderer: mesh -> clip space -> rasterized framebuffers."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from math import isfinite

from camera import Camera
from framebuffer import BLACK, WHITE, Color, clamp, shade_color
from matrix import Matrix4, Vector3, Vector4
from mesh import Mesh


@dataclass(slots=True)
class RendererSettings:
    """Runtime switches for the tiny renderer."""

    backface_culling: bool = True
    wireframe: bool = False
    depth_debug: bool = False
    ambient: float = 0.15
    light_dir: Vector3 = field(
        default_factory=lambda: Vector3(0.0, 1.0, 1.0).normalized()
    )
    base_color: Color = shade_color(1.0)
    ascii_ramp: str = " .:-=+*#%@"


@dataclass(slots=True)
class RenderStats:
    """Tiny frame statistics. Handy when debugging the pipeline."""

    triangles_total: int = 0
    triangles_drawn: int = 0
    triangles_clipped: int = 0
    triangles_culled: int = 0
    pixels_drawn: int = 0


class Renderer:
    """Rasterizes triangles into both an ASCII buffer and an RGB buffer."""

    def __init__(
        self,
        width: int,
        height: int,
        settings: RendererSettings | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.settings = settings or RendererSettings()
        self.stats = RenderStats()

        self.screen: list[list[str]] = []
        self.color_buffer: list[list[Color]] = []
        self.z_buffer: list[list[float]] = []

        self.clear()

    def clear(self) -> None:
        """Reset color, ASCII, depth buffers and per-frame stats."""
        self.screen = [[" " for _ in range(self.width)] for _ in range(self.height)]
        self.color_buffer = [
            [BLACK for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.z_buffer = [
            [float("inf") for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.stats = RenderStats()

    def draw(self, mesh: Mesh, model: Matrix4, camera: Camera) -> None:
        """Transform, light, cull and rasterize a mesh."""
        view = camera.get_view_matrix()
        projection = camera.get_projection_matrix()
        mvp = projection @ view @ model

        world_vertices: list[Vector3] = []
        clip_vertices: list[Vector4] = []

        for vertex in mesh.vertices:
            local = vertex.to_vector4()
            world_vertices.append((model @ local).xyz())
            clip_vertices.append(mvp @ local)

        for i0, i1, i2 in mesh.faces:
            self.stats.triangles_total += 1

            c0 = clip_vertices[i0]
            c1 = clip_vertices[i1]
            c2 = clip_vertices[i2]

            if self.should_skip_triangle_clip(c0, c1, c2):
                self.stats.triangles_clipped += 1
                continue

            v0 = world_vertices[i0]
            v1 = world_vertices[i1]
            v2 = world_vertices[i2]

            normal = (v1 - v0).cross(v2 - v0).normalized()
            to_camera = (camera.position - v0).normalized()

            # This sign matches the current cube winding.
            front_facing = normal.dot(to_camera) <= 0.0
            if self.settings.backface_culling and not front_facing:
                self.stats.triangles_culled += 1
                continue

            intensity = self.lambert_intensity(normal)
            fill_char = self.shade_char(intensity)
            fill_color = shade_color(intensity, self.settings.base_color)

            p0 = self.to_screen(c0.perspective_divide())
            p1 = self.to_screen(c1.perspective_divide())
            p2 = self.to_screen(c2.perspective_divide())

            pixels = self.draw_triangle(
                *p0,
                *p1,
                *p2,
                fill_char=fill_char,
                fill_color=fill_color,
            )

            if pixels > 0:
                self.stats.triangles_drawn += 1
                self.stats.pixels_drawn += pixels

            if self.settings.wireframe:
                self.draw_wireframe(p0, p1, p2)

    def lambert_intensity(self, normal: Vector3) -> float:
        """Simple flat Lambert lighting with ambient fill."""
        diffuse = max(0.0, normal.dot(-self.settings.light_dir))
        ambient = clamp(self.settings.ambient, 0.0, 1.0)
        return ambient + diffuse * (1.0 - ambient)

    def shade_char(self, intensity: float) -> str:
        """Convert intensity 0..1 to an ASCII shade."""
        ramp = self.settings.ascii_ramp
        intensity = clamp(intensity, 0.0, 1.0)
        return ramp[int(intensity * (len(ramp) - 1))]

    @staticmethod
    def should_skip_triangle_clip(c0: Vector4, c1: Vector4, c2: Vector4) -> bool:
        """
        Conservative clip-space safety check.

        This is still not full clipping: triangles crossing near/far are skipped.
        The goal is to avoid perspective-dividing vertices with bad w.
        """
        clips = (c0, c1, c2)
        eps = 1e-5

        for c in clips:
            if not all(isfinite(value) for value in c):
                return True
            if c.w <= eps:
                return True

            # No real near/far clipping yet, so partial intersections are rejected.
            if c.z < -c.w or c.z > c.w:
                return True

        if all(c.x < -c.w for c in clips):
            return True
        if all(c.x > c.w for c in clips):
            return True
        if all(c.y < -c.w for c in clips):
            return True
        if all(c.y > c.w for c in clips):
            return True

        return False

    def draw_point(self, x: int, y: int, point_char: str, color: Color) -> None:
        """Plot one pixel into both framebuffers."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.screen[y][x] = point_char
            self.color_buffer[y][x] = color

    @staticmethod
    def edge_function(
        x0: int,
        y0: int,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> int:
        """Signed twice-area of triangle (p0, p1, p2)."""
        return (x2 - x1) * (y0 - y1) - (y2 - y1) * (x0 - x1)

    def draw_triangle(
        self,
        x1: int,
        y1: int,
        z1: float,
        x2: int,
        y2: int,
        z2: float,
        x3: int,
        y3: int,
        z3: float,
        fill_char: str,
        fill_color: Color,
    ) -> int:
        """Fill a triangle using barycentric coordinates and z-buffering."""
        min_x = max(0, min(x1, x2, x3))
        max_x = min(self.width - 1, max(x1, x2, x3))
        min_y = max(0, min(y1, y2, y3))
        max_y = min(self.height - 1, max(y1, y2, y3))

        if min_x > max_x or min_y > max_y:
            return 0

        area = self.edge_function(x1, y1, x2, y2, x3, y3)
        if area == 0:
            return 0

        pixels_drawn = 0

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                alpha = self.edge_function(x, y, x2, y2, x3, y3) / area
                beta = self.edge_function(x, y, x3, y3, x1, y1) / area
                gamma = self.edge_function(x, y, x1, y1, x2, y2) / area

                if not self.is_inside_triangle(alpha, beta, gamma):
                    continue

                z = alpha * z1 + beta * z2 + gamma * z3
                if z >= self.z_buffer[y][x]:
                    continue

                point_char = fill_char
                point_color = fill_color

                if self.settings.depth_debug:
                    # NDC depth is roughly -1 near, +1 far. Nearer should look brighter.
                    depth_t = clamp((z + 1.0) * 0.5, 0.0, 1.0)
                    depth_intensity = 1.0 - depth_t
                    point_char = self.shade_char(depth_intensity)
                    point_color = shade_color(depth_intensity, WHITE)

                self.z_buffer[y][x] = z
                self.draw_point(x, y, point_char, point_color)
                pixels_drawn += 1

        return pixels_drawn

    @staticmethod
    def is_inside_triangle(alpha: float, beta: float, gamma: float) -> bool:
        """Return True when barycentric coordinates are inside any winding."""
        return (alpha >= 0 and beta >= 0 and gamma >= 0) or (
            alpha <= 0 and beta <= 0 and gamma <= 0
        )

    def draw_wireframe(
        self,
        p0: tuple[int, int, float],
        p1: tuple[int, int, float],
        p2: tuple[int, int, float],
    ) -> None:
        """Draw a simple overlay wireframe without depth testing."""
        x0, y0, _ = p0
        x1, y1, _ = p1
        x2, y2, _ = p2
        self.draw_line(x0, y0, x1, y1, "@", WHITE)
        self.draw_line(x1, y1, x2, y2, "@", WHITE)
        self.draw_line(x2, y2, x0, y0, "@", WHITE)

    def draw_line(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        point_char: str = "*",
        color: Color = WHITE,
    ) -> None:
        """Draw a Bresenham line."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.draw_point(x1, y1, point_char, color)
            if x1 == x2 and y1 == y2:
                break

            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def to_screen(self, vertex: Vector4) -> tuple[int, int, float]:
        """Convert NDC coordinates to framebuffer pixel coordinates."""
        screen_x = (vertex.x + 1.0) * (self.width - 1) / 2.0
        screen_y = (1.0 - vertex.y) * (self.height - 1) / 2.0
        return round(screen_x), round(screen_y), vertex.z

    def present(self) -> None:
        """Clear the terminal and print the ASCII framebuffer."""
        os.system("cls" if os.name == "nt" else "clear")
        print("\n".join("".join(row) for row in self.screen))
