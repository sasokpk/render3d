# My Tiny Software Renderer

Запуск:

```bash
python3 main.py
```

Главные флаги лежат сверху в `main.py`:

```python
USE_TKINTER = True      # окно
USE_TKINTER = False     # CLI ASCII
SHOW_WIREFRAME = False
DEPTH_DEBUG = False
BACKFACE_CULLING = True
MESH_KIND = "cube"      # или "pyramid"
```

Управление:

- `W/S` — вперёд / назад
- `A/D` — влево / вправо
- `R/F` — вверх / вниз
- `ЛКМ + мышь` — обзор камеры в tkinter-режиме
- `I/J/K/L` — обзор с клавиатуры
- `Q` или `Esc` — выход

