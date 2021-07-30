import signal
import os


def kill_previous_from_file(file):
    try:
        with open(file, "r") as f:
            pid = f.read()
        os.kill(int(pid), signal.SIGTERM)
    except ProcessLookupError as e:
        pass

    with open(file, "w+") as f:
        f.write(str(os.getpid()))