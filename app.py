from flask import Flask
from views import index, action

app = Flask(__name__)

app.register_blueprint(action.app)
app.register_blueprint(index.app)

if __name__ == "__main__":
    app.run()
