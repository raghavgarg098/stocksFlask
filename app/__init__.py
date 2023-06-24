from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://raghavgarg:postgres@localhost:5412/stocksdatabase'
CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)

__import__('app.apis')
