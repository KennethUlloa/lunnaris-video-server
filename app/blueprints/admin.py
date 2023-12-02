from flask import Blueprint, abort, render_template, send_file, request, redirect
from model.model import *
import config

Admin = Blueprint(name="admin_path",import_name=__name__)

def is_admin(cookie):
    user = User.objects(sessions__token=cookie).first()
    if not user:
        return False
    
    if user.userType == UserType.ADMIN:
        return True
    
    return False

@Admin.get("/")
def admin():
    if not is_admin(request.cookies.get(config.SESSION_NAME)):
        return abort(401)

    return render_template("admin.html",users=User.objects(), media_list=Media.objects())

@Admin.get("/user/update")
def update_user():

    if not is_admin(request.cookies.get(config.SESSION_NAME)):
        return abort(401)

    userid = request.args.get("username")
    user = User.objects(username=userid).first()
    if user:
        return render_template(
            "admin_user.html",
            user=user, 
            options=[UserType.ADMIN, UserType.USER])
    else:
        return abort(404)


@Admin.get("/user/create")
def create_user():
    if not is_admin(request.cookies.get(config.SESSION_NAME)):
        return abort(401)
    
    return render_template(
            "create_user.html",
            options=[UserType.ADMIN, UserType.USER])

