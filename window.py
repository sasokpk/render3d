"""Tkinter window/input wrapper. Rendering still happens in our code."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable, Sequence

from framebuffer import Color


class Window:
    """A tiny Tk window with keyboard state, mouse-look and PhotoImage output."""

    def __init__(self, width: int, height: int, scale: int = 4) -> None:
        self.width = width
        self.height = height
        self.scale = max(1, scale)

        self.root = tk.Tk()
        self.root.title("My Tiny Software Renderer")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=self.width * self.scale,
            height=self.height * self.scale,
            bg="black",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.image = tk.PhotoImage(width=self.width, height=self.height)
        self.display_image = self.image
        self.canvas_image = self.canvas.create_image(
            0,
            0,
            image=self.display_image,
            anchor=tk.NW,
        )

        self.pressed_keys: set[str] = set()
        self.is_open = True

        self.mouse_look_enabled = False
        self.last_mouse_x: int | None = None
        self.last_mouse_y: int | None = None
        self.mouse_dx = 0.0
        self.mouse_dy = 0.0

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)
        self.root.bind("<FocusOut>", self._on_focus_out)

        self.canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)
        self.canvas.bind("<Motion>", self._on_mouse_motion)

        self.root.focus_force()
        self.canvas.focus_set()

    @staticmethod
    def _normalize_key(key: str) -> str:
        return key.lower()

    def _on_key_press(self, event) -> None:
        self.pressed_keys.add(self._normalize_key(event.keysym))

    def _on_key_release(self, event) -> None:
        self.pressed_keys.discard(self._normalize_key(event.keysym))

    def _on_focus_out(self, event) -> None:
        self.pressed_keys.clear()
        self._stop_mouse_look()

    def _on_mouse_press(self, event) -> None:
        self.mouse_look_enabled = True
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        self.canvas.focus_set()
        self.canvas.grab_set()
        self._set_cursor_hidden(True)

    def _on_mouse_release(self, event) -> None:
        self._stop_mouse_look()

    def _on_mouse_motion(self, event) -> None:
        if not self.mouse_look_enabled:
            return

        if self.last_mouse_x is None or self.last_mouse_y is None:
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y
            return

        self.mouse_dx += event.x - self.last_mouse_x
        self.mouse_dy += event.y - self.last_mouse_y
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def _stop_mouse_look(self) -> None:
        self.mouse_look_enabled = False
        self.last_mouse_x = None
        self.last_mouse_y = None
        self._set_cursor_hidden(False)
        try:
            self.canvas.grab_release()
        except tk.TclError:
            pass

    def _set_cursor_hidden(self, hidden: bool) -> None:
        try:
            self.canvas.configure(cursor="none" if hidden else "")
        except tk.TclError:
            pass

    def get_keys(self) -> set[str]:
        """Return keys currently held down."""
        return set(self.pressed_keys)

    def consume_mouse_delta(self) -> tuple[float, float]:
        """Return accumulated mouse movement and reset it."""
        dx = self.mouse_dx
        dy = self.mouse_dy
        self.mouse_dx = 0.0
        self.mouse_dy = 0.0
        return dx, dy

    def draw_framebuffer(self, color_buffer: Sequence[Sequence[Color]]) -> None:
        """Copy a low-res RGB framebuffer to the Tk image."""
        rows = []
        for y in range(self.height):
            row = " ".join(color_buffer[y][x].to_hex() for x in range(self.width))
            rows.append("{" + row + "}")

        self.image.put(" ".join(rows))

        # Keep a strong reference; Tk images disappear otherwise.
        self.display_image = (
            self.image if self.scale == 1 else self.image.zoom(self.scale, self.scale)
        )
        self.canvas.itemconfig(self.canvas_image, image=self.display_image)

    def set_title(self, title: str) -> None:
        """Update the window title."""
        self.root.title(title)

    def close(self) -> None:
        self.is_open = False
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def run(self, frame_callback: Callable[[], None], fps: int = 60) -> None:
        """Call frame_callback roughly `fps` times per second."""
        delay_ms = max(1, int(1000 / fps))

        def tick() -> None:
            if not self.is_open:
                return
            frame_callback()
            if self.is_open:
                self.root.after(delay_ms, tick)

        self.root.after(0, tick)
        self.root.mainloop()
