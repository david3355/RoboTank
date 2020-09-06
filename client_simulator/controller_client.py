import socket


class ControllerClient:
    def __init__(self, remote_host, remote_port):
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.socket = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

    def send(self, message):
        #print("Sending message to {}:{}".format(self.remote_host, self.remote_port))
        self.socket.sendto(message.encode('utf-8'), (self.remote_host, self.remote_port))
        #print("Message sent.")
