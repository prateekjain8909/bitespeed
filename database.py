from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="bitespeed",
    password="poRALEyErI",
    hostname="bitespeed.mysql.pythonanywhere-services.com",
    databasename="bitespeed$default",
)