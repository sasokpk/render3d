"""Entry point for the tiny software renderer demo."""

from __future__ import annotations

from dataclasses import dataclass
from math import radians
from time import perf_counter, sleep

from camera import Camera
from framebuffer import CUBE_BLUE
from keyboard import Keyboard
from matrix import Matrix4, Vector3
from mesh import Mesh
from renderer import Renderer, RendererSettings
from window import Window

# -----------------------------------------------------------------------------
# Main switches. Change these and run `python3 main.py`.
# -----------------------------------------------------------------------------

USE_TKINTER = True          # True = normal window, False = old CLI ASCII mode
MESH_KIND = "cube"          # "cube" or "pyramid"
AUTO_ROTATE = True
SHOW_WIREFRAME = False
DEPTH_DEBUG = False
BACKFACE_CULLING = True

# Window / framebuffer sizes. The window is WIDTH * SCALE by HEIGHT * SCALE.
TK_WIDTH = 180
TK_HEIGHT = 110
TK_SCALE = 5
CLI_WIDTH = 220
CLI_HEIGHT = 70

FPS = 60
MOVE_SPEED = 6.0
LOOK_SPEED = 2.5
MOUSE_SENSITIVITY = 0.0035
MODEL_SCALE = 3.0
MODEL_ROTATION_SPEED = 0.8


@dataclass(slots=True)
class AppState:
    """Small mutable state bag for the render loop."""

    angle: float = 0.0
    last_time: float = 0.0
    frame_counter: int = 0
    fps_timer: float = 0.0
    fps_value: float = 0.0


def make_renderer(width: int, height: int) -> Renderer:
    """Create a renderer with all global visual switches applied."""
    settings = RendererSettings(
        backface_culling=BACKFACE_CULLING,
        wireframe=SHOW_WIREFRAME,
        depth_debug=DEPTH_DEBUG,
        ambient=0.18,
        light_dir=Vector3(0.0, 1.0, 1.0).normalized(),
        base_color=CUBE_BLUE,
    )
    return Renderer(width=width, height=height, settings=settings)


def make_camera(width: int, height: int) -> Camera:
    """Create the default free camera."""
    return Camera(
        fov=radians(80.0),
        aspect=width / height,
        near=0.1,
        far=100.0,
        position=Vector3(0.0, 0.0, 8.0),
    )


def make_mesh() -> Mesh:
    """Create the selected demo mesh."""
    if MESH_KIND == "pyramid":
        return Mesh.pyramid()
    return Mesh.cube()


def build_model(angle: float) -> Matrix4:
    """Build the animated model matrix."""
    rotation_angle = angle if AUTO_ROTATE else 0.0
    return (
        Matrix4.rotation_z(rotation_angle * 0.35)
        @ Matrix4.rotation_y(rotation_angle)
        @ Matrix4.rotation_x(rotation_angle * 0.65)
        @ Matrix4.uniform_scale(MODEL_SCALE)
    )


def update_camera_keyboard(camera: Camera, keys: set[str], dt: float) -> None:
    """Apply keyboard movement and keyboard look controls."""
    forward_amount = 0.0
    right_amount = 0.0
    up_amount = 0.0

    if "w" in keys:
        forward_amount += MOVE_SPEED * dt
    if "s" in keys:
        forward_amount -= MOVE_SPEED * dt
    if "d" in keys:
        right_amount += MOVE_SPEED * dt
    if "a" in keys:
        right_amount -= MOVE_SPEED * dt
    if "r" in keys:
        up_amount += MOVE_SPEED * dt
    if "f" in keys:
        up_amount -= MOVE_SPEED * dt

    camera.move_local(forward_amount, right_amount, up_amount)

    yaw_delta = 0.0
    pitch_delta = 0.0

    if "j" in keys:
        yaw_delta += LOOK_SPEED * dt
    if "l" in keys:
        yaw_delta -= LOOK_SPEED * dt
    if "i" in keys:
        pitch_delta += LOOK_SPEED * dt
    if "k" in keys:
        pitch_delta -= LOOK_SPEED * dt

    camera.rotate(yaw_delta=yaw_delta, pitch_delta=pitch_delta)


