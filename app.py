import tornado.ioloop
import tornado.web
from tornado.websocket import WebSocketHandler
from tornado import template


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(application.template_loader.load("index.html").generate(myvalue="XXX"))


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