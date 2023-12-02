from flask import Blueprint, jsonify, request, Response
from model.model import User

Users = Blueprint(name="api_users", import_name=__name__)

@Users.put("/")
def updateUser():
    changes = 0
    data = request.get_json()
    user = User.objects(username=data["username"], password=data["password"]).first()

    if not user: 
        return {"status":"FAILED", "message": "Autenticación fallida"}, 401
    
    if "newpassword" in data and data["newpassword"] != "":
        user.password = data["newpassword"]
        changes += 1

    if "displayname" in data and (user.displayName != data["displayname"] and data["displayname"] != ""):
        user.displayName = data["displayname"]
        changes += 1

    if changes > 0:
        user.save()

    return {"status":"OK"}

@Users.post("/")
def create_user():
    data = request.get_json()
    if data["password"] != data["confirmPassword"]:
        return {"status": "FAILED", "message":"Las contraseñas no coinciden"}, 400
    
    user = User()
    user.username = data["username"]
    user.password = data["password"]
    user.displayName = data["displayName"]
    user.userType = data["type"]
    user.save()

    return {"status": "OK", "message": "Usuario creado exitósamente"}