def render_scene(renderer: Renderer, camera: Camera, mesh: Mesh, angle: float) -> None:
    """Render one frame into renderer.screen and renderer.color_buffer."""
    renderer.clear()
    renderer.draw(mesh=mesh, model=build_model(angle), camera=camera)


def update_fps(state: AppState, now: float) -> None:
    """Update a lightweight FPS counter once per second."""
    state.frame_counter += 1
    elapsed = now - state.fps_timer
    if elapsed >= 1.0:
        state.fps_value = state.frame_counter / elapsed
        state.frame_counter = 0
        state.fps_timer = now


def run_tkinter() -> None:
    """Run the renderer in a Tkinter window."""
    renderer = make_renderer(TK_WIDTH, TK_HEIGHT)
    camera = make_camera(TK_WIDTH, TK_HEIGHT)
    mesh = make_mesh()
    window = Window(width=TK_WIDTH, height=TK_HEIGHT, scale=TK_SCALE)

    now = perf_counter()
    state = AppState(last_time=now, fps_timer=now)

    def frame() -> None:
        now = perf_counter()
        dt = min(now - state.last_time, 0.05)
        state.last_time = now

        keys = window.get_keys()
        if "escape" in keys or "q" in keys:
            window.close()
            return

        update_camera_keyboard(camera, keys, dt)

        mouse_dx, mouse_dy = window.consume_mouse_delta()
        camera.rotate(
            yaw_delta=-mouse_dx * MOUSE_SENSITIVITY,
            pitch_delta=-mouse_dy * MOUSE_SENSITIVITY,
        )

        render_scene(renderer, camera, mesh, state.angle)
        window.draw_framebuffer(renderer.color_buffer)

        if AUTO_ROTATE:
            state.angle += MODEL_ROTATION_SPEED * dt

        update_fps(state, now)
        window.set_title(
            "Tiny Software Renderer | "
            f"FPS {state.fps_value:5.1f} | "
            "WASD move, LMB+mouse look, Q/Esc quit"
        )

    window.run(frame, fps=FPS)


def poll_cli_held_keys(
    keyboard: Keyboard,
    held_keys: dict[str, float],
    now: float,
    hold_time: float = 0.12,
) -> set[str]:
    """Make event-based terminal input feel like held-key input."""
    for key in keyboard.poll_keys():
        held_keys[key] = now + hold_time

    expired = [key for key, until in held_keys.items() if until <= now]
    for key in expired:
        del held_keys[key]

    return set(held_keys)


def run_cli() -> None:
    """Run the renderer in old terminal ASCII mode."""
    renderer = make_renderer(CLI_WIDTH, CLI_HEIGHT)
    camera = make_camera(CLI_WIDTH, CLI_HEIGHT)
    mesh = make_mesh()

    now = perf_counter()
    state = AppState(last_time=now, fps_timer=now)
    held_keys: dict[str, float] = {}
    target_frame_time = 1.0 / FPS

    with Keyboard() as keyboard:
        while True:
            frame_start = perf_counter()
            dt = min(frame_start - state.last_time, 0.05)
            state.last_time = frame_start

            keys = poll_cli_held_keys(keyboard, held_keys, frame_start)
            if "q" in keys:
                break

            update_camera_keyboard(camera, keys, dt)
            render_scene(renderer, camera, mesh, state.angle)
            renderer.present()

            print(
                "WASD move | R/F up/down | IJKL look | Q quit | "
                f"pos=({camera.position.x:.2f}, {camera.position.y:.2f}, {camera.position.z:.2f}) | "
                f"tri={renderer.stats.triangles_drawn}/{renderer.stats.triangles_total} | "
                f"pix={renderer.stats.pixels_drawn}"
            )

            if AUTO_ROTATE:
                state.angle += MODEL_ROTATION_SPEED * dt

            elapsed = perf_counter() - frame_start
            if elapsed < target_frame_time:
                sleep(target_frame_time - elapsed)


def main() -> None:
    if USE_TKINTER:
        run_tkinter()
    else:
        run_cli()


if __name__ == "__main__":
    main()
