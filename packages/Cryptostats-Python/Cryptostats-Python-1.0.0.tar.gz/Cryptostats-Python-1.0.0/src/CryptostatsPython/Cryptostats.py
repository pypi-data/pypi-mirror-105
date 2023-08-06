import logging
import threading
import websocket
import ujson as json
from urllib.parse import quote


class Cryptostats():

    def __init__(self, api_key, channels, on_open, on_message, on_error, on_close):
        subscription = {
            'action': 'subscribe',
            'api_key': api_key,
            'channel': channels
        }
        self.ws = None
        self.payload = quote(json.dumps(subscription))
        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close

        self.connect()

    def connect(self):
        wst = threading.Thread(target=self.run)
        wst.daemon = True
        wst.start()

    def run(self):
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(f'wss://pro.cryptostats.dev:8443?options={self.payload}',
                                         on_open=self.on_open,
                                         on_message=self.decode,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()

    def decode(self, _, msg):
        self.on_message(json.decode(msg))

    def send(self, action, channel):
        self.ws.send(json.dumps({'action': action, 'channel': channel}))

    def subscribe(self, channel):
        logging.info("Subscribing to: " + channel)
        self.send("subscribe", channel)

    def unsubscribe(self, channel):
        logging.info("Unsubscribing from: " + channel)
        self.send("unsubscribe", channel)
