import json
from flask import Flask, Response, redirect, request, send_file, abort
import os
import model.db as db

app = Flask(__name__)

webroot = 'webapp/'
resources = 'D:/Documentos/Coding/Web/Lunnaris/Web/static/img/posters'
mapping = {
    'home': 'home.html',
    'player': 'player.html',
    'banner': 'videobanner.html'
}

session_name = "LN-SESSION"

@app.route('/')
def init_page():
    return resource('index.html')

@app.get('/video/<string:id>')
def send_video(id):
    conn = db.DB.get_connection()['LunnarisDB']['movies']
    movie = conn.find_one({"id":id}, projection={"_id":0, "src":1})
    return send_file(movie["src"])

@app.get('/resource/<string:file>')
def file_resource(file):
    img = f'{resources}/{file}'
    return send_file(img)

@app.route('/<path:resource>')
def resource(resource):

    need_auth_, response = need_auth(resource)
    if need_auth_ : return response

    return send_file_(resource)

def need_auth(resource: str):
    if resource in mapping:
        token = request.cookies.get(session_name)
        if dao.SessionDAO().exists(token):
            return True, send_file_(mapping[resource])
        else:
            return True, redirect('/')
    else:
        return False, None

def full_path(resource):
    return webroot + resource

def send_file_(file: str):
    fullpath = full_path(file)
    if os.path.exists(fullpath) and os.path.isfile(fullpath):
        return send_file(fullpath)
    else:
        return abort(404)

@app.post('/api/logout')
def logout():
    response = Response(status=204,response='')
    dao.SessionDAO().delete(request.cookies.get(session_name))
    response.delete_cookie(session_name)
    return response

@app.post('/api/login')
def login():
    user = request.form.get('username')
    password = request.form.get('password')
    user = dao.UserDAO().auth(user, password)
    if user == None:
        return {'login_status':'error',
                        'message':'Fallo la autenticación', 
                        'reason': 'Usuario y/o contraseña incorrecta'}
    session = dao.SessionDAO().create(user.username, user.password, request.remote_addr)

    if session == None:
        return {"login_status":"error","message":"Fallo en la autenticación", "reason": "El servidor no pudo crear la sesión"}

    response = send_json({'login_status':'ok','user': user.display_name})
    response.set_cookie(session_name, session.token)

    return response

@app.get('/api/allmedia')
def all_media():
    return dao.VideoDAO().get_all()

@app.get('/api/media/<string:id>')
def get_media(id):
    token = request.cookies.get(session_name)
    return dao.VideoDAO().get_full(id, token)

@app.put('/api/media/<string:id>/<float:time>')
def update_watched_time(id, time):
    token = request.cookies.get(session_name)
    dao.VideoDAO().update_time(id, time, token)
    return ('', 204)

def send_json(data):
    return Response(response=json.dumps(data), content_type='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True, debug=True)
    print("Closing db connection")
    db.DB.close()
    print("Connection closed")


