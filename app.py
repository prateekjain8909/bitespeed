from flask import Flask
from database import db, SQLALCHEMY_DATABASE_URI
from routes import identify_contact

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

app.route('/identify', methods=['POST'])(identify_contact)

if __name__ == '__main__':
    app.run()

