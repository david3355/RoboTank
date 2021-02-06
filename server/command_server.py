# REST service for controlling robot

import json
import socketserver
import types
from http import server
from threading import Thread

from camera.camera_helper import CameraHelper
from motor.driver import MotorDriver
from network.discovery.network_interface_helper import get_interfaces, get_ip, get_netmask, get_broadcast
from robologger.robologger import get_logger
from server.processor import ControlSignalProcessor, ProcessMode
from system.syshelper import shutdown, restart, get_uptime

log = get_logger('RoboCar control server')


class CommandHandler(server.BaseHTTPRequestHandler):
    ROUTING_TABLE = {}
    driver = None
    cmd_processor = None
    set_command_host_callback = None

    @staticmethod
    def set_driver(driver: MotorDriver):
        CommandHandler.driver = driver

    @staticmethod
    def set_command_processor(command_processor: ControlSignalProcessor):
        CommandHandler.cmd_processor = command_processor

    @staticmethod
    def set_commandeer_handler(set_command_host_callback: types.FunctionType):
        CommandHandler.set_command_host_callback = set_command_host_callback

    def get(self):
        pass

    def post(self, data: dict):
        pass

    def route(self, path):
        CommandHandler.ROUTING_TABLE["/"] = self.root_handler
        CommandHandler.ROUTING_TABLE["/speed"] = SpeedHandler
        CommandHandler.ROUTING_TABLE["/control"] = ControlHandler
        CommandHandler.ROUTING_TABLE["/processmode"] = ModeHandler
        CommandHandler.ROUTING_TABLE["/processmodes"] = ModesHandler
        CommandHandler.ROUTING_TABLE["/commandeer"] = CommandeerHandler
        CommandHandler.ROUTING_TABLE["/camera"] = CameraHandler
        CommandHandler.ROUTING_TABLE["/get_cam_status"] = CameraHandler
        CommandHandler.ROUTING_TABLE["/system"] = SystemHandler
        CommandHandler.ROUTING_TABLE["/interfaces"] = InterfacesHandler
        for route, processor in self.ROUTING_TABLE.items():
            if route == path:
                return processor()
        return None

    def do_POST(self):
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            data_json = json.loads(data_string)
            handler = self.route(self.path)
            if handler is not None:
                handler.post(self, data_json)
            else:
                self.send_response(404)
                self.set_headers({'Content-Type': 'application/json'})
                self.set_return_value({"status": "no such resource"})
                log.warn("Resource is not found: %s", self.path)
        except BaseException as bex:
            self.send_response(500, message=str(bex))
            log.warn("Error while processing request on %s: %s", self.path, str(bex))

    def do_GET(self):
        try:
            handler = self.route(self.path)
            if handler is not None:
                handler.get(self)
            else:
                self.send_response(404)
                self.set_headers({'Content-Type': 'application/json'})
                self.set_return_value({"status": "no such resource"})
                log.warn("Resource is not found: %s", self.path)
        except BaseException as bex:
            self.send_response(500, message=str(bex))
            log.warn("Error while processing request on %s: %s", self.path, str(bex))


    # Handlers:

    def root_handler(self):
        self.send_response(200)
        self.set_headers({'Content-Type': 'application/json'})
        self.set_return_value({"status": "ok"})

    def set_headers(self, headers: dict):
        for key, value in headers.items():
            self.send_header(key, value)
            self.end_headers()

    def set_return_value(self, data: dict):
        self.wfile.write(json.dumps(data).encode('utf-8'))


class BaseHandler:
    def handle_error(self, handler, error_code, message):
        handler.send_response(error_code)
        handler.set_headers({'Content-Type': 'application/json'})
        handler.set_return_value({"error": message})

    def set_response(self, handler, status, resp_value):
        handler.send_response(status)
        handler.set_headers({'Content-Type': 'application/json'})
        handler.set_return_value(resp_value)


class CommandeerHandler(BaseHandler):
    def post(self, base_handler, data: dict):
        id = data.get("id")
        commander_host = base_handler.client_address[0]
        print("Commandeer: {} - {}".format(commander_host, id))
        if id is not None:
            if CommandHandler.set_command_host_callback is not None:
                CommandHandler.set_command_host_callback(commander_host)
            # TODO start receiving UDP
            # TODO start sending status
            self.set_response(base_handler, 202, {"status": "Receiving control over UDP, sending status", "id": id,
                                                  "commander_host": commander_host})
        else:
            self.handle_error(base_handler, 422, "Please provide a commandeer ID!")


