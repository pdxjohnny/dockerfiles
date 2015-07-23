#! /usr/bin/env python
import sys
import ssl
import thread
import argparse
import itertools

import irc.client

__connection__ = False
"The conenction to the irc server"
__target__ = None
"The nick or channel to which to send messages"

def write(message):
    if __connection__ is not False:
        __connection__.privmsg(__target__, message)
        return True
    return False

def stop():
    if __connection__:
        __connection__.quit("Using python irc.client")

def on_connect(connection, event):
    global __connection__
    __connection__ = connection
    if irc.client.is_channel(__target__):
        connection.join(__target__)
        return

def on_disconnect(connection, event):
    global __connection__
    __connection__ = False

def start(args):
    global __target__

    __target__ = args["target"]

    ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
    reactor = irc.client.Reactor()
    try:
        c = reactor.server().connect(
            args["host"],
            args["port"],
            args["nickname"],
            connect_factory=ssl_factory,
        )
    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("disconnect", on_disconnect)

    thread.start_new_thread(reactor.process_forever, tuple())
    return True

def main():
    args = {
        "host": "irc.freenode.com",
        "port": 6697,
        "nickname": "testbot",
        "target": "#target",
    }
    start(args)
    send = raw_input(":")
    while send != "exit":
        send = raw_input(":")
        write(send)
    stop()

if __name__ == '__main__':
    main()
