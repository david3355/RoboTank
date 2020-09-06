#from adafruit_motorkit import MotorKit

#####################################################################
# dummy MotorKit until project is tested on raspberry
class MotorKit:
    def __init__(self):
        self.motor1 = Motor()
        self.motor2 = Motor()
        self.motor3 = Motor()
        self.motor4 = Motor()


class Motor:
    def __init__(self):
        self.throttle = 0

#####################################################################

class MotorDriver:
    def __init__(self):
        self.left_speed = 0
        self.right_speed = 0
        self.engine_ctrl = MotorKit()

    def __set_left_motor(self, throttle):
        if self.__throttle_is_valid(throttle):
            self.left_speed = throttle
            self.engine_ctrl.motor1.throttle = throttle

    def __set_right_motor(self, throttle):
        if self.__throttle_is_valid(-throttle):
            self.right_speed = -throttle
            self.engine_ctrl.motor2.throttle = -throttle

    @staticmethod
    def __throttle_is_valid(throttle):
        if -1 < throttle < 1:
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
        print("AxisX: {}; AxisY: {}".format(axisX, axisY))

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
