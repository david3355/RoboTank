# Jager's RoboTank Project

import signal

from motor.driver import MotorDriver
from network.discovery.broadcaster import Broadcaster
from server.command_server import CommandServer, CommandHandler
from server.control_server import ControlServer
from server.processor import ControlSignalProcessor


broadcaster = Broadcaster(broadcast_interval_sec=2)  # wlan_interface_name="enp0s3" For virtualbox test
command_server = CommandServer(25500)
control_server = ControlServer(25000)


def stop_services():
    try:
        command_server.stop()
        control_server.stop()
        broadcaster.stop_broadcasting()
    except BaseException as bex:
        print("Error on exit: {}".format(bex))


def handle_term_signals(signum, frame):
    print("Handling signal: {}, {}".format(signum, frame))
    stop_services()


def wait_for_user():
    inp = None
    while inp != "x":
        inp = input("Press x to close servers")
    stop_services()


if __name__ == '__main__':

    signal.signal(signal.SIGINT, handle_term_signals)
    signal.signal(signal.SIGTERM, handle_term_signals)

    broadcaster.start_broadcasting()
    driver = MotorDriver()
    cmd_processor = ControlSignalProcessor(driver)

    CommandHandler.set_driver(driver)
    CommandHandler.set_command_processor(cmd_processor)
    CommandHandler.set_commandeer_handler(control_server.set_commander)

    command_server.start()
    control_server.add_command_processor(cmd_processor)
    control_server.start()

    #wait_for_user()
