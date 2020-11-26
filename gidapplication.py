import os
import sys
import datetime
from wsgiref.simple_server import make_server
import sqlite3
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import functools
from flask import Blueprint
#from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from gidhelpers import login_required, lookup, login_as_employer_required
import gidmodal
from gidmodal import gidconnection, gidcursor



# Read port selected for our application
PORT = int(os.getenv('', 8000))




########MODEL/DATABASE MODAL###########################is in gidmodal.py#########




########VIEW MODAL #########is in gid-master/tenplates and static folders########





########CONTROLLER MODEL#######BEGINS##################################
# Configure application
gidapp = Flask(__name__, static_url_path='/static/')
gidapp.secret_key = f'afekudemetrio'
# Ensure templates are auto-reloaded
gidapp.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@gidapp.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
gidapp.config["SESSION_FILE_DIR"] = mkdtemp()
gidapp.config["SESSION_PERMANENT"] = False
gidapp.config["SESSION_TYPE"] = "filesystem"
#Session(gidapp)


#index route
@gidapp.route("/")
def root():
    return gidapp.send_static_file('index.html')

@gidapp.route("/gidsearchengine", methods=["GET", "POST"])
def gid_search_engine():
    if request.method=="POST":
        search=request.form["searchengine"]
        return f"<p>Your search item <em>{search}</em> is quite unique to the system</p>"
    else:
        pass


@gidapp.route("/gidregister", methods=["GET", "POST"])
def register():

    """Register a new user as personnel by

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        firstname = request.form["first_name"]
        lastname = request.form["last_name"]
        country = request.form["country"]
        city = request.form["city"]
        email = request.form["email"]
        telephone = request.form["telephone"]
        qualification = request.form["qualification"]
        experiences = request.form["experiences"]
        skills = request.form["skills"]
        user_name = request.form["user_name"]
        password = request.form["password"]
        personnel_gps=50000
        date_of_reg=datetime.datetime.now()
        error=None

        if (
            gidcursor.execute("SELECT Personnel_Id_No FROM personnels WHERE Personnel_User_Name = ?", (user_name,)).fetchone()
            is not None
        ):

            return f"<h2>Sorry! Username <em>{user_name}</em> is already taken,select another username and</h2><a href = '/gidregister'>" + "<strong>Register again</strong></a>"

        else:
            # the name is not in system, store it in the database and go to
            # the login page
            gidcursor.execute(
                "INSERT INTO personnels (Personnel_First_Name,Personnel_Last_Name,Personnel_User_Name,Personnel_Password,Personnel_Tel_No,Personnel_Email_address,Personnel_Country,Personnel_City_Of_Residence,Personnel_Qualifications,Personnel_Experiences,Personnel_Skills,Personnel_Gps_Location,Personnel_Date_Of_Registration) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (

                firstname,
                lastname,
                user_name,
                generate_password_hash(password),
                telephone,
                email,
                country,
                city,
                qualification,
                experiences,
                skills,
                personnel_gps,
                date_of_reg
                )
            )

            gidconnection.commit()
            return redirect("/gidlogin")
    else:
        return render_template("register.html")



@gidapp.route("/employergidregister", methods=["GET", "POST"])
def employer_register():
    """Register user as employer to creat and post job and
    Validates that the username is not already taken. Hashes the
    password for security."""

    if request.method == "POST":
        efirstName = request.form["firstName"]
        elastName = request.form["lastName"]
        eCountry = request.form["Country"]
        eCity = request.form["City"]
        eEmail = request.form["Email"]
        eTelephone = request.form["Telephone"]
        eUserName = request.form["userName"]
        ePassword = request.form["Password"]
        eEmployer_Gps=50000
        eDate_of_Reg=datetime.datetime.now()
        eError=None

        if (
            gidcursor.execute("SELECT Employer_Id_No FROM employers WHERE Employer_User_Name = ?", (eUserName,)).fetchone()
            is not None
        ):

            return f"<h2>Sorry! Username <em>{eUserName}</em> is already taken,select another username and</h2><a href = '/employergidregister'>" + "<strong>Register again</strong></a>"

        else:
            # the name is not in system, store it in the database and go to
            # the login page
            gidcursor.execute(
                "INSERT INTO employers (Employer_First_Name,Employer_Last_Name,Employer_User_Name,Employer_Password,Employer_Tel_No,Employer_Email_Address,Employer_Country,Employer_City_Of_Residence,Employer_Gps_Location,Employer_Date_Of_Registration) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (

                efirstName,
                elastName,
                eUserName,
                generate_password_hash(ePassword),
                eTelephone,
                eEmail,
                eCountry,
                eCity,
                eEmployer_Gps,
                eDate_of_Reg
                )
            )

            gidconnection.commit()
            return redirect("/employergidlogin")
    else:
        return render_template("employerregistry.html")


#@gidapp.before_app_request
#def load_logged_in_user():
#    """If a user id is stored in the session, load the user object from
#    the database into ``user``."""
#    user_id = session.get("user_id")
#
#   if user_id is None:
#        user = None
#    else:
#       user = (
#            gidcursor.execute("SELECT * FROM personnels WHERE id = ?", (user_id,)).fetchone()
#       )




