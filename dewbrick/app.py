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

    # TODO: Populate card lists from API backend

    cards_p1 = [
        {
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
        },
        {
            'id': 'card_2',
            'name': 'Card Name 2',
            'image': None,
            'description': 'This is card 2',
            'attributes': [
                {'name': 'power', 'value': 90},
                {'name': 'strength', 'value': 10},
                {'name': 'speed', 'value': 80},
                {'name': 'agility', 'value': 30},
                {'name': 'smell', 'value': 2}
            ]
        }
    ]

    cards_p2 = [
        {
            'id': 'card_3',
            'name': 'Card Name 3',
            'image': None,
            'description': 'This is card 3',
            'attributes': [
                {'name': 'power', 'value': 1},
                {'name': 'strength', 'value': 180},
                {'name': 'speed', 'value': 90},
                {'name': 'agility', 'value': 30},
                {'name': 'smell', 'value': 9}
            ]
        },
        {
            'id': 'card_4',
            'name': 'Card Name 4',
            'image': None,
            'description': 'This is card 4',
            'attributes': [
                {'name': 'power', 'value': 980},
                {'name': 'strength', 'value': 110},
                {'name': 'speed', 'value': 890},
                {'name': 'agility', 'value': 10},
                {'name': 'smell', 'value': 222}
            ]
        }
    ]

    players = [
        {
            'player_id': 'abc',
            'player_name': 'Dave Lister',
        },
        {
            'player_id': 'cba',
            'player_name': 'Arnold Rimmer',
        }
    ]

    player_count = 0

    game_state = {
        'turn_no': 0,
        'player_turn': None,
    }

    def check_origin(self, origin):
        return True

    def open(self):
        handlers.append(self)
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(json.dumps(DEMO_TURN))

    def on_close(self):
        print("WebSocket closed")

    def init_game(self):
        # TODO: Assign players to connecting clients
        # and let the games begin!
        pass


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
