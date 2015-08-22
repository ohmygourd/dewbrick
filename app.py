import tornado.ioloop
import tornado.web
from tornado.websocket import WebSocketHandler
from tornado import template


class MainHandler(tornado.web.RequestHandler):

    DEMO_TURN = {
        'player_id': 'abc',
        'player_turn': 1,
        'card': {
            'id': 'card_1',
            'name': 'Card Name',
            'image': None,
            'description': 'This is a card',
            'attributes': {
                'power': 9001,
                'strength': 100,
                'speed': 50,
                'agility': 20,
                'smell': 4
            }
        }
    }

    def get(self):
        self.write(application.template_loader.load("index.html").generate(turn=self.DEMO_TURN))


class SocketHandler(WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/sockets", SocketHandler),
    (r"/content/(.*)", tornado.web.StaticFileHandler, {"path": "static"})
    #(r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    application.template_loader = template.Loader("templates")
    tornado.ioloop.IOLoop.current().start()