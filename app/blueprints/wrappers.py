from model.dao import SessionDAO
from flask import request, abort

sessionDAO = SessionDAO()
def _auth():
    if sessionDAO.exists(request.cookies.get("LN-SESSION")):
        return True, None
    else:
        return False, abort(404)