#!/usr/bin/env python

import sys
import datetime
from time import strftime, localtime
from json import loads, dumps

from websockets.sync.client import connect

server = input("server [wss://relay.snort.social]: ") or "wss://relay.snort.social"
author = input("users pubkey: ") or None

mins = input("minutes [15]: ") or 15

start_point = datetime.datetime.now() - datetime.timedelta(minutes=int(mins))
start_point = int(start_point.timestamp())


def get(since=start_point, author=author):
    with connect("wss://relay.snort.social") as websocket:

        payload = ["REQ", "0", {"since": since}]

        if author:
             payload[2]['authors'] = [author]

        payload = dumps(payload)

        websocket.send(payload)

        while True:
            raw_return = websocket.recv()

            if raw_return == '["EOSE","0"]':
                break

            message = loads(raw_return)[2]

            _id = message['id']
            user = message['pubkey']
            content = message['content']
            created = strftime('%Y-%m-%d %H:%M:%S', localtime(message['created_at']))

            print(f"[{created}][{user}]\n {content}\n\n")

def send():
        with connect("wss://relay.snort.social") as websocket:
            payload = input("payload: ")
            websocket.send(payload)
            print(websocket.recv())

get()