@gidapp.route("/gidlogin", methods=["GET", "POST"])
def login():
    """Log in a registered user by adding the user id to the session."""
    session.clear()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        user = gidcursor.execute(
            "SELECT * FROM personnels WHERE Personnel_User_Name = ?", (username,)
        ).fetchone()

        if user is None:
            return "<h2>Incorrect username, Sorry you have not been logged in!</h2><br><a href = '/gidlogin'>" + "<strong>Login again</strong></a>"
        elif not check_password_hash(user[4], password):
            return "<h2>Incorrect password, Sorry you have not been logged in!</h2><br><a href = '/gidlogin'>" + "<strong>Login again</strong></a>"

        else:
            # store the user id in a new session and return to the index
            session["user_id"] = user[0]
            return redirect("/personnelhomepage")
    else:
        return render_template("gidlogin.html")


@gidapp.route("/employergidlogin", methods=["GET", "POST"])
def employer_login():
    #Log in a registered user by adding the user id to the session.
    session.clear()
    if request.method == "POST":
        euserName = request.form["userName"]
        epassWord = request.form["PassWord"]
        error = None
        userEmployer = gidcursor.execute(
            "SELECT * FROM employers WHERE Employer_User_Name = ?", (euserName,)
        ).fetchone()

        if userEmployer is None:
            return "<h2>Incorrect username, Sorry you have not been logged in!</h2><br><a href = '/employergidlogin'>" + "<strong>Login again</strong></a>"
        elif not check_password_hash(userEmployer[4], epassWord):
            return "<h2>Incorrect password, Sorry you have not been logged in!</h2><br><a href = '/employergidlogin'>" + "<strong>Login again</strong></a>"

        else:
            # store the user id in a new session and redirect to employers page
            session["employer_user_id"] = userEmployer[0]
            return redirect("/employerhomepage")
    else:
        return render_template("employergidlogin.html")

@gidapp.route("/gidlogout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect("/gidlogin")


@gidapp.route("/gidemployerlogout")
def employer_logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect("/employergidlogin")

@gidapp.route("/employerhomepage", methods=["GET", "POST"])
@login_as_employer_required
def employerhomepage():
    """employerhomepage.html."""
    loggedinemployer=session["employer_user_id"]
    useremployer = gidcursor.execute(
            "SELECT * FROM employers WHERE Employer_Id_No = ?", (loggedinemployer,)
        ).fetchone()
    username=useremployer[3]
    username1=username[0]
    taskStatus = gidcursor.execute(
        "SELECT * FROM tasks WHERE Employer_Identity=?"
        " ORDER BY Task_Date_Of_Post DESC", (loggedinemployer,)
    ).fetchall()
    return render_template("gidemployerhomepage.html",username1=username1,username=username,taskStatus=taskStatus)

@gidapp.route("/gidprofile", methods=["GET", "POST"])
@login_required
def profile():
    """profile.html"""
    return "To be implemented"

@gidapp.route("/giddoajob", methods=["GET", "POST"])
@login_required
def doajob():
    """account.html"""
    return ("TODO")



@gidapp.route("/personnelhomepage")
@login_required
def personnelhomepage():
    """personnelhomepage.html"""
    loggedinuser=session["user_id"]
    user = gidcursor.execute(
            "SELECT * FROM personnels WHERE Personnel_Id_No = ?", (loggedinuser,)
        ).fetchone()
    userfirstname1=user[1]
    userlastname=user[2]
    userfirstname2=userfirstname1[0]
    """Show all the task, most recent first."""
    currentTasks = gidcursor.execute(
        "SELECT * FROM tasks"
        " ORDER BY Task_Date_Of_Post DESC"
    ).fetchall()
    return render_template('personnelhomepage.html',userfirstname2=userfirstname2,userfirstname1=userfirstname1,userlastname=userlastname,currentTasks=currentTasks)


@gidapp.route("/gidposttask", methods=["GET", "POST"])
@login_as_employer_required
def gidpostingtask():
    """gidposttask.html"""
    if request.method == "POST":
        taskName = request.form["taskname"]
        taskCategory=request.form["taskcategory"]
        taskDescription=request.form["taskdescription"]
        requiredSkills=request.form["requiredskills"]
        payment=request.form["payment"]
        estimatedBudget=request.form["estimatedbudget"]
        taskCurrency=request.form["currency"]
        taskPostDate=request.form["taskpostdate"]
        taskPosition=50000
        taskDeadline=request.form["taskdeadline"]
        taskEmployerId=session["employer_user_id"]
        gidcursor.execute(
                "INSERT INTO tasks (Employer_Identity,Task_Category,Task_Name,Task_Description,Task_Requirements,Task_Gps_Location,Task_Budget_Amount,Task_Budget_Currency,Task_Date_Of_Post,Task_Deadline) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (

                taskEmployerId,
                taskCategory,
                taskName,
                taskDescription,
                requiredSkills,
                taskPosition,
                estimatedBudget,
                taskCurrency,
                taskPostDate,
                taskDeadline
                )
            )
        gidconnection.commit()
        return redirect("/employerhomepage")
    else:
        return render_template("gidposttask.html")

