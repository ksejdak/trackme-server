from threading import Thread
import thread
from ServerDatabase import ServerDatabase
from Utils.Logger import Logger
from Utils.MessageParser import MessageParser

class ClientThread(Thread):
	
	def __init__(self, socket, clientId):
		super(ClientThread, self).__init__()
		
		self.__name = clientId
		self.__log = Logger.getLogger()
		self.__socket = socket
		self.__messageParser = MessageParser()
		self.__database = ServerDatabase()
		
		self.__log.debug("Creating client thread [%s]", self.__name)
		
		# create functions mapping
		self.__handlers = {
			"setLocation": self.__setLocation,
			"getLocation": self.__getLocation,
			"allowTracking": self.__allowTracking,
			"invalid": self.__invalidMessage
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
		self.__database.setLocation(data["userId"], data["longtitude"], data["latitude"])
		self.__log.info("SET -- userId: [" + data["userId"] + "], X: [" + data["longtitude"] + "], Y: [" + data["latitude"] + "]")
	
	def __getLocation(self):
		self.__log.debug("__getLocation called")
		data = self.__messageParser.getData()
		location = self.__database.getLocation(data["userId"], data["whoseId"])
		self.__socket.send(location["longtitude"] + ":" + location["latitude"] + "\n")
		self.__log.info("GET -- userId: [" + data["userId"] + "], whoseId: [" + data["whoseId"] + "]")
	
	def __allowTracking(self):
		self.__log.debug("__allowTracking called")
		data = self.__messageParser.getData()
		self.__database.allowTracking(data["userId"], data["viewerId"])
		self.__log.info("ALLOW -- userId: [" + data["userId"] + "], viewerId: [" + data["viewerId"] + "]")
		
	def __invalidMessage(self):
		self.__log.debug("__invalidMessage called")
		data = self.__messageParser.getData()
		self.__log.error("invalid message received: [" + data["message"] + "]")