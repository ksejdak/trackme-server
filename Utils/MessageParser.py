import string

class MessageParser(object):

	def __init__(self):
		self.__data = {}
	
	def parse(self, message):
		message = message.rstrip()
		words = string.split(message, ":")
		
		if(words[0] == "SET_LOCATION"):
			self.__data.clear()
			self.__data["userId"] = words[1]
			self.__data["longtitude"] = words[2]
			self.__data["latitude"] = words[3]
			return "setLocation"
		elif(words[0] == "GET_LOCATION"):
			self.__data.clear()
			self.__data["userId"] = words[1]
			self.__data["whoseId"] = words[2]
			return "getLocation"
		elif(words[0] == "ALLOW_TRACKING"):
			self.__data.clear()
			self.__data["userId"] = words[1]
			self.__data["viewerId"] = words[2]
			return "allowTracking"
		else:
			self.__data.clear()
			self.__data["message"] = message
			return "invalid"
	
	def getData(self):
		return self.__data