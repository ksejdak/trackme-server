from threading import Thread
import thread
from Utils.Logger import Logger
from Utils.MessageParser import MessageParser

class ClientThread(Thread):
	
	def __init__(self, socket, clientId):
		super(ClientThread, self).__init__()
		
		self.__name = clientId
		self.__log = Logger.getLogger()
		self.__socket = socket
		self.__messageParser = MessageParser()
		
		self.__log.debug("Creating client thread [%s]", self.__name)
		
		# create functions mapping
		self.__handlers = {
			"setLocation": self.__setLocation,
			"getLocation": self.__getLocation,
			"allowTracking": self.__allowTracking
		}
		
	def run(self):
		while(True):
			request = self.__socket.recv(512)
			if(request == ""):
				self.__log.debug("Connection closed in thread [%s]", self.__name)
				self.__log.debug("Exiting client thread [%s]", self.__name)
				self.__socket.close()
				thread.exit()

			requestType = self.__messageParser.parse(request)
			requestHandler = self.__handlers[requestType]
			requestHandler()
	
	def __setLocation(self):
		self.__log.debug("__setLocation called")
		data = self.__messageParser.getData()
		self.__log.info("user: [" + data["id"] + "], X:[" + data["longtitude"] + "], Y:[" + data["latitude"] + "]")
	
	def __getLocation(self):
		self.__log.debug("__getLocation called")
	
	def __allowTracking(self):
		self.__log.debug("__allowTracking called")