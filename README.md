# Snake Game (Python + Pygame)

Simple, fast Snake built with Python and Pygame. Includes score HUD, pause/restart, and screen-edge wrap.

## Features

- Wrap-around movement at edges
- Gradual speed increase as you eat food
- Pause/resume and game-over restart
- Clean HUD with score and speed

## Setup (Windows)

Requires Python 3.8+.

```powershell
# From the project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If a virtual environment already exists, just activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Run

```powershell
python .\src\snake.py
```

## Controls

- Arrows / WASD: Move
- P: Pause / Unpause
- Space: Restart (when game over)
- Esc: Quit

## Troubleshooting

- "Module not found: pygame": Ensure your venv is active before running.
- Window won’t open on remote/headless: Pygame requires a GUI-capable environment.
- Using a different Python version: Recreate the venv and reinstall with `pip install -r requirements.txt`.

## Notes

- The snake wraps at screen edges.
- Speed increases with score.
