# tests/test_robot.py
import unittest
from src.robot import Robot


class TestRobot(unittest.TestCase):
    """Unit tests for the Cellular Origins Toy Robot."""

    # ------------------------------------------------------------------ #
    #   Helper – fresh robot for every test
    # ------------------------------------------------------------------ #
    def setUp(self) -> None:
        """Create a brand‑new Robot instance before each test."""
        self.robot = Robot()

    # ------------------------------------------------------------------ #
    #   PLACEMENT – VALID
    # ------------------------------------------------------------------ #
    def test_place_valid_position_and_direction(self) -> None:
        """Placing the robot inside the 5×5 table with a valid direction works."""
        self.assertTrue(self.robot.place(0, 0, "NORTH"))
        self.assertEqual(self.robot.x, 0)
        self.assertEqual(self.robot.y, 0)
        self.assertEqual(self.robot.f, "NORTH")

    # ------------------------------------------------------------------ #
    #   PLACEMENT – INVALID COORDINATES
    # ------------------------------------------------------------------ #
    def test_place_invalid_coordinates(self) -> None:
        """
        The robot must reject any X or Y outside the range 0‑4.
        All attributes stay ``None`` after a failed placement.
        """
        invalid_cases = [
            (-1, 0, "NORTH"),   # left of board
            (5, 0, "NORTH"),    # right of board
            (0, -1, "NORTH"),   # below board
            (0, 5, "NORTH"),    # above board
            (2, 5, "EAST"),     # specific example requested
        ]

        for x, y, f in invalid_cases:
            with self.subTest(x=x, y=y, f=f):
                self.assertFalse(self.robot.place(x, y, f))
                self.assertIsNone(self.robot.x)
                self.assertIsNone(self.robot.y)
                self.assertIsNone(self.robot.f)

    # ------------------------------------------------------------------ #
    #   PLACEMENT – INVALID DIRECTION
    # ------------------------------------------------------------------ #
    def test_place_invalid_direction(self) -> None:
        """
        Only the four cardinal directions are allowed.
        Invalid directions leave the robot un‑placed.
        """
        bad_dirs = ["UP", "DOWN", "NORTHWEST", "SOUTHEAST", "LEFT", ""]
        for d in bad_dirs:
            with self.subTest(direction=d):
                self.assertFalse(self.robot.place(2, 2, d))
                self.assertIsNone(self.robot.x)
                self.assertIsNone(self.robot.y)
                self.assertIsNone(self.robot.f)

    # ------------------------------------------------------------------ #
    #   MOVE – NO PRIOR PLACEMENT
    # ------------------------------------------------------------------ #
    def test_move_without_placement_is_ignored(self) -> None:
        """``move()`` does nothing if the robot has never been placed."""
        self.robot.move()
        self.assertIsNone(self.robot.x)
        self.assertIsNone(self.robot.y)
        self.assertIsNone(self.robot.f)

    # ------------------------------------------------------------------ #
    #   MOVE – VALID STEPS
    # ------------------------------------------------------------------ #
    def test_move_forward_inside_table(self) -> None:
        """A placed robot moves one unit in its facing direction."""
        self.robot.place(1, 1, "NORTH")
        self.robot.move()
        self.assertEqual(self.robot.x, 1)
        self.assertEqual(self.robot.y, 2)

    # ------------------------------------------------------------------ #
    #   MOVE – WOULD FALL OFF → IGNORED
    # ------------------------------------------------------------------ #
    def test_move_that_would_fall_off_is_ignored(self) -> None:
        """Attempting to step off the table leaves the robot where it was."""
        self.robot.place(0, 0, "SOUTH")
        self.robot.move()               # tries to go to y = -1
        self.assertEqual(self.robot.x, 0)
        self.assertEqual(self.robot.y, 0)

        self.robot.place(4, 4, "EAST")
        self.robot.move()               # tries to go to x = 5
        self.assertEqual(self.robot.x, 4)
        self.assertEqual(self.robot.y, 4)

    # ------------------------------------------------------------------ #
    #   ROTATION – LEFT
    # ------------------------------------------------------------------ #
    def test_rotate_left(self) -> None:
        """``left()`` rotates 90° counter‑clockwise."""
        self.robot.place(0, 0, "NORTH")
        self.robot.left()
        self.assertEqual(self.robot.f, "WEST")

        self.robot.left()
        self.assertEqual(self.robot.f, "SOUTH")

    # ------------------------------------------------------------------ #
    #   ROTATION – RIGHT
    # ------------------------------------------------------------------ #
    def test_rotate_right(self) -> None:
        """``right()`` rotates 90° clockwise."""
        self.robot.place(0, 0, "NORTH")
        self.robot.right()
        self.assertEqual(self.robot.f, "EAST")

        self.robot.right()
        self.assertEqual(self.robot.f, "SOUTH")

    # ------------------------------------------------------------------ #
    #   REPORT – NO PLACEMENT
    # ------------------------------------------------------------------ #
    def test_report_without_placement_returns_none(self) -> None:
        """``report()`` returns ``None`` when the robot is not on the table."""
        self.assertIsNone(self.robot.report())

    # ------------------------------------------------------------------ #
    #   REPORT – AFTER PLACEMENT
    # ------------------------------------------------------------------ #
    def test_report_returns_correct_string(self) -> None:
        """``report()`` returns ``X,Y,FACING`` after a successful placement."""
        self.robot.place(3, 1, "WEST")
        self.assertEqual(self.robot.report(), "3,1,WEST")

    # ------------------------------------------------------------------ #
    #   EXAMPLE SEQUENCES (original spec)
    # ------------------------------------------------------------------ #
    def test_example_sequence_a(self) -> None:
        """PLACE 0,0,NORTH → MOVE → REPORT → 0,1,NORTH"""
        self.robot.place(0, 0, "NORTH")
        self.robot.move()
        self.assertEqual(self.robot.report(), "0,1,NORTH")

    def test_example_sequence_b(self) -> None:
        """PLACE 0,0,NORTH → LEFT → REPORT → 0,0,WEST"""
        self.robot.place(0, 0, "NORTH")
        self.robot.left()
        self.assertEqual(self.robot.report(), "0,0,WEST")

    def test_example_sequence_c(self) -> None:
        """
        PLACE 1,2,EAST → MOVE → MOVE → LEFT → MOVE → REPORT → 3,3,NORTH
        """
        self.robot.place(1, 2, "EAST")
        self.robot.move()
        self.robot.move()
        self.robot.left()
        self.robot.move()
        self.assertEqual(self.robot.report(), "3,3,NORTH")


if __name__ == "__main__":
    unittest.main(verbosity=2)