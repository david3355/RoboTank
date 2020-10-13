from motor.control_strategies.joystick_control_strategy import JoystickControlStrategy


from adafruit_motorkit import MotorKit
import board


#####################################################################
# dummy MotorKit until project is tested on raspberry
#class MotorKit:
#    def __init__(self):
#        self.motor1 = Motor()
#        self.motor2 = Motor()
#        self.motor3 = Motor()
#        self.motor4 = Motor()
#
#class Motor:
#    def __init__(self):
#        self.throttle = 0
#
#####################################################################


class MotorDriver:
    DEFAULT_LOWEST_THROTTLE = 0.5
    MAX_THROTTLE = 1

    def __init__(self):
        self.left_speed = 0
        self.right_speed = 0
        self.engine_ctrl = MotorKit(i2c=board.I2C())
        self.engine_ctrl = MotorKit()
        self.lowest_throttle = self.DEFAULT_LOWEST_THROTTLE
        self.joystick_control_strategy = JoystickControlStrategy()

    def __set_left_motor(self, throttle):
        if self.__throttle_is_valid(throttle):
            throttle = self.__balance_throttle(throttle)
            self.left_speed = throttle
            self.engine_ctrl.motor1.throttle = throttle
            print("Left engine speed: {}".format(throttle))

    def __set_right_motor(self, throttle):
        if self.__throttle_is_valid(-throttle):
            throttle = self.__balance_throttle(throttle)
            self.right_speed = -throttle
            self.engine_ctrl.motor2.throttle = -throttle
            print("Right engine speed: {}".format(throttle))

    def __balance_throttle(self, throttle):
        """
        Returns a balanced throttle value. If the engine cannot work on the regular lowest throttle
        (nearest real number to zero), the throttle will be translated to a value between the manually set lowest
        throttle value and the maximum throttle
        :param throttle: Original throttle
        :return: Balanced throttle
        """
        sign = lambda x: (1, -1)[x < 0]
        st = sign(throttle)
        throttle = abs(throttle)
        if throttle == 0:
            return 0
        return st * ((self.MAX_THROTTLE - self.lowest_throttle) * throttle + self.lowest_throttle)

    @staticmethod
    def __throttle_is_valid(throttle):
        if -MotorDriver.MAX_THROTTLE < throttle < MotorDriver.MAX_THROTTLE:
            return True
        return False

    def start(self, speed):
        """
        Starts the engine at the given speed
        :param speed:
        :return:
        """
        self.__set_left_motor(speed)
        self.__set_right_motor(speed)

    def stop(self):
        """
        Stops the engine
        :return:
        """
        self.__set_left_motor(0)
        self.__set_right_motor(0)

    def set_lowest_throttle(self, lowest_throttle_value):
        if self.__throttle_is_valid(lowest_throttle_value) and lowest_throttle_value != 0:
            self.lowest_throttle = lowest_throttle_value

    def turn_left(self, angle):
        pass

    def turn_right(self, angle):
        pass

    def go_forward(self, distance, speed):
        print("Forward {}".format(distance, speed))

    def go_backward(self, speed):
        pass

    def joystick_control(self, axisX, axisY):
        """
        Control the engine continuously
        :param axisX: forward/backward [-100;100]
        :param axisY: left/right [-100;100]
        :return:
        """
        #print("AxisX: {}; AxisY: {}".format(axisX, axisY))
        engine_throttle = self.joystick_control_strategy.calculate_strategy(axisX, axisY)
        print("Left throttle: {} ||| Right throttle: {}".format(engine_throttle.left_throttle, engine_throttle.right_throttle))
        self.__set_left_motor(engine_throttle.left_throttle)
        self.__set_right_motor(engine_throttle.right_throttle)

    def set_track(self, left_track, right_track):
        """
        Control the track engines manually
        :param left_track: forward/backward [-1;1]
        :param right_track: left/right [-1;1]
        :return:
        """
        print("Left track: {}; Right track: {}".format(left_track, right_track))
        self.__set_left_motor(left_track)
        self.__set_right_motor(right_track)
