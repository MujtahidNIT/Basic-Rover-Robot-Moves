# src/main.py
import sys
import os
from robot import Robot

# ----------------------------------------------------------------------
# Helper: pretty-print the 5×5 table with the rover (or empty)
# ----------------------------------------------------------------------
def print_table(robot: Robot):
    # Title – "cellular" style
    print("\n" + "═" * 28)
    print("║" + " CELLULAR ORIGINS ROVER ".center(26, "░") + "║")
    print("═" * 28)

    # Build grid
    grid = [["·" for _ in range(5)] for _ in range(5)]
    if robot.x is not None and robot.y is not None:
        # y-axis is flipped for display (0,0 at top-left)
        grid[4 - robot.y][robot.x] = robot.f[0]   # N,E,S,W

    # Print rows
    for row in grid:
        print("║ " + " ".join(cell.center(4) for cell in row) + " ║")
    print("╘" + "═" * 26 + "╛\n")

# ----------------------------------------------------------------------
# Main REPL loop
# ----------------------------------------------------------------------
def main():
    robot = Robot()
    print("Mars Rover CLI – type commands (PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT | EXIT)")

    while True:
        try:
            cmd = input("> ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not cmd:
            continue

        parts = cmd.split()
        action = parts[0]

        # ------------------- EXIT -------------------
        if action == "EXIT":
            print("Shutting down rover control...")
            break

        # ------------------- PLACE -------------------
        elif action == "PLACE" and len(parts) == 2:
            try:
                coords = parts[1].split(",")
                if len(coords) != 3:
                    raise ValueError
                x, y, f = int(coords[0]), int(coords[1]), coords[2]
                if robot.place(x, y, f):
                    print(f"Placed at {x},{y},{f}")
                else:
                    print("Invalid placement – ignored.")
            except Exception:
                print("Invalid PLACE format. Use: PLACE X,Y,F (e.g., PLACE 0,0,NORTH)")

        # ------------------- MOVE -------------------
        elif action == "MOVE":
            robot.move()

        # ------------------- LEFT -------------------
        elif action == "LEFT":
            robot.left()

        # ------------------- RIGHT -------------------
        elif action == "RIGHT":
            robot.right()

        # ------------------- REPORT -------------------
        elif action == "REPORT":
            rep = robot.report()
            if rep:
                print(f"Output: {rep}")
            else:
                print("Robot not placed yet.")

        # ------------------- UNKNOWN -------------------
        else:
            print("Unknown command. Valid: PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT | EXIT")

        # Always show the table after any valid action
        if action in {"PLACE", "MOVE", "LEFT", "RIGHT", "REPORT"}:
            print_table(robot)

# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()