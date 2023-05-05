from flask import Blueprint, request, Response
import json
from model.dao import SessionDAO, UserDAO
import config

sessions = SessionDAO()
users = UserDAO()
Auth = Blueprint(name="api_auth", import_name=__name__)

@Auth.post('/login')
def login():
    user = request.form.get('username','')
    password = request.form.get('password','')
    addr = request.remote_addr
    user = users.auth(user, password)
    if user == None or addr == None:
        return {'login_status':'error',
                        'message':'Fallo la autenticación', 
                        'reason': 'Usuario y/o contraseña incorrecta'}
    session = sessions.create(user.username, user.password, addr)

    if session == None:
        return {"login_status":"error","message":"Fallo en la autenticación", "reason": "El servidor no pudo crear la sesión"}

    response = send_json({'login_status':'ok','user': user.display_name})
    response.set_cookie(config.SESSION_NAME, session.token,path="/")

    return response

@Auth.post("/logout")
def logout():
    response = Response(status=204,response='')
    sessions.delete(request.cookies.get(config.SESSION_NAME))
    response.delete_cookie(config.SESSION_NAME,'/')
    return response


def send_json(data):
    return Response(response=json.dumps(data), content_type='application/json')