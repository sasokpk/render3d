"""Small RGB color helpers for the software framebuffer."""

from __future__ import annotations

from dataclasses import dataclass


def clamp(value: float, low: float, high: float) -> float:
    """Clamp value into the [low, high] range."""
    return max(low, min(high, value))


@dataclass(frozen=True, slots=True)
class Color:
    """8-bit RGB color."""

    r: int
    g: int
    b: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "r", int(clamp(self.r, 0, 255)))
        object.__setattr__(self, "g", int(clamp(self.g, 0, 255)))
        object.__setattr__(self, "b", int(clamp(self.b, 0, 255)))

    def scaled(self, intensity: float) -> "Color":
        """Return this color multiplied by intensity 0..1."""
        intensity = clamp(intensity, 0.0, 1.0)
        return Color(
            int(self.r * intensity),
            int(self.g * intensity),
            int(self.b * intensity),
        )

    def to_hex(self) -> str:
        """Return a Tk-compatible #rrggbb string."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"


BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
CUBE_BLUE = Color(90, 170, 255)


def shade_color(intensity: float, base: Color = CUBE_BLUE) -> Color:
    """Convert light intensity 0..1 into a shaded RGB color."""
    return base.scaled(intensity)
