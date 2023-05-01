from abc import ABC, abstractmethod

class Dictionable(ABC):
    @abstractmethod
    def to_dict(self):
        pass

class Session(Dictionable):
    def __init__(self, token: str, address: str) -> None:
        self.token = token
        self.address = address
    def to_dict(self):
        return {"token": self.token, "address": self.address}
    
    @classmethod
    def load(cls, source: dict):
        return Session(source["token"], source["address"])

    @classmethod
    def load_multiple(cls, source: list[dict]):
        return [cls.load(s) for s in source]

class User(Dictionable):
    def __init__(self, username: str, password: str, display_name: str, sessions: list[Session] = []):
        self.username = username
        self.password = password
        self.display_name = display_name
        self.sessions = sessions
    
    def to_dict(self):
        return {"username":self.username, 
                "password":self.password, 
                "display_name":self.display_name,
                "sessions": [s.to_dict() for s in self.sessions]  }

    @classmethod
    def load(cls, source: dict):
        return User(source["username"], source["password"], source["display_name"], Session.load_multiple(source["sessions"]))

    @classmethod
    def load_multiple(cls, source: list[dict]):
        return [cls.load(s) for s in source]



class VideoMedia:
    def __init__(self, id: str, title: str, desc: str, poster: str, img: str, year: str, genres: str, src: str) -> None:
        self.id = id
        self.title = title
        self.desc = desc
        self.poster = poster
        self.img = img
        self.year = year
        self.genres = genres
        self.src = src

class WatchedMedia:
    def __init__(self, percent: float, media: VideoMedia) -> None:
        self.percent = percent
        self.media = media

class Movie(VideoMedia):
    def __init__(self, id: str, title: str, desc: str, poster: str, img: str, year: str, genres: str, src: str) -> None:
        super().__init__(id, title, desc, poster, img, year, genres, src)

class Episode(VideoMedia):
    def __init__(self, id: str, title: str, desc: str, poster: str, img: str, year: str, genres: str, src: str, episode: int, season: int) -> None:
        super().__init__(id, title, desc, poster, img, year, genres, src)
        self.episode = episode
        self.season = season

class Serie(VideoMedia):
    def __init__(self, id: str, title: str, desc: str, poster: str, img: str, year: str, genres: str, src: str, episodes: list[Episode]) -> None:
        super().__init__(id, title, desc, poster, img, year, genres, src)
        self.episodes = episodes


