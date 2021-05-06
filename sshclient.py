

import sys
import os
from queue import Queue
from queue import Empty
from threading import Thread
from threading import RLock
#from threading import Event
import getopt
import logging
import paramiko
import csv
import argparse
from getpass import getpass

import asyncio
import datetime
import tornado.ioloop
import tornado.web
import socketio


# Lock and error log, to keep track of all the devices that never succeeded.
error_log_lock = RLock()
error_log = {}

# Static variables that are used in comparisons to avoid excessive hardcoding of strings in the program.
CONNECTION_ERROR_MSG = "CONNECTION ERROR"
TASK_NOT_EXECUTED_MSG = "TASK HAS NOT BEEN EXECUTED YET"



############################# TORNADO WEB & SOCKET.IO ##########################################

sio = socketio.AsyncServer(async_mode='tornado',cors_allowed_origins='*')

class MainHandler(tornado.web.RequestHandler):
     def set_default_headers(self):
          self.set_header("Access-Control-Allow-Origin", "*")     

     def get(self):
          self.write("Hello, world!!!!")

     def post(self):
          data = tornado.escape.json_decode(self.request.body)     
          self.write(data)
          print("POST:\n",data)

def make_app():
    return tornado.web.Application([
        (r"/submit", MainHandler),
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
     #    print(datetime.datetime.now(), qweb_out.get())
        json = qweb_out.get()
        print("#############################",json["name"])
        await sio.emit( "data", json )
        await sio.emit("data", msg )
        await sio.emit("data", json_date)
        await sio.emit("data", json_msg1)
        await sio.emit("data", json_msg2)
        await asyncio.sleep(1)
        count += 1

async def send_sockets():
    while True:
          await asyncio.sleep(1)
          try:
               json = qweb_out.get(False)
               print("#############################",json["name"])
               await sio.emit( "data", json )
          except Empty:
               pass   

async def wait_forever():
    while True:
        await asyncio.sleep(1)

async def start_tornado():
    app = make_app()
    app.listen(3000)

async def main():
    await start_tornado()
    await asyncio.create_task(send_events())



############################## START OF SSH TASK ITEM ##########################################
# This represents a task item in a queue.  In this case an SSH task item.  But it is possible
# to create another telnet class item, for example, that uses these methods and can also be
# transparently placed in the threading pool queue to work seamlessly with this program.

class SSHTask(object):
     def __init__(self, qweb_out = None, ip = "127.0.0.1", hostname = "localhost", username = "admin", password = "NOPASSWORD", commands = "show version", port = 22, file = None):
          self.qweb_out = qweb_out
          self.ip = ip
          self.hostname = hostname
          self.username = username
          self.password = password
          self.commands = commands
          self.port = port
          self.result = TASK_NOT_EXECUTED_MSG
          self.timesExecuted = 0
          self.outputFile = file

     def doTask(self):
          try:
               self.timesExecuted += 1
               p = paramiko.SSHClient()
               p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
               p.connect(self.ip, port=self.port, username=self.username, password=self.password, timeout=10, allow_agent=False, look_for_keys=False, banner_timeout=args.banner_timeout)
               stdin, stdout, stderr = p.exec_command(self.commands)
               self.result = stdout.readlines()
               self.result = "".join(self.result)
               self.qweb_out.put( { "name": self.hostname, "data": self.result } )
               # loop.run_until_complete( sio.emit("data", { "name": "SSH", "data": data }) )
               logging.debug("Successfully connected to %s." % self.ip)
               return True
          except KeyboardInterrupt as e:
               exit
          except Exception as e:
               logging.warn("Error occurred while trying to connect to %s (%s). Error: %s" % (self.ip, self.hostname, e))
               self.result = CONNECTION_ERROR_MSG
               return False

     def getTimesExecuted(self):
          return self.timesExecuted

     def getResults(self):
          return self.result

     def getFile(self):
          return self.outputFile if self.outputFile else self.hostname+".txt"

     def resultsToString(self):
          return "Device %s (%s): %s" % (self.hostname, self.ip, self.result)

     def isSuccessful(self):
          if self.result == CONNECTION_ERROR_MSG:
            return False
          else:
            return True

     def getIP(self):
          return self.ip

     def getCommands(self):
          return self.commands



############################## END OF SSH TASK ITEM ##########################################


# This contains the name of SSH thread, but it is really a protocol independent thread instance
# that can be instantiated as many times as needed.
def ssh_thread(clientQueue, error_log_lock):
     global error_log
     while True:
          try:
                myTaskItem=clientQueue.get()
                logging.debug("Pulled item %s out of queue. %s items remaining in queue." % (myTaskItem.getIP(),str(clientQueue.qsize())))
                if (myTaskItem.doTask()):
                    if not args.quiet:
                         print(myTaskItem.resultsToString())
                    if args.save and myTaskItem.isSuccessful():
                         with open(myTaskItem.getFile(), 'w') as f:
                              f.write(myTaskItem.getResults())
                else:
                    if (myTaskItem.getTimesExecuted() < int(args.retries)):
                         logging.warn("Task has not met the required number of retries...requeuing.  At retry %s of %s" % (myTaskItem.getTimesExecuted(),args.retries))
                         clientQueue.put(myTaskItem, True)
                    else:
                         logging.warn("Final attempt was unsuccessful on %s." % (myTaskItem.getIP()))
                         error_log_lock.acquire()
                         try:
                              if myTaskItem.getIP() not in error_log.keys():
                                   error_log[myTaskItem.getIP()] = []
                              error_log[myTaskItem.getIP()].append(myTaskItem.getCommands())
                         finally:
                              error_log_lock.release()
          except KeyboardInterupt:
                logging.critical("Keyboard interrupt occurred on thread, quitting!")
          except Exception as ex:
                logging.exception("TASK MAY HAVE BEEN IMPROPERLY HANDLED: " + str(ex) + " ---- " + str(sys.exc_info()[0]))
          clientQueue.task_done()


# Allows retrieval of usernames and passwords from raw-input.
def get_user_pass():
  #Works in Python 2 and 3:
  try: input = raw_input
  except NameError: pass
  username = input("Username: ")
  password = getpass('Password: ')
  return username, password



async def sshclient():

     localuser = None
     localpass = None

     # Create work queue and log buffer.  These should be global to work
     q = Queue(maxsize=int(args.queue_size))
     
     # Check to see if authentication was provided to overide input file.
     if args.auth :
          localuser,localpass = get_user_pass()


     logging.info("Starting queue %s threads." % args.threads)
     for i in range(int(args.threads)): 
          worker = Thread(target=ssh_thread, args=(q, error_log_lock,), name="QueueWorker#"+str(i))
          worker.daemon = True
          worker.start()


     logging.info("Creating tasks and populating worker queue.")
     with open(filename) as csvfile:
          reader = csv.DictReader(csvfile, restkey="extra")
          for row in reader:
               ExtractedIP = row['ip']
               ExtractedHostname = row['hostname']
               ExtractedPort     = int(row['port']) if "port" in row  else 22
               ExtractedUsername = localuser if localuser else row['username']
               ExtractedPassword = localpass if localpass else row['password']
               ExtractedCommand  = row['command'] if 'extra' not in row else row['command']+","+",".join(row['extra'])
               ExtractedFile     = row['file'] if 'file' in row else row['hostname']+".txt"

               #print(command)
               q.put(SSHTask(qweb_out = qweb_out, ip = ExtractedIP, hostname = ExtractedHostname, username = ExtractedUsername, password = ExtractedPassword, commands = ExtractedCommand, port = ExtractedPort, file = ExtractedFile),True)


     # Halt program termination until the queue is empty.
     try:
          q.join()
     except Exception as ex:
          logging.exception("Could not gracefully clear out SSH queue!")
     print("---------Problem Devices---------")
     for key in error_log.keys():
          print(" "+str(key))
          for item in error_log[key]:
               print(" --"+str(item))
          print("")

async def main():
     await start_tornado()
     await asyncio.create_task(sshclient())
     await asyncio.create_task(send_sockets())
     # await asyncio.create_task(wait_forever())


##################################################### START OF MAIN METHOD #############################################################
# Setup initial logging.
logging.basicConfig(level=logging.WARN, format='%(asctime)s UTC %(levelname)s %(module)s(%(funcName)s) [%(process)d-%(thread)d-%(threadName)s]: %(message)s')
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s UTC %(levelname)s %(module)s(%(funcName)s) [%(process)d-%(thread)d-%(threadName)s]: %(message)s')

# The parser allows for program parameters to change.
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Specify the CSV file for SSH connectivity. Default is hosts.csv in current directory', nargs='?', default="hosts.csv")
parser.add_argument('-t', '--threads', help='Specify the number of concurrent SSH threads to run.', nargs='?', default=os.getenv("THREADS", 20))
parser.add_argument('-m', '--queue_size', help='Specify the maximum SSH queue size.', nargs='?', default=os.getenv("QUEUE_SIZE", 100000))
parser.add_argument('-r', '--retries', help='Specify the maximum number of SSH retry attempts.', nargs='?', default=os.getenv("RETRIES", 1))
parser.add_argument('-b', '--banner_timeout', help='Specify the SSH banner timeout in seconds.', nargs='?', default=os.getenv("BANNER_TIMEOUT", 10))
parser.add_argument('-a', '--auth', help='Ask for usuername/password and use that for SSH authentication instead of provided credentials in the CSV file', action='store_true')
parser.add_argument('-q', '--quiet', help='Do not display results', action='store_true')
parser.add_argument('-s', '--save', help='Save results to output file as hostname.txt', action='store_true')
args = parser.parse_args()
filename = args.file
qweb_out = Queue()

asyncio.run(main())