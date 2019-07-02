from flask import Blueprint, Response

app = Blueprint('action', __name__)


@app.route("/action")
def hello():
    return Response('''
            NON-RESTRICTED AREA: Hello from action.py<br />
            <a href="/index">RESTRICTED AREA</a><br />
            ''')
