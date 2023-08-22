"""Copyright (C) 2023  Ryan Bauroth, Cem Akdurak, Arda Güzel, and Marcos Ginemar => See license file for more details"""

from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
