from random import Random
from threading import Thread
from time import sleep

from client_simulator.command_client import CommandClient
from client_simulator.controller_client import ControllerClient
from client_simulator.robotank_ip_receiver import RoboTankAddressReceiver

rnd = Random()
client = ControllerClient("127.0.0.1", 25000)
inp = None

cont_range = -100, 100
man_range = -1, 1

mode = 0


rec = RoboTankAddressReceiver()
rec.start()

sending = True

def sender():
    while sending: #inp != "x":
        # inp = str(input("Command: "))
        rng = cont_range if mode == 0 else man_range
        x = rnd.randint(*rng)
        y = rnd.randint(*rng)
        rc = "{};{}".format(x, y)
        print("Sending {}".format(rc))
        client.send(rc)
        sleep(0.5)


rc_sender = Thread(target=sender)
rc_sender.start()


command_client = CommandClient("127.0.0.1", 25500)


def process_input(cmd_input):
    params = cmd_input.split(" ")
    if params[0] == "getspeed":
        print (command_client.get_speed())
    elif params[0] == "setspeed":
        command_client.set_speed(params[1], params[2])
    elif params[0] == "getmodes":
        print(command_client.get_modes())
    elif params[0] == "getmode":
        print(command_client.get_mode())
    elif params[0] == "setmode":
        global mode
        mode = 1 if params[1] == "manual" else 0
        command_client.set_mode(params[1])


cmd_input = None
while cmd_input != "x":
    cmd_input = str(input("Command: "))
    print("Processing {}".format(cmd_input))
    try:
        process_input(cmd_input)
    except BaseException as bex:
        print(bex)

rec.stop()
sending = False
print("Command client is done")

