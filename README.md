# Cellular Origins Rover Simulator  
**A toy‑robot simulator:**  CLI, Tkinter GUI, and Streamlit Web UI.

---

## Project Structure
```
TOYROBOT/
├── assets/
│   └── logo.png                 # Application logo (used in GUIs)
├── src/
│   ├── robot.py                 # Core robot logic (5×5 table, PLACE/MOVE/LEFT/RIGHT/REPORT)
│   ├── basic.py                 # **CLI version:** simple command‑line interface
│   ├── tk_app.py                # **Tkinter GUI:** desktop graphical simulator
│   └── web_app.py               # **Streamlit Web UI:** browser‑based graphical simulator
├── tests/
│   └── test_robot.py            # Comprehensive unit tests for `robot.py`
├── requirements.txt             # Python dependencies
└── README.md                    # ← You are here
```

---

## Features

| Mode | Interface | Animation | Rotation | Bounce |
|------|-----------|----------|----------|--------|
| **CLI (`basic.py`)** | Terminal | ASCII table | N/E/S/W | No |
| **Tkinter (`tk_app.py`)** | Desktop GUI | SVG rover | Full | Yes |
| **Streamlit (`web_app.py`)** | Web browser | SVG rover | Full | Yes |

---

## `src/basic.py` Simple CLI Simulator

**No GUI, pure command line.**  
Perfect for quick testing or scripting.

### Run
```bash
cd src
python basic.py
```

### Commands
```
PLACE X,Y,F    → e.g. PLACE 0,0,NORTH
MOVE
LEFT
RIGHT
REPORT
EXIT
```

### Example
```text
> PLACE 0,0,NORTH
> MOVE
> REPORT
Output: 0,1,NORTH
```

> Uses ASCII art with **"ROVER"** cellular title.

### Demo Video

![Rover CLI Demo](assets/basicCLI.mov)

---

## `src/tk_app.py` Tkinter Desktop GUI

A **rich desktop GUI** with:
- Sky‑blue custom title bar with centered logo
- SVG rover with **rotation + bounce animation**
- Hover effects on grid cells
- Deploy, Move, Left, Right, Report controls

### Run
```bash
cd src
python tk_app.py
```

### Troubleshooting `cairosvg` (macOS)

`tk_app.py` uses `cairosvg` to convert SVG → PNG for Tkinter.

If you get:
```
ImportError: cannot import name 'svg2png' from 'cairosvg'
```
or
```
dyld: Library not found: /usr/local/opt/cairo/lib/libcairo.2.dylib
```

**Fix (macOS with Homebrew):**
```bash
brew install cairo
brew install pango
brew install gdk-pixbuf
brew install libffi

# Then run with correct library path
DYLD_LIBRARY_PATH=$(brew --prefix cairo)/lib:$DYLD_LIBRARY_PATH \
    /usr/local/bin/python3 src/tk_app.py
```

> **Tip**: Add this to a shell script:
> ```bash
> #!/bin/bash
> export DYLD_LIBRARY_PATH=$(brew --prefix cairo)/lib:$DYLD_LIBRARY_PATH
> python3 src/tk_app.py
> ```

---

## `src/web_app.py` Streamlit Web UI

**No installation hassle** run in browser.

### Run
```bash
cd src
streamlit run web_app.py
```

Opens at `http://localhost:8501`

### Features
- Responsive grid with **CSS‑animated bouncing rover**
- Full **rotation (N/E/S/W)**
- Sky‑blue title bar with **centered logo**
- Works on any device with a browser

> **Alternative to Tkinter** ideal for sharing or remote access.

---

## `requirements.txt`

```txt
# Core
streamlit>=1.30.0

# Tkinter GUI
cairosvg>=2.7.0
Pillow>=10.0.0

# Testing
unittest2; python_version < '3.0'
# (built‑in `unittest` is used in Python 3+)

# Optional: for colored CLI output
colorama>=0.4.6
```

Install all:
```bash
pip install -r requirements.txt
```

---

## General Setup & Run Steps


### 1. Create virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
# or
venv\Scripts\activate       # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run your preferred interface

| Mode | Command |
|------|---------|
| **CLI** | `python src/basic.py` |
| **Tkinter GUI** | `python src/tk_app.py` |
| **Web UI** | `streamlit run src/web_app.py` |

---

## Run Unit Tests

```bash
python -m unittest discover -s tests -v
```

All test cases will run with **clear pass/fail output**.

---

## General Troubleshooting

| Issue | Solution |
|------|----------|
| `ModuleNotFoundError: No module named 'cairosvg'` | `pip install cairosvg` |
| `dyld: Library not found: libcairo` (macOS) | Use the `DYLD_LIBRARY_PATH` fix above |
| `streamlit: command not found` | `pip install streamlit` |
| Logo not showing | Ensure `assets/logo.png` exists and is readable |
| Rover not rotating in web app | Use **latest Chrome/Firefox** older browsers may block SVG `<use>` |

---

**Banbury, England, UK, OX164RL. November 10, 2025**

*May my rover never fall off the table.*
