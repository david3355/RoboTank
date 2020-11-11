import socket
from threading import Thread


class RoboTankAddressReceiver:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 25555
        self.sock = None
        self.receiving = False

    def start(self):
        print("Start receiving IP broadcast")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        receiver = Thread(target=self.__receive, daemon=True)
        receiver.start()

    def __receive(self):
        self.receiving = True
        while self.receiving:
            (data, addr) = self.sock.recvfrom(1024)
            self.__process(data.decode("utf-8"))

    def stop(self):
        self.receiving = False
        if self.sock is not None:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()

    def __process(self, data: str):
        # print(data)
        pass
