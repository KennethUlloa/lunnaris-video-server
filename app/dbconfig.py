import mongoengine
from model.dao import MediaDAO, UserDAO, User, SessionDAO
from mongoengine import connect, disconnect
connect("LunnarisDB")
cookie = "Ia8hKxWckspYH1ZYNN99"
print(SessionDAO.exists(cookie))
 
disconnect("LunnarisDB")