import pymongo as mg
class DB:
    connection = None
    @classmethod
    def get_connection(cls):
        if cls.connection == None:
            cls.connection = mg.MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=1000)
        return cls.connection
    @classmethod
    def close(cls):
        if cls.connection != None:
            cls.connection.close()
            cls.connection = None
            print("First close")