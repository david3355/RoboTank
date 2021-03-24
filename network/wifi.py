from wifi import Cell
import subprocess


def get_available_networks(interface):
    networks = {}
    try:
        Cells = Cell.all(interface)
        i = 0
        for cell in list(Cells):
            networks[i] = {
                "ssid": cell.ssid,
                "ap_mac": cell.address,
                "encrypted": cell.encrypted,
                "encryption": cell.encryption_type,
                "signal": cell.signal,
            }
            i += 1
    except BaseException as bex:
        print(bex)
    return networks


def get_connected_wifi_ssid():
    try:
        output = subprocess.check_output(['sudo', 'iwgetid'])
        return output.decode("utf-8")
    except:
        return ""


def connect_to_wifi(ssid, psk=None):
    try:
        params = ['sudo', './connect_wifi.sh', ssid]
        if psk is not None:
            params.append(psk)
        output = subprocess.check_output(params)
        return output.decode("utf-8")
    except:
        return ""
