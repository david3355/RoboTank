import subprocess


# Default delay is 1 sec instead of 'now' so leave time to respond to client

def shutdown(delay='1'):
    subprocess.Popen(['sudo', 'shutdown', '-h', delay])


def restart(delay='1'):
    subprocess.Popen(['sudo', 'shutdown', '-r', delay])


def get_uptime():
    output, err = subprocess.Popen(['uptime']).communicate()
    return output
