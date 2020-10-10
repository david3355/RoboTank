import requests


class CommandClient:
    COMMANDEER = "commandeer"
    SPEED = "speed"
    PROCESS_MODE = "processmode"
    PROCESS_MODES = "processmodes"

    def __init__(self, server_address: str, server_port: int):
        self.address = server_address
        self.port = server_port

    def __get_url(self, resource):
        return "http://{}:{}/{}".format(self.address, self.port, resource)

    def commandeer(self, id):
        resp = requests.post(url=self.__get_url(CommandClient.COMMANDEER), json={"id": id})
        if resp.status_code == 200:
            return resp.json()

    def set_speed(self, left_speed, right_speed):
        resp = requests.post(url=self.__get_url(CommandClient.SPEED),
                             json={"left_speed": left_speed, "right_speed": right_speed})
        return resp

    def get_speed(self):
        resp = requests.get(url=self.__get_url(CommandClient.SPEED))
        if resp.status_code == 200:
            return resp.json()

    def set_mode(self, process_mode):
        resp = requests.post(url=self.__get_url(CommandClient.PROCESS_MODE),
                             json={"mode": process_mode})
        return resp

    def get_mode(self):
        resp = requests.get(url=self.__get_url(CommandClient.PROCESS_MODE))
        if resp.status_code == 200:
            return resp.json()

    def get_modes(self):
        resp = requests.get(url=self.__get_url(CommandClient.PROCESS_MODES))
        if resp.status_code == 200:
            return resp.json()