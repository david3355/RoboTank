# Jager's RoboTank Project

from motor.driver import MotorDriver
from network.discovery.broadcaster import Broadcaster
from server.command_server import CommandServer, CommandHandler
from server.control_server import ControlServer
from server.processor import CommandProcessor


if __name__ == '__main__':
    broadcaster = Broadcaster(broadcast_interval_sec=2)
    # wlan_interface_name="enp0s3" For virtualbox test
    broadcaster.start_broadcasting()

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
    broadcaster.stop_broadcasting()
