from model.dao import SessionDAO
from flask import request, abort

def _auth():
    if SessionDAO.exists(request.cookies.get("LN-SESSION")):
        return True, None
    else:
        return False, abort(404)