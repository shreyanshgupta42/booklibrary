from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Book(db.Model):
	__tablename__="book"
	id=db.Column(db.Integer,primary_key=True)
	isbn=db.Column(db.BigInteger,nullable=False)
	title=db.Column(db.String,nullable=False)
	author=db.Column(db.String,nullable=False)
	year=db.Column(db.Integer,nullable=False)

class Consumer(db.Model):
	"""docstring for Consumer"""
	__tablename__="consumer1"
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String,nullable=False)
	password=db.Column(db.String,nullable=False)
	

