import asyncio
import datetime
import tornado.ioloop
import tornado.web
import socketio
import os

sio = socketio.AsyncServer(async_mode='tornado',cors_allowed_origins='*')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!!")

def make_app():
    return tornado.web.Application([
        # (r"/", MainHandler),
        (r"/socket.io/", socketio.get_tornado_handler(sio)),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join( os.getcwd(), "dist") , "default_filename": "index.html" })
    ])

async def send_events():
    count = 1
    while True:
        # print(datetime.datetime.now())
        msg = "Default Message: " + str(count) + "\n"
        msg1 = "Message1: " + str(count) + "\n"
        msg2 = "Message2: " + str(count) + "\n"
        json_date = { "name": "CurrentDate", "data": str( datetime.datetime.now() ) + "\n" }
        json_msg1 = { "name": "Message1", "data": msg1 }
        json_msg2 = { "name": "Message2", "data": msg2 }
        await sio.emit("data", msg )
        await sio.emit("data", json_date)
        await sio.emit("data", json_msg1)
        await sio.emit("data", json_msg2)
        await asyncio.sleep(1)
        count += 1

async def start_tornado():
    app = make_app()
    app.listen(3000)

async def main():
    await start_tornado()
    await asyncio.create_task(send_events())

asyncio.run(main())