@gidapp.route("/joblist", methods=["GET", "POST"])
@login_required
def joblist():
    """joblist.html"""
    return "<h1>To be implemented</h1>"

@gidapp.route("/jobcategories", methods=["GET", "POST"])
@login_required
def jobcategories():
    """jobcategories.html"""
    return ("TODO")

@gidapp.route("/lookingajob", methods=["GET", "POST"])
@login_required
def lookingajob():
    """lookingajob.html"""
    return ("TODO")

@gidapp.route("/biddingonjob", methods=["GET", "POST"])
@login_required
def biddingonjob():
    """bidding on job"""
    if request.method=="POST":
        bidder=session["user_id"]
        taskId=request.form["TaskId"]
        employerId=request.form["EmployerIdentity"]
        return f"<h1><em>bidder {bidder}, Your bid on task {taskId} by {employerId} is under processing <a href=""/personnelhomepage"">Back to Home</a></em></h1>"
    else:
        pass

@gidapp.route("/selectingpersonnel", methods=["GET", "POST"])
@login_required
def selectingpersonnel():
    """selectingpersonnel.html"""
    return ("TODO")

@gidapp.route("/taskagreement", methods=["GET", "POST"])
@login_required
def taskagreement():
    """taskagreement.html"""
    return ("TODO")

@gidapp.route("/taskdoneconfirmation", methods=["GET", "POST"])
@login_required
def taskdoneconfirmation():
    """taskdoneconfirmation.html"""
    return ("TODO")

@gidapp.route("/fundrequest", methods=["GET", "POST"])
@login_required
def fundrequest():
    """fundrequest.html"""
    return ("TODO")

@gidapp.route("/fundprocessing", methods=["GET", "POST"])
@login_required
def fundprocessing():
    """fundprocessing.html"""
    return ("TODO")

@gidapp.route("/history", methods=["GET", "POST"])
@login_required
def history(
):
    """history.html"""
    return ("TODO")

@gidapp.route("/map", methods=["GET", "POST"])
@login_required
def map():
    """map.html"""
    return ("TODO")

@gidapp.route("/gidInfo", methods=["GET", "POST"])
@login_required
def info():
    """gidinfo.html"""
    return "To be implemented"

@gidapp.route("/gidchatboard", methods=["GET", "POST"])
@login_required
def chatboard():
    """message.html"""
    return "To be implemented"

#########CONTROLLER APPLICATION######ENDS#########################

#save any changes
gidconnection.commit()
#########MODAL##########ENDS######################################
###########WSGIsever##############BEGINS##########################
if __name__ == "__main__":
    with make_server('', PORT,gidapp) as httpd:
        print(f"gidapplication server is switched on port {PORT}")
        # WSGIsever Serve until process is killed
        httpd.serve_forever()
###########WSGIsever##############ENDS############################/