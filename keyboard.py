"""
Tiny non-blocking keyboard input helper for terminal demos.

Маленький helper для неблокирующего ввода с клавиатуры в терминале.
"""

import os
import sys


if os.name == "nt":
    import msvcrt
else:
    import select
    import termios
    import tty


class Keyboard:
    """
    Non-blocking keyboard reader.

    Неблокирующее чтение клавиш.
    """

    def __enter__(self) -> "Keyboard":
        if os.name != "nt":
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if os.name != "nt":
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def poll_keys(self) -> set[str]:
        """
        Return all currently available key presses.

        Возвращает все нажатия, которые успели прийти в stdin.
        """
        keys: set[str] = set()

        if os.name == "nt":
            while msvcrt.kbhit():
                ch = msvcrt.getwch()
                keys.add(ch.lower())
            return keys

        while select.select([sys.stdin], [], [], 0)[0]:
            ch = sys.stdin.read(1)
            keys.add(ch.lower())

        return keys