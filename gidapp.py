import os
import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import functools
from flask import Blueprint
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from gidhelpers import login_required, lookup, login_as_employer_required
import gidmodal
from gidmodal import gidconnection
import waitress
import psycopg2
import ibm_db






########MODEL/DATABASE MODAL###########################is in gidmodal.py#########




########VIEW MODAL #########is in gid-master/tenplates and static folders########
# Read port selected by the cloud for our application

PORT = int(os.getenv('PORT', 8000))





########CONTROLLER MODEL#######BEGINS##################################
# Configure application
gidapp = Flask(__name__, static_url_path='/static/')
gidapp.secret_key = f'afekudemetrio'
# Ensure templates are auto-reloaded
gidapp.config["TEMPLATES_AUTO_RELOAD"] = True

#Ensure responses aren't cached
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

    """Register a new user as personnel

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        firstname = request.form["first_name"]
        middlename=request.form["middle_name"]
        lastname = request.form["last_name"]
        country = request.form["country"]
        city = request.form["city"]
        email = request.form["email"]
        telephone = request.form["telephone"]
        dob=request.form["date_of_birth"]
        #qualification = request.form["qualification"]
        #experiences = request.form["experiences"]
        #skills = request.form["skills"]
        user_name = request.form["user_name"]
        password = request.form["password"]
        gpslong=0.5000
        gpslat=0.5000
        photo=None
        date_of_reg=datetime.datetime.now()
        """acessing DB2 database to check if the username exists"""
        check_userame_sql="SELECT Personnel_Id_No FROM personnel WHERE Personnel_User_Name =?"
        check_userame_sql_prepared=ibm_db.prepare(gidconnection,check_userame_sql)
        check_userame_sql_parameters=user_name
        personnel_username_checked=ibm_db.execute(check_userame_sql_prepared,check_userame_sql_parameters).ibm_db.fetch_assoc()
        if personnel_username_checked is not None:

            return f"<h2>Sorry! Username <em>{user_name}</em> is already taken,select another username and</h2><a href = '/gidregister'>" + "<strong>Register again</strong></a>"

        else:
            """ the name is not in system, store it in the database and go to
            the login page"""
            personnel_register_sql="INSERT INTO personnel (Personnel_First_Name,Personnel_Middle_Name,Personnel_Last_Name,Personnel_User_Name,Personnel_Password,Personnel_Tel_No,Personnel_Email_Address,Personnel_Country,Personnel_City_Of_Residence,Personnel_DOB,Personnel_Gps_Location_Long,Personnel_Gps_Location_Lat,Personnel_Date_Of_Registration,Personnel_Facial_Reco) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
            personnel_register_sql_prepared=ibm_db.prepare(gidconnection,personnel_register_sql)
            personnel_sql_parameters=firstname,middlename,lastname,user_name,generate_password_hash(password),telephone,email,country,city,dob,gpslong,gpslat,date_of_reg,photo
            ibm_db.execute(personnel_register_sql_prepared,personnel_sql_parameters)
            return redirect("/gidlogin")
    else:
        return render_template("register.html")






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
    """Log in a registered personell"""
    session.clear()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_sql ="SELECT * FROM personnel WHERE Personnel_User_Name =?"
        user_sql_prepared=ibm_db.prepare(gidconnection,user_sql)
        user_sql_parameters=username
        user_personnel=ibm_db.execute(user_sql_prepared,user_sql_parameters).ibm_db.fetch_assoc()

        if user_personnel is None:
            return "<h2>Incorrect username, Sorry you have not been logged in!</h2><br><a href = '/gidlogin'>" + "<strong>Login again</strong></a>"
        elif not check_password_hash(user_personnel["Personnel_Password"], password):
            return "<h2>Incorrect password, Sorry you have not been logged in!</h2><br><a href = '/gidlogin'>" + "<strong>Login again</strong></a>"

        else:
            # store the user id in a new session and return to the index
            session["user_id"] = user_personnel["Personnel_Id_No"]
            return redirect("/personnelhomepage")
    else:
        return render_template("gidlogin.html")


#registration as expert to do job and build cv/profile
@gidapp.route("/gidexperts", methods=["GET", "POST"])
def expertregisterupdater():
    pass

@gidapp.route("/gidlogout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect("/gidlogin")


"""to be continued"""
@gidapp.route("/employerhomepage", methods=["GET", "POST"])
@login_as_employer_required
def employerhomepage():
    """employerhomepage.html."""
    loggedin_employer=session["employer_user_id"]
    employer_loggedin_sql="SELECT * FROM employers WHERE Employer_Id_No =?"
    employer_loggedin_sql_prepared=ibm_db.prepare(gidconnection,employer_loggedin_sql)
    employer_loggedin_sql_parameters=loggedin_employer
    user_employer=ibm_db.execute(employer_loggedin_sql_prepared,employer_loggedin_sql_parameters)
    username=user_employer[3]
    username1=username[0]
    task_sql="SELECT * FROM tasks WHERE Employer_Identity=?" ," ORDER BY Task_Date_Of_Post DESC"
    task_sql_prepared=ibm_db.prepare(gidconnection,task_sql)
    task_sql_parameters=loggedin_employer
    task_status=ibm_db.execute(task_sql_prepared,task_sql_parameters)
    return render_template("gidemployerhomepage.html",username1=username1,username=username,taskStatus=task_status)

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
    loggedin_user=session["user_id"]
    user = gidcursor.execute(
            "SELECT * FROM personnels WHERE Personnel_Id_No = ?", (loggedinuser)
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
                "INSERT INTO tasks (Employer_Identity,Task_Category,Task_Name,Task_Description,Task_Requirements,Task_Gps_Location,Task_Budget_Amount,Task_Budget_Currency,Task_Date_Of_Post,Task_Deadline) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
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

#########MODAL##########ENDS######################################
###########WSGIsever##############BEGINS##########################
if __name__ == "__main__":
    gidapp.debug=False
    waitress.serve(gidapp,port=PORT)
###########WSGIsever##############ENDS############################/