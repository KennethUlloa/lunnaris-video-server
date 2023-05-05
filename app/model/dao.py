from model.db import DB
import model.model as m
from utils.utils import genToken

class UserDAO():

    def auth(self, username: str, password: str):
        conn = DB.get_connection()
        collection = conn['LunnarisDB']['users']
        user_data = collection.find_one({"username":username,"password":password})
        if user_data != None:
            return m.User.load(user_data)
        else:
            return None

    def get(self, **kwargs):
        conn = DB.get_connection()
        collection = conn['LunnarisDB']['users']
        if len(kwargs.keys()) == 0:
            user_data = collection.find()
            return m.User.load_multiple(list(user_data))
        elif "username" in kwargs.keys():
            user_data = collection.find_one({"username":kwargs["username"]})
            return m.User.load(user_data) if user_data != None else None  # type: ignore
    
    def register(self, **kwargs):
        user = kwargs["user"]
        if type(user) == m.User:
            collection = DB.get_connection()['LunnarisDB']['users']
            return collection.insert_one(user.to_dict()).acknowledged
        else:
            return False
        
    def update(self, **kwargs):
        user = kwargs["user"]
        if type(user) == m.User:
            collection = DB.get_connection()['LunnarisDB']['users']
            return collection.update_one({"username":user.username},{"$set":user.to_dict()}).acknowledged
        else:
            return False
    def delete(self, **kwargs):
        if "username" in kwargs:
            collection = DB.get_connection()['LunnarisDB']['users']
            return collection.delete_one({"username":kwargs["username"]}).acknowledged
        else:
            return False

class SessionDAO:

    def delete(self, token):
        collection = DB.get_connection()['LunnarisDB']['users']
        results = collection.update_one(filter={"sessions.token": token},
                update=[{
            "$addFields":
                {"sessions":{
                    "$filter":{
                        "input":"$sessions", 
                        "as": "session",
                        "cond": {"$ne":["$$session.token",token]}
                        }
                    }}}])


    def create(self, username: str, password: str, address: str):

        session = {
            "address": address,
            "token": genToken(10)
        }

        collection = DB.get_connection()['LunnarisDB']['users']
        results = collection.update_one(filter={"username":username,"password": password},
                update=[{
            "$addFields":
                {"sessions":{
                    "$filter":{
                        "input":"$sessions", 
                        "as": "session",
                        "cond": {"$ne":["$$session.address",session["address"]]}
                        }
                    }}},{
            "$addFields":
                {"sessions":{
                    "$concatArrays":["$sessions",[session]]}}}])
        
        if results.modified_count + results.matched_count == 0:
            return None
        
        return m.Session(token=session['token'], address=session['address'])

    def exists(self, token):
        if token == None: return False
        collection = DB.get_connection()['LunnarisDB']['users']
        return collection.find_one({"sessions.token":token},{"_id":1}) != None
        

class VideoDAO:
    def get_all(self):
        conn = DB.get_connection()['LunnarisDB']['media']
        media = conn.aggregate([{"$match":{"src":{"$regex":".*(.mp4)"}}},{"$project":{"_id":0,"src":0}}])
        return list(media)
    
    def get_full(self, id, token, default=None):
        collection = DB.get_connection()['LunnarisDB']['media']
        movie = collection.find_one({"id":id},projection={"_id":0, "src":0})
        if movie == None:
            return default
        movie = dict(movie)
        collection = DB.get_connection()['LunnarisDB']['users']
        watched = collection.find_one({"sessions.token":token},projection={"watched":{"$elemMatch":{"id":id}}, "_id":0})
        movie['time'] = 0.0 if (watched == None or len(watched) == 0) else watched['watched'][0]['time']
        
        return movie

    def update_time(self, id:str, time:float, token:str):
        collection = DB.get_connection()['LunnarisDB']['users']
        result = collection.update_one(filter={"sessions.token":token,"watched.id":id}, update={"$set":{"watched.$[watch].time":time}}, array_filters=[{"watch.id":{"$eq":id}}])
        if result.matched_count == 0:
            result = collection.update_one(filter={"sessions.token":token}, update={"$push":{"watched":{"id":id,"time":0.0}}})
        return result.modified_count > 0

    def get_video_src(self, id):
        collection = DB.get_connection()['LunnarisDB']['media']
        video = collection.find_one({"id":id}, projection={"_id":0, "src":1})
        if video != None: return video['src']
        else: return ""
    
    def get_watched_time(self, id, token):
        collection = DB.get_connection()['LunnarisDB']['users']
        video = collection.find_one({"sessions.token":token}, projection={"watched":{"$elemMatch":{"id":id}},"_id": 0})
        if video != None and video != {}:
            return video["watched"][0]
        
        return None

