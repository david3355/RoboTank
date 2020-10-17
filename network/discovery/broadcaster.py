import socket
from threading import Thread
from time import sleep

from network.discovery.network_interface_helper import get_ip, RASPBERRY_WLAN_INTERFACE


class Broadcaster:
    BROADCAST_PORT = 25555

    def __init__(self, broadcast_interval_sec=1, wlan_interface_name=RASPBERRY_WLAN_INTERFACE):
        self.remote_port = self.BROADCAST_PORT
        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcasting = False
        self.caster = Thread(target=self.__sender, daemon=True)
        self.sleep_time = broadcast_interval_sec
        self.wlan_interface = wlan_interface_name


    def __send(self, robotank_ip):
        print("Broadcasting RoboTank IP [{}] to port {}".format(robotank_ip, self.remote_port))
        #self.socket.sendto(robotank_ip, ("<broadcast>", self.remote_port))
        self.socket.sendto(robotank_ip.encode('utf-8'), ("<broadcast>", self.remote_port))

    def __sender(self):
        while self.broadcasting:
            try:
                ip = get_ip(self.wlan_interface)
                self.__send(ip)
                sleep(self.sleep_time)
            except BaseException as ip_exception:
                print("Cannot broadcast RoboTank IP: ".format(ip_exception))

    def start_broadcasting(self):
        self.broadcasting = True
        self.caster.start()

    def stop_broadcasting(self):
        self.broadcasting = False
