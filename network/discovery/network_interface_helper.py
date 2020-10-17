import netifaces as ni

RASPBERRY_WLAN_INTERFACE = "wlan0"


def get_ip(interface):
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return ip