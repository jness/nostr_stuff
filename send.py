#!/usr/bin/env python

from websockets.sync.client import connect

server = input("server [wss://relay.snort.social]: ") or "wss://relay.snort.social"

def send():
        with connect(server) as websocket:
            payload = input("payload: ")
            websocket.send(payload)
            print(websocket.recv())

send()
