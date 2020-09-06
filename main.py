# Jager
from motor.driver import MotorDriver
from server.command_server import CommandServer, CommandHandler
from server.control_server import ControlServer
from server.processor import CommandProcessor


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    driver = MotorDriver()
    cmd_processor = CommandProcessor(driver)

    CommandHandler.set_driver(driver)
    CommandHandler.set_command_processor(cmd_processor)
    command_server = CommandServer(25500)
    command_server.start()

    control_server = ControlServer(25000)
    control_server.add_command_processor(cmd_processor)
    control_server.start()

    inp = None
    while inp != "x":
        inp = input("Press x to close servers")

    command_server.stop()
    control_server.stop()



