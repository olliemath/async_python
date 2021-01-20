from sanic import Sanic

from extensions import setup_database
from routes import bp


app = Sanic(__name__)
app.blueprint(bp)
setup_database(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, access_log=False)
