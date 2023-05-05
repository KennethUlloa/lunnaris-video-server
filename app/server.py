from flask import Flask
from blueprints.files import file_handler
from blueprints.api.auth import Auth
from blueprints.api.media import Media

app = Flask(__name__)
app.register_blueprint(file_handler)
app.register_blueprint(Auth, url_prefix="/api/auth")
app.register_blueprint(Media, url_prefix="/api/media")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

