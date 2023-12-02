from flask import Flask
from blueprints.api.user import Users
from blueprints.files import file_handler
from blueprints.admin import Admin
from blueprints.api.auth import Auth
from blueprints.api.media import Media
from mongoengine import connect, disconnect
import config

connect("LunnarisDB")
app = Flask(__name__, 
            static_url_path='',
            template_folder=config.TEMPLATES_FOLDER, 
            static_folder=config.STATIC_FOLDER)
app.register_blueprint(file_handler)
app.register_blueprint(Auth, url_prefix="/api/auth")
app.register_blueprint(Media, url_prefix="/api/media")
app.register_blueprint(Users, url_prefix="/api/users")
app.register_blueprint(Admin, url_prefix="/admin")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    disconnect("LunnarisDB")
