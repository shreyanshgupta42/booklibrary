

from flask import Flask, session,render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
if not "postgres://evukltujjcdxos:e5d987d492a3d8d8f4d322dad093184f6777079f71695077cd2f766df624e756@ec2-34-230-149-169.compute-1.amazonaws.com:5432/dcg8r0q9p6kb9n":
	raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://evukltujjcdxos:e5d987d492a3d8d8f4d322dad093184f6777079f71695077cd2f766df624e756@ec2-34-230-149-169.compute-1.amazonaws.com:5432/dcg8r0q9p6kb9n")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
	#book= db.execute("SELECT * FROM book").fetchall()
	#return render_template("book.html",books=book)
	return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
	
	username=request.form.get("username")
	password=request.form.get("password")
	db.execute("INSERT INTO consumer1 (username, password) VALUES (:username, :password)",
			{"username": username, "password": password})
	db.commit()
	return render_template("login.html")

@app.route("/search",methods=["POST"])
def search():
	username=request.form.get("username")
	password=request.form.get("password")
	if db.execute("SELECT * FROM consumer1 WHERE username=:username",{"username":username}).rowcount >=1:
		if db.execute("SELECT * FROM consumer1 WHERE password=:password",{"password":password}).rowcount >=1:
			#book= db.execute("SELECT * FROM book").fetchall()
			return render_template("search.html")
	return render_template("failedlogin.html")

@app.route("/bookbyisbn",methods=["POST"])
def bookbyisbn():
	byisbn=(request.form.get("byisbn"))
	bookbyisbn=db.execute("SELECT * FROM book WHERE isbn like :byisbn",{"byisbn":"%"+byisbn+"%"}).fetchall()
	return render_template("book.html",books=bookbyisbn)

@app.route("/bookbyauthor",methods=["POST"])
def bookbyauthor():
	byauthor=request.form.get("byauthor")
	bookbyauthor=db.execute("SELECT * FROM book WHERE author like :byauthor",{"byauthor":"%"+byauthor+"%"}).fetchall()
	return render_template("book.html",books=bookbyauthor)

@app.route("/bookbytitle",methods=["POST"])
def bookbytitle():
	bybook=request.form.get("bybook")
	bookbybook=db.execute("SELECT * FROM book WHERE title like :bybook",{"bybook":"%"+bybook+"%"}).fetchall()
	return render_template("book.html",books=bookbybook)

@app.route("/bookbyall",methods=["POST"])
def bookbyall():
	book=db.execute("SELECT * FROM book").fetchall()
	return render_template("book.html",books=book)

#a particular book

@app.route("/books/<int:book_id>")
def bookid(book_id):
	book=db.execute("SELECT * FROM book WHERE id=:id",{"id":book_id}).fetchone()
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "25mcRLrxL3R0ZyfluzuiNA", "isbns": "9781442468351"})
	data = res.json()
	averagerat=data['books'][0]['average_rating']
	noofrating=data['books'][0]['work_ratings_count']
	print(data)
	#averagerat=data["books"]['average_rating']
	#averagerat=data["average_rating"]
	#return render_template("bookid.html",books=book,averagerat=averagerat)
	#render_template("bookid.html",books=book,data=data,averagerat=averagerat)
	return render_template("bookid.html",books=book,averagerat=averagerat,noofrating=noofrating)


	