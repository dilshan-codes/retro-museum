# Retro Computing Museum

A Windows desktop application that brings the history of computing to life through interactive emulators and historical documentation. Built with Python and PyQt6.

![Python](https://img.shields.io/badge/Python-3.12-blue) ![PyQt6](https://img.shields.io/badge/PyQt6-6.11-green) ![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

https://github.com/user-attachments/assets/0931c121-8246-4883-aa28-5cdc86e6eec5

---

## What Is This?

Retro Computing Museum is an educational desktop app that lets you explore three landmark machines from computing history — interact with them, run real programs, and read the history behind each one.

The app was built as a learning project to understand how emulators work from the ground up, with every line of code written from scratch.

<div align="center">
  <img src="assets/ss's/img1.png" width="48%"/>
  &nbsp;&nbsp;
  <img src="assets/ss's/img2.png" width="48%"/>
</div>
<br>
<div align="center">
  <img src="assets/ss's/img3.png" width="48%"/>
  &nbsp;&nbsp;
  <img src="assets/ss's/img4.png" width="48%"/>
</div>

---

## Machines Included

### Turing Machine — 1936
Alan Turing's theoretical machine that defined what computation means. Load one of three built-in programs, step through execution one instruction at a time, and watch the tape and read/write head update in real time.


### Manchester Baby — 1948
The world's first stored-program computer. The app loads the actual first program ever run on June 21, 1948. Watch the 32-word memory grid update as the machine executes each of its 7 instructions.


### CHIP-8 — 1977
A virtual machine from the hobbyist computing era. Load any `.ch8` ROM file and play real games — Pong, Breakout, Space Invaders — with live register and memory display.


---

## Features

- Browser-style navigation with back/forward history stack
- Dropdown menu and breadcrumb location bar
- Interactive timeline of computing history from 1936 to 1977
- Detailed history documents for every machine and every timeline event
- Each emulator has a toggle between the emulator view and its history document
- Crossfade image slideshow on the home screen
- Clean warm off-white paper theme throughout

---

## Languages and Tools

| Category | Technology | Purpose |
|---|---|---|
| Language | Python 3.12 | Core application language |
| UI Framework | PyQt6 | Windows, widgets, layouts, painting |
| Document Rendering | Python `markdown` library | Renders `.md` history files as rich text |
| Packaging | PyInstaller | Bundles app into standalone `.exe` |
| Code Formatting | Black | Automatic code formatting |
| Version Control | Git + GitHub | Source control and remote backup |
| IDE | VS Code | Development environment |
| Build System | pip + venv | Package and environment management |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| UI Framework | PyQt6 |
| Document rendering | Python `markdown` library |
| Packaging | PyInstaller |
| Code formatting | Black |

---

## Project Structure
```
retro-museum/
├── main.py                  # App entry point
├── core/
│   ├── navigation.py        # Browser-style history stack
│   └── router.py            # Maps routes to screen classes
├── screens/
│   ├── home.py              # Home screen with image slideshow
│   ├── history.py           # Computing history timeline
│   ├── history_detail.py    # Full event document reader
│   ├── emulators.py         # Emulator selection screen
│   ├── turing.py            # Turing Machine screen
│   ├── baby.py              # Manchester Baby screen
│   └── chip8.py             # CHIP-8 screen
├── emulators/
│   ├── turing_engine.py     # Turing Machine logic
│   ├── baby_engine.py       # Manchester Baby CPU
│   └── chip8_engine.py      # Full CHIP-8 interpreter
├── widgets/
│   └── navbar.py            # Navigation bar widget
├── content/
│   ├── timeline.json        # Timeline event data
│   └── docs/                # History documents in Markdown
└── assets/
    └── images/              # Home screen background images
```

---

## How to Run

**Requirements:** Python 3.12, Windows
```bash
# Clone the repository
git clone https://github.com/dilshan-codes/retro-museum.git
cd retro-museum

# Create virtual environment
py -3.12 -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

---

## How to Use the Emulators

### Turing Machine
1. Go to Emulators → Turing Machine
2. Select a program from the dropdown:
   - **binary_increment** — increments a binary number on the tape
   - **unary_add** — adds two unary numbers
   - **copy** — copies a sequence of 1s
3. Press **Step** to execute one instruction at a time
4. Watch the gold highlighted cell show the read/write head position
5. Press **Run** to execute automatically — adjust speed with the slider
6. Press **Reset** to start the program over

<div align="center">
  <img src="assets/ss's/turing.png" width="78%"/>
</div>

### Manchester Baby
1. Go to Emulators → Manchester Baby
2. The machine loads the actual first program ever run — June 21, 1948
3. Press **Step** to execute one instruction at a time
4. Watch the gold highlighted row in the memory grid show the current instruction
5. Watch the Accumulator and PC values change with each step
6. The current instruction is decoded and shown in plain English below the grid
7. Press **Run** to execute automatically
8. Press **Reset** to reload the 1948 program

<div align="center">
  <img src="assets/ss's/baby.png" width="78%"/>
</div>

### CHIP-8
1. Go to Emulators → CHIP-8
2. Click **Load ROM** and select any `.ch8` file
3. Press **Run**
4. Use the keyboard to play:
```
CHIP-8 Key    Keyboard
─────────────────────
1 2 3 C  →   1 2 3 4
4 5 6 D  →   Q W E R
7 8 9 E  →   A S D F
A 0 B F  →   Z X C V

```

Free CHIP-8 ROMs can be found at [zophar.net](https://www.zophar.net/pdroms/chip8.html).

<div align="center">
  <img src="assets/ss's/ch8.png" width="78%"/>
</div>

---

## What I Learned Building This

- How a virtual machine works at the byte level — fetch, decode, execute
- How the Manchester Baby's 7-instruction architecture executes real programs
- How CHIP-8's 35 opcodes map to a complete game platform
- PyQt6 signals, slots, custom widgets, and paint events
- Browser-style navigation stack implementation
- Python virtual environments, packaging, and project structure

---

*Built from scratch as a personal learning project.* 
<p><strong>dilshan-codes: </strong><a href="https://github.com/dilshan-codes">@dilshan-codes</a></p>
