import os

from flask import Flask, session,render_template,url_for,flash,redirect,request,jsonify

from flask_login import logout_user
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'da3f03842283a7023ea42bc7738ab17a'
bcrypt = Bcrypt(app)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database


uri = os.getenv("DATABASE_URL")
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
engine = create_engine('postgresql://postgres:dagi123!@localhost:5432/bookreview')
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@app.route("/welcome" , )
def welcome():
    return render_template('welcome.html')
@app.route("/login", endpoint= 'login',methods=['GET','POST'])
def login():
    form = LoginForm()
    info = db.execute("SELECT * FROM users WHERE username = :username", {"username": form.username.data}).fetchone()
    if form.validate_on_submit():
        if (info and bcrypt.check_password_hash(info.password, form.password.data)):
            session["user"] = info.id
            flash(f'Welcome back {form.username.data}!', 'success')
            return redirect(url_for('index'))
        else:
             flash(f'Login Unsuccessful, Please check your username and password', 'danger')
            
    return render_template('login.html',form = form)
@app.route("/createAccount" , endpoint= 'createAccount',methods=['GET','POST'])
def createAccount():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", {
               "username": form.username.data, "email":form.email.data, "password": hashed_password})
        db.commit()
        flash(f'Account created for {form.username.data},\n Please Login!', 'success')
       
        return redirect(url_for('login'))
        
    return render_template('createAccount.html',form = form)



def home():
    return db.execute("SELECT * FROM books ORDER BY random() limit 12")
    
@app.route("/index", endpoint= 'index', methods=['GET','POST'])
def index():
    if not session['user']:
        return redirect('welcome')
    if request.method == "GET":
        return render_template("index.html", homeInfo = home())

    search_text = request.form.get("search_text")
    option = request.form.get("option")
    if option == "isbn":
        
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn",
                            {'isbn':search_text}).fetchall()
        if not books:
            
            flash(f'No book with specified ISBN Number', 'danger')
        return render_template("review.html",books = books ) 
   
    search_text = "%" + search_text + "%"
    if option == 'author':
        books = db.execute("SELECT * FROM books WHERE author LIKE :search_text",
                            {'search_text':search_text}).fetchall()
        if not books:
            flash(f'No book with specified Author', 'danger')
        return render_template("review.html",books = books ) 
    if option == 'title':
        books = db.execute("SELECT * FROM books WHERE title LIKE :search_text",
                            {'search_text':search_text}).fetchall()
        if not books:
            flash(f'No book with specified Title', 'danger')
        return render_template("review.html",books = books ) 
        
        
def getApi(isbn):
    api = f"https://www.googleapis.com/books/v1/volumes?q=isnn:{isbn}"
    return requests.get(api).json()

    
@app.route("/details/<int:bookid>", methods=["GET","POST"],endpoint='details')
def details(bookid):
    # review= []
   # result = db.execute("SELECT * from books WHERE id = :id", {"id": bookid}).fetchone()
    result = db.execute("SELECT * from books WHERE id = :id", {"id": bookid}).fetchone()
    if request.method == "GET":
       
        comment_list = db.execute("SELECT u.username, u.email, r.review_score, r.review_msg from reviews r JOIN users u ON u.id=r.users_id WHERE books_id = :id", {"id": bookid}).fetchall()
       
        if not result:
            flash(f'Invalid book id', 'danger')
        return render_template("single.html", result=result, comment_list=comment_list , bookid=bookid ,google = getApi(result.isbn))
       
    else:
        
        user_reviewed_before = db.execute("SELECT * from reviews WHERE users_id = :users_id AND books_id = :book_id",  {"users_id": session["user"], "book_id": bookid}).fetchone()
        if user_reviewed_before:
            flash(f'You reviewed this book before!', 'warning')
            return redirect(url_for("details", bookid=bookid))
        
        user_comment = request.form.get("comments")
        user_rating = request.form.get("rating")

        if not user_comment:
            flash(f'Comment section cannot be empty!', 'danger')
            return redirect(url_for("details", bookid=bookid))

        # try to commit to database, raise error if any
        
        try:
            db.execute("INSERT INTO reviews (users_id, books_id, review_score, review_msg) VALUES (:users_id, :books_id, :review_score, :review_msg)",
                           {"users_id": session["user"], "books_id": bookid, "review_score":user_rating, "review_msg": user_comment})
            
        except Exception as e:
            flash(f'Error occured {e}', 'warning')
        
        db.commit()
        return redirect(url_for("details", bookid=bookid))
            
           
            
        
            
           

            
            
           


    
@app.route("/contact", endpoint= 'contact')
def contact():
    return render_template('contact.html')
@app.route("/review", endpoint= 'review')
def review():
    return render_template('review.html')
# @app.route("/single", endpoint= 'single')
# def single():
#     return render_template('single.html')

@app.route('/logout')
def logout():
    session.clear()  
    session['user'] = ""
    
    return redirect(url_for("welcome")) 
        


if __name__ == '__main__':
    app.run(debug=True)
