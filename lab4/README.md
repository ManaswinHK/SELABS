# Lab 4: VibeCoding - Marble Tilt Maze

**Name:** H K Manaswin  **SRN:** PES1UG24AM108

Fixing and extending a broken Pygame marble tilt maze with an LLM as the pair-programming partner. The marble accelerates toward the mouse cursor (relative to the window centre) and must reach the green goal before the timer runs out.

## Contents

```
lab4/
├── code/                    # updated game (original README inside)
│   ├── main.py
│   ├── requirements.txt
│   └── game/
│       ├── game_engine.py
│       ├── marble.py
│       ├── wall.py
│       └── sounds.py
├── videos/
│   ├── before.mp4           # original code, showing the corner-collision bug
│   └── after.mp4            # final code, showing the fixes and new features
├── Lab4_Chat_History.pdf    # exported chat with the LLM
└── README.md
```

## Tasks completed (one commit each)

| Task | What changed |
|------|--------------|
| 1. Collision detection | Replaced the square bounding-box test with a true circle-vs-rectangle test (closest point on the wall), so the marble only bounces when it really touches a wall. Handles the marble centre ending up inside a wall. |
| 2. Game over screen | In-window end screen showing "Maze Solved!" with the finish time, or "Time's Up!", instead of printing to the console. Waits for a key press. |
| 3. Replay | Choose **1 Easy / 2 Medium / 3 Hard** after the end screen to play again (or **Q / ESC** to exit). Difficulty changes tilt strength, friction and time limit, and is shown next to the timer. |
| 4. Sound feedback | Sound effects for bouncing off a wall, reaching the goal, and the timer running out (`game/sounds.py`). |
| Fix | HUD timer freezes after the round ends and rounds remaining seconds up. |

| Difficulty | Tilt | Friction | Time limit |
|------------|------|----------|-----------|
| Easy | 0.5 | 0.04 | 60 s |
| Medium | 0.6 | 0.02 | 45 s |
| Hard | 0.8 | 0.01 | 30 s |

## How to run

Requires Python 3.10+.

```bash
cd code
pip install -r requirements.txt
python main.py
```

Move the mouse around the window centre to tilt the board. Reach the green circle before time runs out.
