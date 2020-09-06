# REST service for controlling robot
import json
import socketserver
from http import server
from threading import Thread

from motor.driver import MotorDriver
from robologger.robologger import get_logger
from server.processor import CommandProcessor, ProcessMode

log = get_logger('RoboCar control server')


class CommandHandler(server.BaseHTTPRequestHandler):
    ROUTING_TABLE = {}
    driver = None
    cmd_processor = None

    @staticmethod
    def set_driver(driver: MotorDriver):
        CommandHandler.driver = driver

    @staticmethod
    def set_command_processor(command_processor: CommandProcessor):
        CommandHandler.cmd_processor = command_processor

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
        for route, processor in self.ROUTING_TABLE.items():
            if route == path:
                return processor()
        return None

    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data_json = json.loads(data_string)
        handler = self.route(self.path)
        if handler is not None:
            handler.post(self, data_json)
        else:
            self.send_response(404)

    def do_GET(self):
        handler = self.route(self.path)
        if handler is not None:
            handler.get(self)
        else:
            self.send_response(404)
            self.set_headers({'Content-Type': 'application/json'})
            self.set_return_value({"status": "no such resource"})

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


class SpeedHandler(BaseHandler):
    def get(self, base_handler):
        left_speed = CommandHandler.driver.left_speed
        right_speed = CommandHandler.driver.right_speed
        base_handler.send_response(200)
        base_handler.set_headers({'Content-Type': 'application/json'})
        base_handler.set_return_value({"left_speed": left_speed, "right_speed": right_speed})

    def post(self, base_handler, data: dict):
        base_handler.send_response(202)
        left_speed = data.get("left_speed")
        right_speed = data.get("right_speed")
        if left_speed is not None:
            CommandHandler.driver.left_speed = left_speed
        if right_speed is not None:
            CommandHandler.driver.right_speed = right_speed


class ControlHandler(BaseHandler):
    def post(self, base_handler, data: dict):
        base_handler.send_response(202)
        direction = data.get("direction")
        distance = data.get("distance")
        if direction is not None and distance is not None:
            CommandHandler.driver.go_forward(distance, 10)


class ModeHandler(BaseHandler):
    def validate_mode(self, mode):
        return mode in ProcessMode.get_modes()

    def post(self, base_handler, data: dict):
        base_handler.send_response(202)
        mode = data.get("mode")
        if mode is not None and self.validate_mode(mode):
            CommandHandler.cmd_processor.set_process_mode(mode)
            base_handler.set_headers({'Content-Type': 'application/json'})
            base_handler.set_return_value({"process_mode": mode})
        else:
            self.handle_error(base_handler, 422, "mode {} is not valid".format(mode))

    def get(self, base_handler):
        base_handler.send_response(200)
        process_mode = CommandHandler.cmd_processor.get_process_mode()
        base_handler.set_headers({'Content-Type': 'application/json'})
        base_handler.set_return_value({"process_mode": process_mode})


class ModesHandler(BaseHandler):
    def get(self, base_handler):
        base_handler.send_response(200)
        process_modes = ProcessMode.get_modes()
        base_handler.set_headers({'Content-Type': 'application/json'})
        base_handler.set_return_value({"process_modes": process_modes})


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
