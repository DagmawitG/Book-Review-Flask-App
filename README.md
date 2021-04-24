
# Project 1: BookHub
This project is adopted form Harvard's most popular class CS50 Programming with Python and JavaScript.

# Objectives

# Become more comfortable with Python.
# Gain experience with Flask.
# Learn to use SQL to interact with databases.


# Overview
This project,BookHub, is a book review website. Users will be able to register for BookHub and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. The website will also use a third-party API by GoogleAPI, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via the website’s API.

# Getting Started

# PostgreSQL
For this project, the database used is PostgreSQL database hosted by Heroku.
# Python and Flask
The required libraries,as mentioned in the requirements.txt file,  were first installed before proceeding to the website.
# Google API
Google API is a popular book review website, and the API will be used in this project to get access to the review data for individual books.
Note that ratingsCount here is the number of ratings that this particular book has received, and averageRating is the book’s average score out of 5.

# Requirements


# Registration: 
The "createAccount.html" page registers users by providing username, email, and password. The password is then encrypted and stored in the database. The Sign up button will submit only when the user enters the information in all the fields.


# Login:
Once the users are registered they will automatically be redirected to the Login page("login.html") to enter their username and password. The input they enter will then be checked if it matches with the one inserted in the database when a user creates an account. If it's correct, the page will redirect users to the "index.html" page where they can search for books as well as get random books information on the page.

# Logout:
 Logged in users will be able to log out of the site and then be redirected to the welocome page.

# Import:
The provided books.csv file, a spreadsheet in CSV format of 5000 different books, will be used in this project to get the ISBN number, title, author, and a publication year of each books. The import.py file will take the books and import them into the PostgreSQL database. There are three tables formed in this database. The first one is the books table where the books in the books.csv file are stored. The second table is the users table that stores users information(username, hashed password,email and the user's id). The last table is the reviews table that stores the rating and reviews related informations such as the review score and review message.

# Search:
 Once a user has logged in, they will be taken to a index.html where they can search for a book. Users will be able to choose whether they would like to use the ISBN number of a book, the title of a book, or the author of a book. After performing the search, the website will display a list of possible matching results in the review.html page, or no books found message if there were no matches. If the user typed in only part of a title, or author name, the search page will find matches for those as well!

# Book Page:
 When users click on a book from the results of the search page, they will be taken to a book page(single.html), with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on the website.

# Review Submission: 
On the book page, users will be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users will not be able to submit multiple reviews for the same book.

# GoogleAPI Review Data: 
On the book page,  the average rating and number of ratings the work has received from GoogleAPI will be displayed. When the user submit a review it automatically adds it to the database and the number of ratings will increase with one and get the average rating of the book by adding the review score and taking the average.

# API Access:
 If users make a GET request to the website’s /api/ route, where is an ISBN number, the website will return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON will follow the format:

    {
        "title": "Memory",
        "author": "Doug Lloyd",
        "year": 2015,
        "isbn": "1632168146",
        "review_count": 28,
        "average_score": 5.0
    }
If the requested ISBN number isn’t in the database, the website will return a 404 error.

