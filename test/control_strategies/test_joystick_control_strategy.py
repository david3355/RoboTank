from unittest import TestCase

from motor.control_strategies.joystick_control_strategy import JoystickControlStrategy


class TestJoystickControlStrategy(TestCase):
    def setUp(self) -> None:
        self.control_strategy = JoystickControlStrategy()

    def test_almost_equal_true(self):
        almost_eq = self.control_strategy.almost_equal(95, 100)
        self.assertTrue(almost_eq)

    def test_almost_equal_false(self):
        almost_eq = self.control_strategy.almost_equal(94, 100)
        self.assertFalse(almost_eq)

    def test_get_quarter_throttle_north_east_x10(self):
        x = 100
        y = 10
        left, right = self.control_strategy.get_quarter_throttle(x, y)
        self.assertEqual(left, 1)
        self.assertEqual(right, 0.95)

    def test_get_quarter_throttle_north_east_y10(self):
        x = 10
        y = 100
        left, right = self.control_strategy.get_quarter_throttle(x, y)
        self.assertEqual(left, 1)
        self.assertEqual(right, 0.05)

    def test_get_quarter_throttle_east_south_x10(self):
        x = -100
        y = 10
        left, right = self.control_strategy.get_quarter_throttle(x, y)
        self.assertEqual(left, -1)
        self.assertEqual(right, -0.95)

    def test_get_quarter_throttle_east_south_y10(self):
        x = -10
        y = 100
        left, right = self.control_strategy.get_quarter_throttle(x, y)
        self.assertEqual(left, -1)
        self.assertEqual(right, -0.05)

    def test_get_quarter_throttle_north_east(self):
        x = 50
        y = 50
        left, right = self.control_strategy.get_quarter_throttle(x, y)
        self.assertEqual(left, 1)
        self.assertEqual(right, 0.5)

    def test_get_quarter_throttle_east_south(self):
        x = -50
        y = 50
        left, right = self.control_strategy.get_quarter_throttle(x, y)
        self.assertEqual(left, -1)
        self.assertEqual(right, -0.5)

    def test_get_quarter_throttle_south_west(self):
        x = -50
        y = -50
        left, right = self.control_strategy.get_quarter_throttle(x, y)
        self.assertEqual(left, -0.5)
        self.assertEqual(right, -1)

    def test_get_quarter_throttle_west_north(self):
        x = 50
        y = -50
        left, right = self.control_strategy.get_quarter_throttle(x, y)
        self.assertEqual(left, 0.5)
        self.assertEqual(right, 1)

    def test_calculate_strategy_forward(self):
        x = 100
        y = 0
        engine_throttle = self.control_strategy.calculate_strategy(x, y)
        self.assertEqual(engine_throttle.left_throttle, 1)
        self.assertEqual(engine_throttle.right_throttle, 1)

    def test_calculate_strategy_backward(self):
        x = -100
        y = 0
        engine_throttle = self.control_strategy.calculate_strategy(x, y)
        self.assertEqual(engine_throttle.left_throttle, -1)
        self.assertEqual(engine_throttle.right_throttle, -1)

    def test_calculate_strategy_left_rotation(self):
        x = 0
        y = 100
        engine_throttle = self.control_strategy.calculate_strategy(x, y)
        self.assertEqual(engine_throttle.left_throttle, 1)
        self.assertEqual(engine_throttle.right_throttle, -1)

    def test_calculate_strategy_right_rotation(self):
        x = 0
        y = -100
        engine_throttle = self.control_strategy.calculate_strategy(x, y)
        self.assertEqual(engine_throttle.left_throttle, -1)
        self.assertEqual(engine_throttle.right_throttle, 1)

    def test_calculate_strategy_full_strength(self):
        x = 100
        y = 0
        engine_throttle = self.control_strategy.calculate_strategy(x, y)
        self.assertEqual(engine_throttle.left_throttle, 1)
        self.assertEqual(engine_throttle.right_throttle, 1)

    def test_calculate_strategy_half_strength(self):
        x = 50
        y = 0
        engine_throttle = self.control_strategy.calculate_strategy(x, y)
        self.assertEqual(engine_throttle.left_throttle, 0.5)
        self.assertEqual(engine_throttle.right_throttle, 0.5)