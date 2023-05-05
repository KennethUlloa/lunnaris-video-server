import model.dao as dao
import model.model as m
import model.db as db


def test_register():
    _ = db.DB.get_connection()
    user = m.User("leo2","1234","kenneth",[m.Session("asdfasdf1","127.0.0.1")])
    res = dao.UserDAO().register(user=user)
    print(res)
    db.DB.close()

def test_get_all():
    _ = db.DB.get_connection()
    res = dao.UserDAO().get()
    print(res)
    db.DB.close()

def test_auth():
    _ = db.DB.get_connection()
    res = dao.UserDAO().auth("leo","leo1234")
    print(res.to_dict() if res != None else None)
    db.DB.close()

def test_update():
    _ = db.DB.get_connection()
    user = dao.UserDAO().get(username="leo")
    if user != None and type(user) == m.User:
        user.sessions.append(m.Session("xcvvvvvs123","192.168.100.3"))
        state = dao.UserDAO().update(user=user)
        print(state)
    else:
        print(False)
    db.DB.close()

def test_movie(): #'HU7gT9GIqd'
    movie = dao.VideoDAO().get_full('the_batman',"HU7gT9GIqd")
    print(movie)

def test_update_time(id,time,token):
    ack = dao.VideoDAO().update_time(id,time,token)
    print(ack)

def test_exists_session():
    print(dao.SessionDAO().exists("HU7gT9GIqda"))

def test_create_session():
    s = dao.SessionDAO().create('leo', 'leo1234', '127.0.0.1')
    print(s)

def test_time(id, token):
    resp = dao.VideoDAO().get_watched_time(id, token)
    print(resp)

if __name__ == "__main__":
    test_update_time('aquaman',0.2,'0GQNJH9A8y')

