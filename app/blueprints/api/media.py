from flask import Blueprint, request, abort
from model.dao import MediaDAO, SessionDAO
from model.dto import MediaDTO
from utils.utils import require_auth, handle_null
import config

Media = Blueprint("media", __name__)


def _auth():
    cookie = request.cookies.get(config.SESSION_NAME)
    if SessionDAO.exists(cookie):
        return True, None
    else:
        return False, {"status": "Failed", "reason": "No auth method find"}


@Media.get("/")
@require_auth(_auth)
def all_media():
    media = []
    if request.args.get("search") is None:
        
        media = [MediaDTO(media=m).to_dict() for m in MediaDAO.getAllMedia()]
    else:
        search = request.args["search"]
        media = [MediaDTO(media=m).to_dict() for m in MediaDAO.getFromSearch(search)]
    return media


@Media.get("/<string:id>")
@require_auth(_auth)
def send_media(id):
    cookie = request.cookies.get(config.SESSION_NAME)
    res = MediaDAO.getFull(id, cookie)
    if res is None:
        return []
    return MediaDTO(res).to_dict()


@Media.get("/watched/<string:id>")
@require_auth(_auth)
def send_watched_time(_id):
    token = request.cookies.get(config.SESSION_NAME)
    res = MediaDAO.getWatchedTime(_id, token)
    if res is None:
        return []
    return MediaDTO(res).to_dict()


@Media.put("/watched")
def update_watched_time():
    _id = request.form.get('id')
    time = request.form.get('time')
    token = request.cookies.get(config.SESSION_NAME)

    if token is None:
        return ({'message':'No autorizado'}, 401)

    if _id is None or time is None:
        return ({'message':'No hay suficientes argumentos'}, 400)
    
    time = float(time)
    if MediaDAO.updateWatchTime(_id, time, token):
        return ({'message':'Actualización exitosa'}, 200)
    else:
        return ({'message':'Actualización fallida'}, 400)




