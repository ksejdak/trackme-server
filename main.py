import sys
from Utils.Logger import Logger

from Server.ServerCore import ServerCore

def main(argv = None):
	if(argv is None):
		argv = sys.argv
	
	Logger.initLogger()
	log = Logger.getLogger()
	
	if(len(argv) != 3):
		log.error("IP, port or server name not specified!")
		log.info("usage: TrackMe-Server <IP> <Port>")
		return 1
		
	server = ServerCore()
	serverIP = argv[1]
	serverPort = int(argv[2])
	try:
		server.start(serverIP, serverPort)
	except IOError:
		log.error("TrackMe-Server terminated")
	except KeyboardInterrupt:
		log.info("TrackMe-Server terminated")

if __name__ == '__main__':
	sys.exit(main())