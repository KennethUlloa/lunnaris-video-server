from flask import Blueprint, request, Response
import json
from model.dao import SessionDAO, UserDAO
import config


Auth = Blueprint(name="api_auth", import_name=__name__)

@Auth.post('/login')
def login():
    user = request.form.get('username','')
    password = request.form.get('password','')
    addr = request.remote_addr
    user = UserDAO.authorize(user, password)
    if user == None or addr == None:
        return {'status':'error',
                        'message':'Fallo la autenticación', 
                        'reason': 'Usuario y/o contraseña incorrecta'}
    session = UserDAO.createSession(user.username, user.password, addr)

    if session == None:
        return {"status":"error","message":"Fallo en la autenticación", "reason": "El servidor no pudo crear la sesión"}

    response = send_json({'status':'ok','user': user.displayName})
    response.set_cookie(config.SESSION_NAME, session.token.__str__() ,path="/")

    return response

@Auth.post("/logout")
def logout():
    response = Response(status=200, content_type='application/json')
    SessionDAO.delete(request.cookies.get(config.SESSION_NAME)) 
    response.response = json.dumps({"status": "ok"})
    response.delete_cookie(config.SESSION_NAME,'/')
    return response


def send_json(data):
    return Response(response=json.dumps(data), content_type='application/json')