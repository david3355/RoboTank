from wifi import Cell


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
