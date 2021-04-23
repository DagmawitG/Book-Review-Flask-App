import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



# Set up database
engine = create_engine('postgresql://yxkzxdsvfclkom:86cc791678693a713e5f8c05bae3be2b75d56c3424f1e16d5f8664027575e78d@ec2-34-225-167-77.compute-1.amazonaws.com:5432/d5r51ksuqtpl6r')

db = scoped_session(sessionmaker(bind=engine))

def main():
    global db

    f = open("books.csv") 
    reader = csv.reader(f) 
    next(reader, None)
   
    for isbn, title, author, year in reader:
        
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", 
                {"isbn": isbn, 
                "title": title, 
                "author": author, 
                "year": year})
 
    db.commit()
def create_user_table():
    global db
    create_user_table = """
    CREATE TABLE users (
          id SERIAL PRIMARY KEY,
          username VARCHAR NOT NULL unique,
          email VARCHAR NOT NULL,
          password VARCHAR NOT NULL
      )
    """
    db.execute(create_user_table)
    db.commit()

def create_book_table():
    global db
    create_book_table = """
    CREATE TABLE books (
          id SERIAL PRIMARY KEY,
          isbn VARCHAR NOT NULL,
          title VARCHAR NOT NULL,
          author VARCHAR NOT NULL,
          year VARCHAR NOT NULL
      )
    """
    db.execute(create_book_table)
    db.commit()

def create_review_table():
    global db
    create_book_table = """
    CREATE TABLE reviews (
          id SERIAL PRIMARY KEY,
          review_msg VARCHAR NOT NULL,
          review_score INTEGER NOT NULL,
          books_id INTEGER REFERENCES books,
          users_id INTEGER REFERENCES users
      )
    """
    db.execute(create_book_table)
    db.commit()


if __name__ == '__main__':
    #main()
    #create_user_table()
    #create_book_table()
    #create_review_table()
