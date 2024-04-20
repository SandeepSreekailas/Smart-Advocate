from flask import *
from admin import *
from advocate import *
from client import *
from public import public

app=Flask(__name__)

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(advocate)
app.register_blueprint(client)

app.secret_key='223344'

app.run(debug=True)