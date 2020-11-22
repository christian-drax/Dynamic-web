from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import models
from flask import Flask, render_template, request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bookexampledbpassword@localhost:5432/bookexample'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/")
def home():
    return render_template('home.html', title="Home")


@app.route("/products-and-services/")
def products_and_services():
    return render_template('products-and-services.html', title="Products and Services")


@app.route("/about-us/")
def about_us():
    return render_template('about-us.html', title="About Us")


if __name__ == "__main__":
    app.run(port=5001) # here we are using a different port so as not to conflict with that allocated to our helloworld.py


@app.route("/signup/")
def signup():
    return render_template('signup.html', title="SIGN UP", information="Use the form displayed to register")


@app.route("/process-signup/", methods=['POST'])
def process_signup():
    # Let's get the request object and extract the parameters sent into local variables.
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    othernames = request.form['othernames']
    email = request.form['email']
    password = request.form['password']
    # let's write to the database
    try:
        user = models.User(firstname=firstname, lastname=lastname, othernames=othernames, email=email, password=password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        # Error caught, prepare error information for return
        information = 'Could not submit. The error message is {}'.format(e.__cause__)
        return render_template('signup.html', title="SIGN-UP", information=information)

    # If we have gotten to this point, it means that database write has been successful. Let us compose success info
    information = 'User by name {} {} successfully added. The login name is the email address {}.'.format(firstname, lastname, email)
    return render_template('signup.html', title="SIGN-UP", information=information)
