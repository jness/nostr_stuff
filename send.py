#!/usr/bin/env python

from websockets.sync.client import connect


def send():
        with connect("wss://relay.snort.social") as websocket:
            payload = input("payload: ")
            websocket.send(payload)
            print(websocket.recv())

send()
