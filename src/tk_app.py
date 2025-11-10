# --------------------------------------------------------------
#  <<<  START OF tk_app.py  >>>
# --------------------------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
from robot import Robot
import time
import os

# --------------------------------------------------------------
#  Build absolute path to the logo that is in ../assets/logo.png
# --------------------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_PATH  = os.path.join(ASSETS_DIR, "logo.png")

class ToyRobotGUI:
    # ====================  REPLACE THE __init__ METHOD  ====================
    def __init__(self, root):
        self.root = root
        self.root.title("")                     # <-- remove native title
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # ----- HIDE NATIVE TITLE BAR -----
        self.root.overrideredirect(True)        # <-- custom title bar

        # ----- CUSTOM SKYBLUE TITLE BAR -----
        self.title_bar = tk.Frame(self.root, bg="skyblue", height=40)
        self.title_bar.pack(fill=tk.X)
        self.title_bar.pack_propagate(False)

        # ---- LOGO (centered) ----
        # ---- LOGO (centered) ----
        try:
            # Load the original image
            logo_raw = tk.PhotoImage(file=LOGO_PATH)

            # Title-bar height = 40 px  → target height
            TARGET_HEIGHT = 40

            # Compute scale factor so height fits exactly
            scale = TARGET_HEIGHT / logo_raw.height()
            new_width  = int(logo_raw.width()  * scale)
            new_height = int(logo_raw.height() * scale)   # will be ≈40

            # Tkinter scaling: zoom for enlargement, subsample for reduction
            if scale > 1:
                # Enlarge
                logo_resized = logo_raw.zoom(int(scale), int(scale))
            else:
                # Reduce (subsample gives integer steps)
                factor = int(1 / scale)
                logo_resized = logo_raw.subsample(factor, factor)

            # If the factor wasn't integer, fall back to PIL for perfect fit
            if abs(logo_resized.height() - TARGET_HEIGHT) > 2:
                # ----- OPTIONAL: use PIL for pixel-perfect resize -----
                from PIL import Image, ImageTk
                pil_img = Image.open(LOGO_PATH)
                pil_img = pil_img.resize((new_width, new_height), Image.LANCZOS)
                logo_resized = ImageTk.PhotoImage(pil_img)
                # -----------------------------------------------------

            self.logo_label = tk.Label(self.title_bar, image=logo_resized, bg="skyblue")
            self.logo_label.image = logo_resized          # keep reference
            self.logo_label.pack(expand=True)             # centered
        except Exception as e:
            # Fallback text
            tk.Label(self.title_bar, text="Mars Rover", bg="skyblue",
                     fg="white", font=('Helvetica', 14, 'bold')).pack(expand=True)

        # ---- CLOSE BUTTON (top-right) ----
        close_btn = tk.Button(self.title_bar, text="X", bg="skyblue", fg="white",
                              bd=0, font=('Helvetica', 12, 'bold'),
                              command=self.root.quit,
                              activebackground="#ff5f5f", activeforeground="white")
        close_btn.place(relx=1.0, x=-10, rely=0.5, anchor='e')

        # ---- DRAG TO MOVE WINDOW ----
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<ButtonRelease-1>", self.stop_move)
        self.title_bar.bind("<B1-Motion>", self.on_motion)

        # ----- MAIN CONTENT FRAME (everything below the title bar) -----
        self.main_frame = tk.Frame(self.root, bg="#0f2027")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # ----- robot & UI init (unchanged) -----
        self.robot = Robot()
        self.placed = False

        # --- SVG Rover (Embedded) ---
        self.rover_svg = {
            "NORTH": self._create_svg(0),
            "EAST":  self._create_svg(90),
            "SOUTH": self._create_svg(180),
            "WEST":  self._create_svg(-90),
        }

        self.setup_ui()
        self.canvas = None
        self.rover_item = None
        self.create_grid()

        # drag helpers
        self.start_x = None
        self.start_y = None

    # ====================  ADD THESE 3 DRAG METHODS  ====================
    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def stop_move(self, event):
        self.start_x = None
        self.start_y = None

    def on_motion(self, event):
        if self.start_x is None or self.start_y is None:
            return
        x = self.root.winfo_x() + event.x - self.start_x
        y = self.root.winfo_y() + event.y - self.start_y
        self.root.geometry(f"+{x}+{y}")

    # ====================  REPLACE setup_ui  ====================
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=10, font=('Helvetica', 10, 'bold'))

        # --- Left Panel (now inside self.main_frame) ---
        left = tk.Frame(self.main_frame, bg="#1a2a3a", width=300)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        left.pack_propagate(False)

        tk.Label(left, text="Mars Rover Control", font=('Helvetica', 16, 'bold'), 
                bg="#1a2a3a", fg="#00ff88").pack(pady=(20, 10))

        # PLACE
        place_frame = tk.LabelFrame(left, text=" Place Rover ", bg="#1a2a3a", fg="white", font=('Helvetica', 10))
        place_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(place_frame, text="X:", bg="#1a2a3a", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.x_var = tk.IntVar(value=0)
        tk.Spinbox(place_frame, from_=0, to=4, textvariable=self.x_var, width=5).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(place_frame, text="Y:", bg="#1a2a3a", fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.y_var = tk.IntVar(value=0)
        tk.Spinbox(place_frame, from_=0, to=4, textvariable=self.y_var, width=5).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(place_frame, text="Facing:", bg="#1a2a3a", fg="white").grid(row=2, column=0, padx=5, pady=5)
        self.f_var = tk.StringVar(value="NORTH")
        tk.OptionMenu(place_frame, self.f_var, "NORTH", "EAST", "SOUTH", "WEST").grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(place_frame, text="PLACE", command=self.place_robot).grid(row=3, column=0, columnspan=2, pady=10)

        # Commands
        cmd_frame = tk.LabelFrame(left, text=" Commands ", bg="#1a2a3a", fg="white", font=('Helvetica', 10))
        cmd_frame.pack(pady=10, fill=tk.X, padx=10)

        ttk.Button(cmd_frame, text="MOVE", command=self.move).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(cmd_frame, text="LEFT", command=self.left).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(cmd_frame, text="RIGHT", command=self.right).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(cmd_frame, text="REPORT", command=self.report).grid(row=1, column=1, padx=5, pady=5)

        # Report
        self.report_label = tk.Label(left, text="Status: Not placed", bg="#1a2a3a", fg="#ffcc00", font=('Courier', 11))
        self.report_label.pack(pady=20)

    # ====================  REPLACE create_grid  ====================
    def create_grid(self):
        canvas_frame = tk.Frame(self.main_frame, bg="#0f2027")
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.canvas = tk.Canvas(canvas_frame, width=400, height=400, bg="#1a2a3a", highlightthickness=0)
        self.canvas.pack()

        cell_size = 70
        margin = 25
        for i in range(6):
            x = margin + i * cell_size
            y = margin + i * cell_size
            self.canvas.create_line(x, margin, x, margin + 5*cell_size, fill="#334455", width=2)
            self.canvas.create_line(margin, y, margin + 5*cell_size, y, fill="#334455", width=2)

        self.cells = {}
        for x in range(5):
            for y in range(5):
                cx = margin + x * cell_size + cell_size // 2
                cy = margin + (4 - y) * cell_size + cell_size // 2
                cell = self.canvas.create_rectangle(
                    cx - 30, cy - 30, cx + 30, cy + 30,
                    fill="#2a3e52", outline="#445566", width=2, tags=f"cell_{x}_{y}"
                )
                self.cells[(x, y)] = cell
                self.canvas.tag_bind(cell, "<Enter>", lambda e, xx=x, yy=y: self.hover_cell(xx, yy, enter=True))
                self.canvas.tag_bind(cell, "<Leave>", lambda e, xx=x, yy=y: self.hover_cell(xx, yy, enter=False))

    # ====================  THE REST OF THE CLASS (unchanged)  ====================
    # (all the methods you already have: _create_svg, _svg_to_png_base64,
    #  hover_cell, place_robot, update_rover, animate_bounce,
    #  move, left, right, report, etc.)
    # --------------------------------------------------------------
    #  <<<  COPY EVERYTHING BELOW THIS LINE EXACTLY AS-IS  >>>
    # --------------------------------------------------------------
    def _create_svg(self, rotation):
        svg = f'''
        <svg width="50" height="50" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="body{rotation}" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#00ff88"/>
              <stop offset="100%" stop-color="#00cc66"/>
            </linearGradient>
            <linearGradient id="window{rotation}" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#66ccff"/>
              <stop offset="100%" stop-color="#3399ff"/>
            </linearGradient>
          </defs>
          <g transform="rotate({rotation} 50 50)">
            <ellipse cx="50" cy="60" rx="36" ry="24" fill="url(#body{rotation})" stroke="#00cc66" stroke-width="3"/>
            <path d="M 35 45 Q 50 35, 65 45 L 65 55 Q 50 62, 35 55 Z" fill="url(#window{rotation})" stroke="#3399ff" stroke-width="2"/>
            <circle cx="28" cy="74" r="12" fill="#333" stroke="#111" stroke-width="3"/>
            <circle cx="72" cy="74" r="12" fill="#333" stroke="#111" stroke-width="3"/>
            <line x1="50" y1="35" x2="50" y2="20" stroke="#ffcc00" stroke-width="3" stroke-linecap="round"/>
            <circle cx="50" cy="16" r="5" fill="#ff6600"/>
          </g>
        </svg>
        '''
        return tk.PhotoImage(data=self._svg_to_png_base64(svg))

    def _svg_to_png_base64(self, svg):
        import io, base64
        from cairosvg import svg2png
        png = svg2png(bytestring=svg.encode('utf-8'), output_width=50, output_height=50)
        return base64.b64encode(png).decode('utf-8')

    def hover_cell(self, x, y, enter):
        color = "#3a5066" if enter else "#2a3e52"
        self.canvas.itemconfig(self.cells[(x, y)], fill=color)

    def place_robot(self):
        x, y, f = self.x_var.get(), self.y_var.get(), self.f_var.get()
        if self.robot.place(x, y, f):
            self.placed = True
            self.update_rover()
            self.report_label.config(text=f"Placed: {x},{y},{f}", fg="#00ff88")
        else:
            messagebox.showerror("Error", "Invalid placement!")

    def update_rover(self):
        if self.rover_item:
            self.canvas.delete(self.rover_item)
        if not self.placed:
            return
        x, y = self.robot.x, self.robot.y
        cell_size = 70
        margin = 25
        cx = margin + x * cell_size + cell_size // 2
        cy = margin + (4 - y) * cell_size + cell_size // 2
        self.rover_item = self.canvas.create_image(cx, cy, image=self.rover_svg[self.robot.f])
        self.animate_bounce()

    def animate_bounce(self):
        if not self.placed or not self.rover_item:
            return
        self.canvas.move(self.rover_item, 0, -2)
        self.root.after(600, lambda: self.canvas.move(self.rover_item, 0, 2))
        self.root.after(1200, self.animate_bounce)

    def move(self):
        if not self.placed: return
        old_x, old_y = self.robot.x, self.robot.y
        self.robot.move()
        if (self.robot.x, self.robot.y) != (old_x, old_y):
            self.update_rover()
            self.report_label.config(text=f"Moved to {self.robot.x},{self.robot.y}", fg="#00ccff")

    def left(self):
        if not self.placed: return
        self.robot.left()
        self.update_rover()
        self.report_label.config(text=f"Facing {self.robot.f}", fg="#ffcc00")

    def right(self):
        if not self.placed: return
        self.robot.right()
        self.update_rover()
        self.report_label.config(text=f"Facing {self.robot.f}", fg="#ffcc00")

    def report(self):
        if not self.placed: return
        rep = self.robot.report()
        self.report_label.config(text=f"REPORT: {rep}", fg="#92fe9d")
        self.root.bell()

# --------------------------------------------------------------
#  <<<  END OF CLASS – keep the if __name__ block unchanged  >>>
# --------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ToyRobotGUI(root)
    root.mainloop()