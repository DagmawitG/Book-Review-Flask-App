import os

from flask import Flask, session,render_template,url_for,flash,redirect,request,jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm,LoginForm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt

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

@app.route("/index", endpoint= 'index', methods=['GET','POST'])
def index():
 
    if request.method == "GET":
        return render_template("index.html")

    search_text = request.form.get("search_text")
    option = request.form.get("option")
    if option == "isbn":
        
        books = db.execute("SELECT * FROM books WHERE isbn=:isbn",
                            {'isbn':search_text}).fetchall()
        if not books:
            
            flash(f'No book with specified ISBN Number', 'danger')
        return render_template("review.html",books = books ) 
   
    
    if option == 'author':
        books = db.execute("SELECT * FROM books WHERE author=:search_text",
                            {'search_text':search_text}).fetchall()
        if not books:
            flash(f'No book with specified Author', 'danger')
        return render_template("review.html",books = books ) 
    if option == 'title':
        books = db.execute("SELECT * FROM books WHERE title=:search_text",
                            {'search_text':search_text}).fetchall()
        if not books:
            flash(f'No book with specified Title', 'danger')
        return render_template("review.html",books = books ) 
        
        

    
  
    

    
@app.route("/contact", endpoint= 'contact')
def contact():
    return render_template('contact.html')
@app.route("/review", endpoint= 'review')
def review():
    return render_template('review.html')
@app.route("/single", endpoint= 'single')
def single():
    return render_template('single.html')




if __name__ == '__main__':
    app.run(debug=True)
