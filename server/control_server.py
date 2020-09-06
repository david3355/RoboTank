import socket
from threading import Thread

from robologger.robologger import get_logger
from server.processor import Processor

log = get_logger('RoboCar control server')


"""
Control server for receiving continuous control data (X, Y axis)
"""


class ControlServer:
    def __init__(self, port, host="0.0.0.0"):
        self.host = host
        self.port = port
        self.processors = []
        self.sock = None
        self.receiving = False

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        log.info("Listening on UDP %s:%s" % (self.host, self.port))
        self.sock.bind((self.host, self.port))
        receiver = Thread(target=self.__receive)
        receiver.start()

    def __receive(self):
        log.info("Receiving data...")
        self.receiving = True
        while self.receiving:
            (data, addr) = self.sock.recvfrom(1024)
            self.__process(data.decode("utf-8"))

    def stop(self):
        log.info("Stopping control server...")
        self.receiving = False
        if self.sock is not None:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()

    def add_command_processor(self, processor: Processor):
        self.processors.append(processor)

    def __process(self, command: str):
        log.info("Processing command: %s", command)
        for processor in self.processors:
            processor.process(command)