class SystemHandler(BaseHandler):
    CMDS = {
        "shutdown": shutdown,
        "restart": restart
    }

    def post(self, base_handler, data: dict):
        base_handler.send_response(202)
        command = data.get("command")
        if command is not None and command is not None:
            cmd_func = SystemHandler.CMDS.get(command)
            if cmd_func is not None:
                cmd_func()
                self.set_response(base_handler, 200, {"command_executed": command})

    def get(self, base_handler):
        self.set_response(base_handler, 200, {"uptime": get_uptime()})


class CameraHandler(BaseHandler):
    def __init__(self):
        self.cam_helper = CameraHelper()

    def get(self, base_handler):
        base_handler.send_response(200)
        base_handler.set_headers({'Content-Type': 'application/json'})

        base_handler.set_return_value(
            {"broadcast_address": self.cam_helper.get_broadcast_address(),
             "broadcast_port": self.cam_helper.get_broadcast_port(),
             "status": self.cam_helper.get_status()})

    def post(self, base_handler, data: dict):

        cmd = data.get("command")
        if cmd == "start":
            broadcast_address = data.get("broadcast_address", None)
            broadcast_port = data.get("broadcast_port", None)
            width = data.get("width", None)
            height = data.get("height", None)
            self.cam_helper.set_broadcast_address(broadcast_address)
            self.cam_helper.set_broadcast_port(broadcast_port)
            self.cam_helper.set_width(width)
            self.cam_helper.set_height(height)
            self.cam_helper.start_camera()
            self.set_response(base_handler, 202, {"status": "started", "params": "{}, {}, {}, {}".format(
                broadcast_address, broadcast_port, width, height)})
        elif cmd == "stop":
            self.cam_helper.stop_camera()
            self.set_response(base_handler, 202, {"status": "stopped"})


class SpeedHandler(BaseHandler):
    def get(self, base_handler):
        left_speed = CommandHandler.driver.left_speed
        right_speed = CommandHandler.driver.right_speed
        self.set_response(base_handler, 200, {"left_speed": left_speed, "right_speed": right_speed})

    def post(self, base_handler, data: dict):
        left_speed = data.get("left_speed")
        right_speed = data.get("right_speed")
        if left_speed is not None:
            CommandHandler.driver.left_speed = left_speed
        if right_speed is not None:
            CommandHandler.driver.right_speed = right_speed
        self.set_response(base_handler, 202, {"left_speed": left_speed, "right_speed": right_speed})


class ControlHandler(BaseHandler):
    def post(self, base_handler, data: dict):
        base_handler.send_response(202)
        direction = data.get("direction")
        distance = data.get("distance")
        if direction is not None and distance is not None:
            CommandHandler.driver.go_forward(distance, 10)
            self.set_response(base_handler, 202, {"direction": direction, "distance": distance})


class ModeHandler(BaseHandler):
    def validate_mode(self, mode):
        return mode in ProcessMode.get_modes()

    def post(self, base_handler, data: dict):
        mode = data.get("mode")
        if mode is not None and self.validate_mode(mode):
            CommandHandler.cmd_processor.set_process_mode(mode)
            self.set_response(base_handler, 202, {"process_mode": mode})
        else:
            self.handle_error(base_handler, 422, "mode {} is not valid".format(mode))

    def get(self, base_handler):
        process_mode = CommandHandler.cmd_processor.get_process_mode()
        self.set_response(base_handler, 200, {"process_mode": process_mode})


class ModesHandler(BaseHandler):
    def get(self, base_handler):
        process_modes = ProcessMode.get_modes()
        self.set_response(base_handler, 200, {"process_modes": process_modes})


class InterfacesHandler(BaseHandler):
    def get(self, base_handler):
        interfaces = get_interfaces("wlan")
        interface_data = {}
        for iface in interfaces:
            interface_data[iface] = {
                "ip_address": get_ip(iface),
                "netmask": get_netmask(iface),
                "broadcast": get_broadcast(iface)
            }
        self.set_response(base_handler, 200, interface_data)


class CmdServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class CommandServer:
    def __init__(self, port, host="0.0.0.0"):
        self.address = (host, port)
        self.server = CmdServer(self.address, CommandHandler)

    def start(self):
        log.info("Starting command server on %s:%s", self.address[0], self.address[1])
        thread = Thread(target=lambda: self.server.serve_forever())
        thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
