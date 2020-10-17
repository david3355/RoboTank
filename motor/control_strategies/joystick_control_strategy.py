from math import sqrt


class EngineThrottle:
    def __init__(self, left_throttle, right_throttle):
        self.left_throttle = left_throttle
        self.right_throttle = right_throttle


class ControlStrategy:
    def calculate_strategy(self, control_x: int, control_y: int) -> EngineThrottle:
        pass


class JoystickControlStrategy(ControlStrategy):

    def almost_equal(self, number, sought, e=5):
        return sought-e <= number <= sought + e

    def get_quarter_throttle(self, control_x, control_y):
        quarter_half_point = 0.5
        if abs(control_x) >= abs(control_y):
            rate = abs(control_y) / abs(control_x)
            turner = 1
            pivot = 1 - rate * quarter_half_point
        else:
            rate = abs(control_x) / abs(control_y)
            turner = 1
            pivot = 0 + rate * quarter_half_point

        if control_y > 0:
            left = turner
            right = pivot
        elif control_y < 0:
            right = turner
            left = pivot
        else:
            return 0,0      # This case is not possible since zero throttle is tested prior to this method

        if control_x < 0:
            left *= -1
            right *= -1
        return left, right

    def calculate_strategy(self, control_x: int, control_y: int) -> EngineThrottle:
        strength = sqrt(pow(control_x, 2) + pow(control_y, 2)) / 100.0

        sign = lambda x: (1, -1)[x < 0]
        sx = sign(control_x)
        sy = sign(control_y)

        if self.almost_equal(control_y, 0, e=10):
            return EngineThrottle(sx * strength, sx * strength)
        if self.almost_equal(control_x, 0, e=10):
            return EngineThrottle(sy * strength, -sy * strength)

        if control_x == 0 or control_y == 0:
            return EngineThrottle(0,0)
        left, right = self.get_quarter_throttle(control_x, control_y)

        right *= strength
        left *= strength
        return EngineThrottle(left, right)

