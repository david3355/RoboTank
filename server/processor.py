from abc import abstractmethod

from motor.driver import MotorDriver


class InvalidCommandException(BaseException):
    pass


class Processor:
    @abstractmethod
    def process(self, command: str):
        pass

    @abstractmethod
    def _valid(self, command: str):
        pass


class ProcessMode:
    MANUAL = "manual"
    CONTROLLED = "controlled"

    @staticmethod
    def get_modes():
        return [ProcessMode.CONTROLLED, ProcessMode.MANUAL]

class CommandProcessor(Processor):
    def __init__(self, motor_driver: MotorDriver):
        self.driver = motor_driver
        self.process_mode = ProcessMode.CONTROLLED
        self.processor = self.__get_processor(self.process_mode)

    def __get_processor(self, process_mode):
        procs = {
            ProcessMode.MANUAL: ManualProcessor,
            ProcessMode.CONTROLLED: ControlledlProcessor
        }

        processor = procs.get(process_mode, ControlledlProcessor)
        return processor(self.driver)

    def set_process_mode(self, process_mode: str):
        self.process_mode = process_mode
        self.processor = self.__get_processor(self.process_mode)


    def get_process_mode(self):
        return self.process_mode

    def process(self, command: str):
        if not self.processor.valid(command):
            return
        self.processor.process(command)


class BaseProcessor:
    def __init__(self, motor_driver: MotorDriver):
        self.driver = motor_driver

    def valid(self, command: str):
        pass

    def process(self, command: str):
        pass


class ManualProcessor(BaseProcessor):

    def valid(self, command: str):
        tags = command.split(":")
        if len(tags) != 2:
            return False
        return True

    def process(self, command: str):
        tags = command.split(":")
        left_track = int(tags[0])
        right_track = int(tags[1])
        self.driver.set_track(left_track, right_track)


class ControlledlProcessor(BaseProcessor):

    def valid(self, command: str):
        tags = command.split(";")
        if len(tags) != 2:
            return False
        return True

    def process(self, command: str):
        tags = command.split(";")
        x_axis = int(tags[0])
        y_axis = int(tags[1])
        self.driver.joystick_control(x_axis, y_axis)
