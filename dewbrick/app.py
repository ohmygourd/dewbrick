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


class MainHandlerP1(tornado.web.RequestHandler):
    def get(self):
        player_turn = True
        player_id = 'abc'
        player_name = 'Dave Lister'
        opponent_name = 'Arnold Rimmer'
        self.write(application.template_loader.load("index.html").generate(
            card=cards_p1[0],
            player_name=player_name,
            player_turn=player_turn,
            player_id=player_id,
            opponent_name=opponent_name
        ))


class MainHandlerP2(tornado.web.RequestHandler):
    def get(self):
        player_turn = False
        player_id = 'abc'
        opponent_name = 'Dave Lister'
        player_name = 'Arnold Rimmer'
        self.write(application.template_loader.load("index.html").generate(
            card=cards_p2[0],
            player_name=player_name,
            player_turn=player_turn,
            player_id=player_id,
            opponent_name=opponent_name
        ))



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

    handlers = []

    def check_origin(self, origin):
        return True

    def open(self):
        self.handlers.append(self)
        self.init_game()

        if self.player_count == 0:
            self.game_state['player_turn'] = 0
            #self.write_message(self.cards_p1[0])
        else:
            pass
            #self.write_message(self.cards_p2[1])

        print("WebSocket opened")

    def on_message(self, message):
        #self.write_message()json.dumps(DEMO_TURN))
        # get the message and break it up
        user_id, card_num, name = message.split('-')

        card1 = cards_p1[self.game_state['turn_no']]
        card2 = cards_p2[self.game_state['turn_no']]

        c1 = 0
        c2 = 0

        for values in card1['attributes']:
            if values['name'] == name:
                c1 = values['value']
                for values in card2['attributes']:
                    if values['name'] == name:
                        c2 = values['value']
                        break
        if c1 > c2:
            self.write_message("player 1 wins!")

        else:
            self.write_message("player 2 wins!")
        self.game_state['turn_no']

    def on_close(self):
        print("WebSocket closed")

    def init_game(self):
        # TODO: Assign players to connecting clients
        # and let the games begin!
        #self.player_count += 1
        pass


application = tornado.web.Application([
    (r"/p1", MainHandlerP1),
    (r"/p2", MainHandlerP2),
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
