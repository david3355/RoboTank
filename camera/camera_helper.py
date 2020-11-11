import subprocess

from robologger.robologger import get_logger

log = get_logger('RoboCar control server')


class CameraHelper:
    STATUS_BROADCASTING = "BROADCASTING"
    STATUS_OFF = "OFF"
    CAMERA_PID = None
    BROADCASTING = False

    def __init__(self):
        self.broadcast_address = None
        self.broadcast_port = 25005
        self.width = 1280
        self.height = 720

    def start_camera(self):
        params = {
            "host": self.broadcast_address,
            "port": self.broadcast_port,
            "w": self.width,
            "h": self.height}
        cmd = self.__build_cmd(params)
        log.info("Run command: {}".format(cmd))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        CameraHelper.BROADCASTING = True
        CameraHelper.CAMERA_PID = process.pid
        #output, error = process.communicate()
        log.info("Camera started. PID: {}".format(CameraHelper.CAMERA_PID))
        return CameraHelper.CAMERA_PID

    def stop_camera(self):
        pid = CameraHelper.CAMERA_PID
        if pid is not None:
            cmd = ["sudo", "kill", str(pid)]
            log.info("Stopping raspivid ({})".format(pid))
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            #output, error = process.communicate()
            log.info("Stopped raspivid ({})".format(pid))
            return True
        else:
            log.warn("Camera process ID is not saved")
            return False

    def __build_cmd(self, params):
        vid_cmd = ['raspivid', '-a', '12', '-t', '0', '-w', str(params.get("w")), '-h', str(params.get("h")),
                   '-ih', '-fps', '30', '-o', 'udp://{host}:{port}'.format(**params)]
        return vid_cmd

    def set_broadcast_address(self, broadcast_address):
        if self.__value_is_valid(broadcast_address):
            self.broadcast_address = broadcast_address

    def set_broadcast_port(self, broadcast_port):
        if self.__value_is_valid(broadcast_port):
            self.broadcast_port = broadcast_port

    def set_width(self, width):
        if self.__value_is_valid(width):
            self.width = width

    def set_height(self, height):
        if self.__value_is_valid(height):
            self.height = height

    def get_broadcast_address(self):
        return self.broadcast_address

    def get_broadcast_port(self):
        return self.broadcast_port

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_status(self):
        return self.STATUS_BROADCASTING if CameraHelper.BROADCASTING else self.STATUS_OFF

    @staticmethod
    def __value_is_valid(value):
        return value is not None and value != ""
