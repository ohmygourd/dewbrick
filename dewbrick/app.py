#!/usr/bin/env python3

import json
import tornado.ioloop
import tornado.web
from tornado.websocket import WebSocketHandler
from tornado import template
from majesticapi import GameDataSet

data_set = GameDataSet(22)
cards_p1 = list(data_set.get(11))
cards_p2 = list(data_set.get(11))

game_state = {
    'turn_no': 1,
    'player_turn': None,
}


class MainHandlerP1(tornado.web.RequestHandler):
    def get(self):
        player_turn = True
        player_id = 'player1'
        player_name = 'Dave Lister'
        opponent_name = 'Arnold Rimmer'
        self.write(application.template_loader.load("index.html").generate(
            card=cards_p1[game_state['turn_no']],
            player_name=player_name,
            player_turn=player_turn,
            player_id=player_id,
            opponent_name=opponent_name
        ))


class MainHandlerP2(tornado.web.RequestHandler):
    def get(self):
        player_turn = False
        player_id = 'player2'
        opponent_name = 'Dave Lister'
        player_name = 'Arnold Rimmer'
        self.write(application.template_loader.load("index.html").generate(
            card=cards_p2[game_state['turn_no']],
            player_name=player_name,
            player_turn=player_turn,
            player_id=player_id,
            opponent_name=opponent_name
        ))



class SocketHandler(WebSocketHandler):

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

    handlers = []

    def check_origin(self, origin):
        return True

    def open(self):
        self.handlers.append(self)
        self.init_game()
        print("WebSocket opened")

    def on_message(self, message):
        #self.write_message()json.dumps(DEMO_TURN))
        # get the message and break it up
        user_id, name = message.split('-')

        card1 = cards_p1[game_state['turn_no']]
        card2 = cards_p2[game_state['turn_no']]

        c1 = 0
        c2 = 0

        for values in card1['attributes']:
            if values['name'] == name:
                c1 = values['value']
                for values in card2['attributes']:
                    if values['name'] == name:
                        c2 = values['value']
                        break

        for handle in self.handlers:
            if self is not handle:
                if game_state['turn_no'] % 2:
                    socket2 = handle

        if c1 > c2:
            self.write_message("you win player 1!")
            socket2.write_message("you lose player 2!")
        else:
            self.write_message("you lose player 1!")
            socket2.write_message("you win player 2!")
        pass

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
