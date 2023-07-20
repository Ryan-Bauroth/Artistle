from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")


if __name__ == '__main__':
    print("http://127.0.0.1:8080/views/single-player")
    app.run(debug=True, port=8080)
