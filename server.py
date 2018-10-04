"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    if session["active"]:
        # logout

        return render_template("homepage.html",
                                #logout=logout)




    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html",
                            users=users)

@app.route('/login')
def login_page():
    """Take use to login page."""

    return render_template("login_form.html")

@app.route('/login-check')
def login_check():

    email = request.args.get("user_email")
    password = request.args.get("user_password")
    user_info = db.session.query(User.email, User.password, User.user_id).all()

    for user in user_info:
        if user[0] == email and user[1] == password:
            flash(u"Logged In")
            session["active"] = user[2]

            return render_template("homepage.html")
        else:
            continue

    flash(u"No account found for the entered email/password.")
    return render_template("login_form.html")




@app.route('/register')
def route_to_form():
    """Take user to registration page"""

    return render_template("register_form.html")

@app.route('/process-registration', methods =["POST"])
def register_process():
    email = request.form.get("user_email")
    password = request.form.get("user_password")

    user_info = User.query.filter_by(email=email).all()

    if user_info:
        print("You are already in our database. Please log in.")

        return render_template("homepage.html")
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template("homepage.html")
        




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
