import subprocess


def shutdown(delay='now'):
    subprocess.Popen(['sudo', 'shutdown', '-h', delay])


def restart(delay='now'):
    subprocess.Popen(['sudo', 'shutdown', '-r', delay])


def get_uptime():
    output, err = subprocess.Popen(['uptime']).communicate()
    return output
