from Utils.Logger import Logger
from ConnectionListener import ConnectionListener

class ServerCore(object):

	def start(self, serverIP, serverPort):
		# start logging
		log = Logger.getLogger()
		log.info("Starting TrackMe-Server...")
		
		# start listening for incomming messages
		listener = ConnectionListener()
		listener.listen(serverIP, serverPort)