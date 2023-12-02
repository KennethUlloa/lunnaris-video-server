import mongoengine as m

class Genre:
    ACTION = "Acción"
    COMEDY = "Comedia"
    SCIFI = "Ciencia Ficción"
    FANTASY = "Fantasía"
    TERROR = "Terror"
    ADVENTURE = "Aventura"
    DRAMA = "Drama"
    ROMANCE = "Romance"

class UserType:
    ADMIN = "admin"
    USER = "user"

class MediaType:
    SERIE = "serie"
    MOVIE = "película"

class Session(m.EmbeddedDocument):
    token = m.StringField(required=True)
    address = m.StringField(required=True)


class Media(m.Document):
    mediaId = m.StringField()
    title = m.StringField()
    poster = m.StringField()
    synopsis = m.StringField()
    year = m.IntField()
    genres = m.ListField(m.StringField())
    src = m.StringField()
    thumb = m.StringField()
    mediaType = m.StringField()
    timeWatched = 0.0


class WatchSession(m.EmbeddedDocument):
    media = m.ReferenceField(Media, unique=True)
    mediaId = m.StringField()
    time = m.FloatField()


class User(m.Document):
    username = m.StringField(required=True, unique=True)
    password = m.StringField(required=True)
    displayName = m.StringField(required=True)
    sessions = m.EmbeddedDocumentListField(Session)
    watched = m.EmbeddedDocumentListField(WatchSession)
    userType = m.StringField(required=True)

