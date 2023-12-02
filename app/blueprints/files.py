from flask import Blueprint, abort, render_template, send_file, request, redirect
from model.dao import MediaDAO, SessionDAO, User
import config
from blueprints.wrappers import _auth

file_handler = Blueprint(name="file_handler", import_name=__name__)

@file_handler.get('/<path:file>')
def send_files(file):
    try:
        return send_file(f'/{file}')
    except FileNotFoundError:
        return abort(404)

@file_handler.get("/")
def index():
    cookie = request.cookies.get(config.SESSION_NAME)
    
    user = User.objects(sessions__token=cookie).first()
    if not SessionDAO.exists(cookie) or not user:
        return redirect('/login')
    

    return render_template("index.html", user=user)

@file_handler.get("/login")
def login():
    return render_template("login.html")

@file_handler.get("/video/<string:video_id>")
def send_video(video_id): 
    try:
        path = MediaDAO.getVideoSrc(video_id)
        if path == "": raise FileNotFoundError
        return send_file(path)
    except FileNotFoundError:
        return abort(404)

