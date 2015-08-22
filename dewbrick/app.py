#!/usr/bin/env python3

import json
import tornado.ioloop
import tornado.web
from tornado.websocket import WebSocketHandler
from tornado import template

DEMO_TURN = {
    'player_id': 'abc',
    'player_name': 'Dave Lister',
    'opponent_name': 'Arnold Rimmer',
    'player_turn': 1,
    'card': {
        'id': 'card_1',
        'name': 'Card Name',
        'image': None,
        'description': 'This is a card',
        'attributes': [

            {'name': 'power', 'value': 9001},
            {'name': 'strength', 'value': 100},
            {'name': 'speed', 'value': 50},
            {'name': 'agility', 'value': 20},
            {'name': 'smell', 'value': 4}
        ]
    }
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(application.template_loader.load(
            "index.html").generate(turn=DEMO_TURN))


class SocketHandler(WebSocketHandler):

    wesisright = {
        "turn": "1"
    }

    handlers = []

    def check_origin(self, origin):
        return True

    def open(self):
        handlers.append(self)
        print("WebSocket opened")

    def on_message(self, message):
        self.wesisright['turn'] = "2"
        self.write_message(json.dumps(DEMO_TURN))
        #self.write(json.dumps(DEMO_TURN))

    def on_close(self):
        print("WebSocket closed")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/sockets", SocketHandler),
    (r"/content/(.*)", tornado.web.StaticFileHandler,
        {"path": "static"})
], debug=True)


def main():
    application.listen(8888)
    application.template_loader = template.Loader("templates")

    print('Starting app on port 8888..')
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
