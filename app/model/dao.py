import mongoengine
from model.model import *
from utils.utils import genToken

class UserDAO:
    @classmethod
    def authorize(cls, username, password) -> User | None:
        results = User.objects(username=username, password=password)
        if len(results) == 0:
            return None

        return User.objects(username=username).first()

    @classmethod
    def createSession(cls, username, password, address) -> Session | None:
        user: User | None = User.objects(username=username, password=password).first()
        if user is None:
            return None
        
        try:
            return user.sessions.get(address=address)
        except mongoengine.errors.DoesNotExist:
            session = Session(token=genToken(20), address=address)
            user.sessions.append(session)
            user.save()
            return session


class MediaDAO:
    @classmethod
    def getAllMedia(cls):
        return Media.objects() # type: ignore

    @classmethod
    def getFromSearch(cls, search):
        return Media.objects(title__icontains=search)
    
    @classmethod
    def getVideoSrc(cls, mediaId):
        return Media.objects(mediaId=mediaId).first().src
    
    @classmethod
    def getFull(cls, id, cookie):
        user = User.objects(sessions__token=cookie).first()
        if user is None:
            print("no user")
            return Media.objects(mediaId=id).first()
        
        media = None
        for watched in user.watched:
            if watched.media.mediaId == id:
                media = watched.media
                media.timeWatched = watched.time
                break

        if media is None:
            media = Media.objects(mediaId=id).first()

        return media
    
    @classmethod
    def getWatchedTime(cls, id, token):
        user = User.objects(sessions__token=token).first()
        if user is None:
            return 0.0
        for w in user.watched:
            if w.media.mediaId == id:
                return w.time
        return 0.0
    
    @classmethod
    def updateWatchTime(cls, media_id, time, token):
        time = min(1.0, max(0.0, time))

        user: User = User.objects(sessions__token=token).first()
        
        if user is None:
            return False
        
        media = user.watched.filter(mediaId=media_id).first()

        if not media:
            watchSession = cls.createWatchSession(media_id, time)
            user.watched.append(watchSession)
            user.save()
            return True
        
        media.time = time
        user.save()
        
        return True
    
    @classmethod
    def createWatchSession(cls, media_id, time):
        media = Media.objects(mediaId=media_id).first()
        return WatchSession(media=media, time=time)


class SessionDAO:
    @classmethod
    def exists(cls, cookie):
        if cookie == None:
            return False
        return len(User.objects(sessions__token=cookie)) > 0

    @classmethod
    def delete(cls, cookie):
        user = User.objects(sessions__token=cookie).first()
        if user is None:
            return
        sessions = []
        for s in user.sessions:
            if s.token != cookie:
                sessions.append(s)
        user.sessions = sessions
        user.save()
        



