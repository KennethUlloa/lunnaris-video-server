from flask import Blueprint
from model.dao import VideoDAO

Media = Blueprint("media",__name__)
videoDAO = VideoDAO()
@Media.get("/")
def all_media():
    return videoDAO.get_all()

@Media.get("/<id>")
def send_media(id):
    return {"response": None}



