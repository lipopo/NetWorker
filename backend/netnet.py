# -*- coding: utf8 -*-

import os
from functions import RemoteFunction

from tornado.web import RequestHandler, StaticFileHandler, Application
from tornado.websocket import WebSocketHandler
from tornado.gen import coroutine
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# index_app
class index_handler(RequestHandler):
    def get(self):
        self.render("index.html", remote_function_js="netnet/static/js/remote.js")

# websocket handler
class infoHandler(WebSocketHandler):
    def open(self):
        pass
    
    def on_message(self, message):
        pass
    
    def on_close(self):
        pass

class funcHandler(WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        print(message)
        msgs = message.split(" ")
        res = RemoteFunction.__dict__[msgs[0]](msgs[1:])
        self.write_message(res)

    def on_close(self):
        pass
    
    def check_origin(self, url):
        return True
# 主函数
def main():
    application = Application([
        # 主页
        (r"/", index_handler),
        # 信息通讯
        (r"/ws", infoHandler),
        # 远程执行函数
        (r"/func", funcHandler),
        # 静态文件
        (r"/(.*)", StaticFileHandler, {"path": os.path.realpath("./template")}),
    ],
    template_path=os.path.realpath("./template")
    )
    server = HTTPServer(application)
    server.listen(9108)

    try:
        # 开启事件循环
        IOLoop.current().start()
    except:
        # 关闭事件循环
        IOLoop.current().stop()

if __name__ == "__main__":
    main()