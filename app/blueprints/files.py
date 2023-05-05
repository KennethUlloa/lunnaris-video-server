from flask import Blueprint, abort, send_file, request, redirect
from model.dao import VideoDAO
import config
from blueprints.wrappers import _auth

videoDAO = VideoDAO()
file_handler = Blueprint(name="file_handler", import_name=__name__)


@file_handler.get('/', defaults={'file':'index.html'})
@file_handler.get('/login', defaults={'file':'login.html','path': config.TEMPLATES_FOLDER})
@file_handler.get('/<path:file>')
def send_files(file, path = config.STATIC_FOLDER):
    #If cookie doesn't exits
    if request.cookies.get(config.SESSION_NAME) is None:
        if file in ['index.html']:
            return redirect('/login')
    
    try:
        return send_file(f'{path}/{file}')
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
