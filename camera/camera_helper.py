import subprocess


class CameraHelper:
    STATUS_BROADCASTING = "BROADCASTING"
    STATUS_OFF = "OFF"

    def __init__(self):
        self.broadcast_address = None
        self.broadcast_port = 25005
        self.broadcasting = False
        self.cam_pid = None

    def start_camera(self):
        params = {
            "host": self.broadcast_address,
            "port": self.broadcast_port}
        cmd = self.__build_cmd(params)
        print("Run command: {}".format(cmd))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self.broadcasting = True
        self.cam_pid = process.pid
        output, error = process.communicate()
        print("Camera started. Output: {}, Error: {}, PID: {}".format(output, error, self.cam_pid))
        return output

    def stop_camera(self):
        if self.cam_pid is not None:
            cmd = ["sudo", "kill", str(self.cam_pid)]
            print("Stopping raspivid ({})".format(self.cam_pid))
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
            print("Stopped raspivid ({})".format(self.cam_pid))

    def __build_cmd(self, params):
        vid_cmd = ['raspivid', '-a', '12', '-t', '0', '-w', '1280', '-h', '720', '-ih', '-fps', '30', '-o',
                   'udp://{host}:{port}'.format(**params)]
        return vid_cmd

    def set_broadcast_address(self, broadcast_address):
        if self.__value_is_valid(broadcast_address):
            self.broadcast_address = broadcast_address

    def set_broadcast_port(self, broadcast_port):
        if self.__value_is_valid(broadcast_port):
            self.broadcast_port = broadcast_port

    def get_broadcast_address(self):
        return self.broadcast_address

    def get_broadcast_port(self):
        return self.broadcast_port

    def get_status(self):
        return self.STATUS_BROADCASTING if self.broadcasting else self.STATUS_OFF

    @staticmethod
    def __value_is_valid(value):
        return value is not None and value != ""
