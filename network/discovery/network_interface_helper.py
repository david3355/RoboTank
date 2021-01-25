import netifaces as ni

RASPBERRY_WLAN_INTERFACE = "wlan0"


def get_ip(interface):
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return ip


def get_broadcast(interface):
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['broadcast']
    return ip


def get_interfaces(name_filter=""):
    interfaces = ni.interfaces()
    return [iface for iface in interfaces if name_filter in iface]