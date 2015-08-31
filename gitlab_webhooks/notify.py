"""
File: gitlab_webhooks/notify.py
Author: John Andersen
Description: Sends notification to screen on text received

To run:
python examples/daemon.py
python sillystream/__main__.py client
"""
import os
import sys
import time
import argparse
import sillystream
import subprocess

DESCRIPTION = "Popups on message recv"
# Stream output from this process to sillystream server
STREAM = False

class on_recv(sillystream.client):
    """
    Calls functions based on what was received
    """
    def __init__(self):
        super(on_recv, self).__init__()
        self.actions = {
            "finished push": self.build_finished,
            "Building \"": self.notify,
        }

    def recv(self, message):
        super(on_recv, self).recv(message)
        for grep in self.actions:
            if grep in message:
                self.actions[grep](message)

    def notify(self, message, title="Notify"):
        command = [
            "notify-send",
            title,
            message
        ]
        return subprocess.check_output(command)

    def build_finished(self, message):
        self.notify(message, "Docker Build Finished")
        # Pull the new image and restart the nodes
        restart_and_update = [
            "/usr/bin/python",
            "/home/john/Documents/distributed-android-testing/docker/docker.py",
            "stop",
            "rm",
            "pull",
            "start"
        ]
        # Restart the manager
        restart_manager = [
            ["docker", "stop", "dat-manager"],
            ["docker", "rm", "dat-manager"],
            ["docker", "run", "-d", "--name", "dat-manager", "--privileged", "--net=host", "raat.jf.intel.com:5000/pdxjohnny/distributed-android-testing", "/bin/dat-manager"]
        ]
        # Pull new before restarting manager
        pull_new = [
            "docker",
            "pull",
            "raat.jf.intel.com:5000/pdxjohnny/distributed-android-testing"
        ]
        try:
            subprocess.check_output(pull_new)
            for command in restart_manager:
                try:
                    subprocess.check_output(command)
                except:
                    pass
            subprocess.check_output(restart_and_update)
            self.notify("Nodes were updated and restarted", "DAT Nodes Redeployed")
        except Exception as error:
            self.notify("Failed to update and restart nodes {}".format(str(error)), "DAT Nodes Failed")

def make_daemon():
    """
    Daemonize to run in background
    """
    pid = os.fork()
    if pid > 0:
        # exit first parent
        sys.exit(0)
    pid = os.fork()
    if pid > 0:
        # exit second parent
        sys.exit(0)
    if STREAM:
        # Create sillystream server
        output = sillystream.server()
        # Start the server
        output.start_thread()
    else:
        output = open("/dev/null", 'wb')
    sys.stdout = output
    sys.stderr = output

def arg_setup():
    arg_parser = argparse.ArgumentParser(description=DESCRIPTION)
    arg_parser.add_argument("--host", type=unicode, \
        help="Address of host server")
    arg_parser.add_argument("--port", type=int, \
        help="Port of sillystream server")
    arg_parser.add_argument('--daemon', "-d", action='store_true', \
        help="Start as a daemon")
    arg_parser.set_defaults(daemon=False)
    initial = vars(arg_parser.parse_args())
    args = {}
    for arg in initial:
        if initial[arg] is not None:
            args[arg] = initial[arg]
    return args

def main():
    """
    Connects and sends input to server ctrl-d to stop
    """
    args = arg_setup()
    # Work in background
    if args["daemon"]:
        make_daemon()
    # Client connect doesn't take this argument
    del args["daemon"]
    # Create the client
    test = on_recv()
    # Connect the client, default host is localhost
    test.connect(**args)
    # Listen unitl killed
    while True:
        time.sleep(300)

if __name__ == '__main__':
    main()
