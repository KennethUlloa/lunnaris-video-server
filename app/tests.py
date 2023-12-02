from model import model as md
from model import dao
import utils.tests_utils as _ts
from utils import utils
from mongoengine import connect

tester = _ts.Tester()
connect('LunnarisDB')


#@tester.test()
def test_register():
    # _ = db.DB.get_connection()
    user = md.User()
    user.username = "leo"
    user.password = "leo1234"
    user.displayName = "Kenneth"
    session = md.Session(token=utils.genToken(10), address="127.0.0.1")
    user.sessions = [session]
    user.save()


#@tester.test("leo", "leo1234", expected=True)
def test_query_user(username, password):
    res = dao.UserDAO.authorize(username, password)
    #print(res.to_json())
    if res is not None:
        print(res.to_json())
    return res is not None


#@tester.test("leo","leo1234","127.0.0.2", expected=True)
def test_create_session(username, password, address):
    session = dao.UserDAO.createSession(username, password, address)
    print(session)
    return session is not None


#@tester.test()
def test_get_all_media():
    print(dao.MediaDAO.getAllMedia())


def test_watch_session():
    dao.MediaDAO.updateWatchTime("the_batman", 0.0, "U0uMkjZZ2p")


if __name__ == "__main__":
    test_watch_session()
    