from flask import Blueprint

Auth = Blueprint(name="api_auth", import_name=__name__)

@Auth.post('/login')
def login():
    return {"state": "you are logged id"}

@Auth.post("/logout")
def logout():
    return {"state": "you are logged out"}