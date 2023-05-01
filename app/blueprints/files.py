from flask import Blueprint, abort, send_file
from model.dao import VideoDAO

videoDAO = VideoDAO()
file_handler = Blueprint(name="file_handler", import_name=__name__)

@file_handler.get('/', defaults={'file':'index.html'})
@file_handler.get('/<path:file>')
def send_files(file):
    try:
        return send_file(f'webapp/static/{file}')
    except FileNotFoundError:
        return abort(404)

@file_handler.get("/video/<string:video_id>")
def send_video(video_id): 
    try:
        path = videoDAO.get_video_src(video_id)
        if path == "": raise FileNotFoundError
        return send_file(path)
    except FileNotFoundError:
        return abort(404)