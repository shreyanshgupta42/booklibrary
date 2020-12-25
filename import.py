import csv

from flask import Flask, render_template, request

# Import table definitions.
from models import *

app = Flask(__name__)

# Tell Flask what SQLAlchemy databas to use.
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://evukltujjcdxos:e5d987d492a3d8d8f4d322dad093184f6777079f71695077cd2f766df624e756@ec2-34-230-149-169.compute-1.amazonaws.com:5432/dcg8r0q9p6kb9n"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)


def main():
    # Create tables based on each table definition in `models`
    db.create_all()
    consumer=Consumer(username="shreyansh",password="cosmos")
    db.session.add(consumer)
    print("added")
    db.session.commit()
    """
    f = open("books2.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        book = Book(isbn=isbn, title=title, author=author,year=year)
        db.session.add(book)
        print(f"Added book with isbn {isbn} ; title {title} ; author {author} in year {year}")
    db.session.commit()
    """

if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main()