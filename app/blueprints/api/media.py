from flask import Blueprint, request, abort
from model.dao import VideoDAO, SessionDAO
from utils.utils import require_auth, handle_null
import config

Media = Blueprint("media",__name__)
videos = VideoDAO()
sessions = SessionDAO()

def _auth():
    cookie = request.cookies.get(config.SESSION_NAME)
    if sessions.exists(cookie):
        return True, None
    else:
        return False, {"status": "Failed", "reason": "No auth method find"}


@Media.get("/")
@require_auth(_auth)
def all_media():
    return videos.get_all()

@Media.get("/<string:id>")
@require_auth(_auth)
def send_media(id):
    cookie=request.cookies.get(config.SESSION_NAME)
    res = videos.get_full(id, cookie)
    if res == None: return []
    return res

@Media.get("/watched/<string:id>")
@require_auth(_auth)
def send_watched_time(id):
    token = request.cookies.get(config.SESSION_NAME)
    res = videos.get_watched_time(id, token)
    if res == None: return []
    return res


@Media.put("/watched")
def update_watched_time():
    id = request.form.get('id')
    time = request.form.get('time')
    token = request.cookies.get(config.SESSION_NAME)

    if token == None:
        return ({'message':'No autorizado'}, 401)

    if id == None or time == None: 
        return ({'message':'No hay suficientes argumentos'}, 400)
    
    time = float(time)
    if videos.update_time(id, time, token):
        return ({'message':'Actualización exitosa'}, 200)
    else:
        return ({'message':'Actualización fallida'}, 400)




