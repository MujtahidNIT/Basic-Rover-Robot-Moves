# src/robot.py
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Robot:
    """
    A class representing a toy robot on a 5x5 tabletop.
    """

    def __init__(self):
        """
        Initialize the robot with no position or direction.
        """
        self.x = None  # X coordinate (0-4)
        self.y = None  # Y coordinate (0-4)
        self.f = None  # Facing direction
        self.directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']

    def place(self, x, y, f):
        """
        Place the robot on the table if the position is valid.

        :param x: Integer X position (0-4)
        :param y: Integer Y position (0-4)
        :param f: Direction string (NORTH, SOUTH, EAST, WEST)
        :return: True if placed successfully, False otherwise
        """
        if not (isinstance(x, int) and isinstance(y, int)):
            logging.warning("Invalid place: x and y must be integers")
            return False
        if 0 <= x < 5 and 0 <= y < 5 and f in self.directions:
            self.x = x
            self.y = y
            self.f = f
            logging.info(f"Placed at {x},{y},{f}")
            return True
        logging.warning(f"Invalid place: {x},{y},{f}")
        return False

    def move(self):
        """
        Move the robot one unit forward if possible without falling off.
        """
        if self.x is None:
            logging.warning("Move ignored: Robot not placed")
            return
        deltas = {
            'NORTH': (0, 1),
            'SOUTH': (0, -1),
            'EAST': (1, 0),
            'WEST': (-1, 0)
        }
        dx, dy = deltas[self.f]
        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < 5 and 0 <= ny < 5:
            self.x, self.y = nx, ny
            logging.info(f"Moved to {self.x},{self.y}")
        else:
            logging.warning("Move ignored: Would fall off table")

    def left(self):
        """
        Rotate the robot 90 degrees left.
        """
        if self.f is None:
            logging.warning("Left ignored: Robot not placed")
            return
        idx = self.directions.index(self.f)
        self.f = self.directions[(idx - 1) % 4]
        logging.info(f"Turned left to {self.f}")

    def right(self):
        """
        Rotate the robot 90 degrees right.
        """
        if self.f is None:
            logging.warning("Right ignored: Robot not placed")
            return
        idx = self.directions.index(self.f)
        self.f = self.directions[(idx + 1) % 4]
        logging.info(f"Turned right to {self.f}")

    def report(self):
        """
        Get the current position and direction as a string.

        :return: "X,Y,F" or None if not placed
        """
        if self.f is None:
            logging.warning("Report ignored: Robot not placed")
            return None
        report_str = f"{self.x},{self.y},{self.f}"
        logging.info(f"Report: {report_str}")
        return report_str