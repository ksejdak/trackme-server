import os
import sqlite3
from Utils.Settings import RESOURCE_PATH, SERVER_DB_FILE
from Utils.Logger import Logger

class ServerDatabase(object):
	def __init__(self):
		self.__dbName = RESOURCE_PATH + SERVER_DB_FILE
		self.__log = Logger.getLogger()

		# check if database file exists
		if(os.path.exists(self.__dbName) == False):
			self.__log.debug("DB file doesn't exists, creating...")
		
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		# check if tables exist within database
		c.execute("CREATE TABLE IF NOT EXISTS UserLocation (userId VARCHAR(30), longtitude VARCHAR(30), latitude VARCHAR(30))")
		c.execute("CREATE TABLE IF NOT EXISTS TrackingPermission (userId VARCHAR(30), viewerId VARCHAR(30))")
		c.execute("CREATE TABLE IF NOT EXISTS User (userId VARCHAR(30), password VARCHAR(30))")
		
		dbConnection.close()
		
	def setLocation(self, userId, longtitude, latitude):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		# delete previous user location
		values = (userId,)
		c.execute("DELETE FROM UserLocation WHERE userId = ?", values)
		
		# insert new user location
		values = (userId, longtitude, latitude)
		c.execute("INSERT INTO UserLocation VALUES (?, ?, ?)", values)
		
		dbConnection.commit()
		dbConnection.close()
	
	def getLocation(self, userId, whoseId):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		location = {}
		values = (whoseId, userId)
		c.execute("SELECT * FROM TrackingPermission WHERE userId = ? AND viewerId = ?", values)
		permission = c.fetchone()
		
		# if tracking for this user is not allowed
		if(permission is None):
			location["longtitude"] = ""
			location["latitude"] = ""
		else:
			values = (whoseId,)
			c.execute("SELECT * FROM UserLocation WHERE userId = ?", values)
			userLocation = c.fetchone()
			
			# if location is not set
			if(userLocation is None):
				location["longtitude"] = ""
				location["latitude"] = ""
			else:
				location["longtitude"] = userLocation[1]
				location["latitude"] = userLocation[2]
		
		dbConnection.close()
		return location

	def allowTracking(self, userId, viewerId):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		# delete previous user permission
		values = (userId,)
		c.execute("DELETE FROM TrackingPermission WHERE userId = ?", values)
		
		# insert new user permission
		values = (userId, viewerId)
		c.execute("INSERT INTO TrackingPermission VALUES (?, ?)", values)
		
		dbConnection.commit()
		dbConnection.close()
	
	def registerUser(self, userId, password):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		# delete previous user permission
		values = (userId,)
		c.execute("SELECT * FROM User WHERE userId = ?", values)
		user = c.fetchone()
		if(user is None):
			# insert new user login and password
			values = (userId, password)
			c.execute("INSERT INTO User VALUES (?, ?)", values)
		
		dbConnection.commit()
		dbConnection.close()
		
	def loginUser(self, userId, password):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		# delete previous user permission
		values = (userId,)
		c.execute("SELECT * FROM User WHERE userId = ?", values)
		user = c.fetchone()
		dbConnection.commit()
		dbConnection.close()
		
		if(user is None):
			return False
		
		if(user[1] == password):
			return True
		else:
			return False
		
	def checkPermission(self, userId, viewerId):
		dbConnection = sqlite3.connect(self.__dbName)  # @UndefinedVariable
		c = dbConnection.cursor()
		
		# delete previous user permission
		values = (userId, viewerId)
		c.execute("SELECT * FROM TrackingPermission WHERE userId = ? AND viewerId = ?", values)
		user = c.fetchone()
		dbConnection.commit()
		dbConnection.close()
		
		if(user is None):
			return False
		else:
			return True