# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 13:31:34 2021

@author: Anziko Fred
"""
import os
import datetime
#import re
from flask import Flask, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from gidhelpers import login_required
#from gidmodal import giddb2connection
import waitress
#import ibm_db

"""Read port selected by the cloud for our application"""

PORT = int(os.getenv('PORT', 8080))

"""gidweb controller in current file gidapp.py"""
"""gidweb modal imported from gidmodal.py"""
"""gidweb view resides in static and templates folders"""
# Configure application
gidapp = Flask(__name__, static_url_path='/static/')
gidapp.secret_key = 'afekudemetrio'
# Ensure templates are auto-reloaded
gidapp.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
gidapp.config["SESSION_FILE_DIR"] = mkdtemp()
gidapp.config["SESSION_PERMANENT"] = False
gidapp.config["SESSION_TYPE"] = "filesystem"

#Database connection
#print("connecting DB2 database")
#gidconnection=giddb2connection()
#print("Database connection is",gidconnection)

#index route
@gidapp.route("/")
def root():
    """function to open index page/first page when a user access www.gidweb.com"""
    return gidapp.send_static_file('index.html')

@gidapp.route("/gidaboutus", methods=["GET", "POST"])
def about_us():
    return render_template("todo.html")
    pass

@gidapp.route("/gidhowto", methods=["GET", "POST"])
def howto():
    return render_template("todo.html")
    pass

@gidapp.route("/gidtermsandconditions", methods=["GET", "POST"])
def terms_and_conditions():
    return render_template("todo.html")
    pass

@gidapp.route("/gidsearchengine", methods=["GET", "POST"])
def gid_search_engine():
    """function to manage search and filter of content"""
    if request.method=="POST":
        search=request.form["searchengine"]
        print(search)
        return render_template("todo.html")
    else:
        pass


@gidapp.route("/gidregister", methods=["GET", "POST"])
def register():

    """Function to register and update users as personnel

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
        user_name = request.form["user_name"]
        password = request.form["password"]
        gpslat=request.form["gpsla"]
        gpslong=request.form["gpslo"]
        photo=None
        date_of_reg=datetime.datetime.now()
        #print(firstname,middlename,lastname,user_name,generate_password_hash(password),telephone,email,country,city,dob,gpslong,gpslat,date_of_reg,photo)
        """acessing DB2 database"""
        personnel_register_sql="INSERT INTO personnel (Personnel_First_Name,Personnel_Middle_Name,Personnel_Last_Name,Personnel_User_Name,Personnel_Password,Personnel_Tel_No,Personnel_Email_Address,Personnel_Country,Personnel_City_Of_Residence,Personnel_DOB,Personnel_Gps_Location_Long,Personnel_Gps_Location_Lat,Personnel_Date_Of_Registration,Personnel_Facial_Reco) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        personnel_register_sql_prepared=ibm_db.prepare(gidconnection,personnel_register_sql)
        personnel_sql_parameters=firstname,middlename,lastname,user_name,generate_password_hash(password),telephone,email,country,city,dob,gpslong,gpslat,date_of_reg,photo
        ibm_db.execute(personnel_register_sql_prepared,personnel_sql_parameters)
        return redirect("/gidlogin")
    else:
        return render_template("register.html")



@gidapp.route("/gidlogin", methods=["GET", "POST"])
def login():
    """function for Logging in a registered perssonel"""
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
            # store the user id in a new session and redirect user to the personnel homepage
            session["user_id"] = user_personnel["Personnel_Id_No"]
            return redirect("/gidpersonnelhomepage")
    else:
        return render_template("gidlogin.html")
    
@gidapp.route("/gidpersonnelhomepage")
@login_required
def personnelhomepage():
    """function for the management of personnel homepage"""
    loggedin_user=session["user_id"]
    loggedin_user_sql="SELECT * FROM personnels WHERE Personnel_Id_No = ?"
    loggedin_user_sql_prepared=ibm_db.prepare(gidconnection,loggedin_user_sql)
    loggedin_user_sql_parameters=loggedin_user
    loggedin_user_personnel=ibm_db.execute(loggedin_user_sql_prepared,loggedin_user_sql_parameters).ibm_db.fetch_assoc()
    userfirstname1=loggedin_user_personnel[1]
    userlastname=loggedin_user_personnel[2]
    userfirstname2=userfirstname1[0]
    """Show all the task, most recent first."""
    current_tasks_sql = "SELECT * FROM tasks" ," ORDER BY Task_Date_Of_Post DESC"
    current_tasks_sql_prepared=ibm_db.prepare(gidconnection,current_tasks_sql)
    current_tasks=ibm_db.execute(current_tasks_sql_prepared).ibm_db.fetch_assoc()
    return render_template('personnelhomepage.html',userfirstname2=userfirstname2,userfirstname1=userfirstname1,userlastname=userlastname,currentTasks=current_tasks)

@gidapp.route("/gidjobcreaterhomepage", methods=["GET", "POST"])
@login_required
def jobcreaterhomepage():
    """function for the management of employers homepage"""
    loggedin_jobcreater=session["user_id"]
    jobcreater_loggedin_sql="SELECT * FROM employers WHERE Employer_Id_No =?"
    jobcreater_loggedin_sql_prepared=ibm_db.prepare(gidconnection,jobcreater_loggedin_sql)
    jobcreater_loggedin_sql_parameters=loggedin_jobcreater
    user_jobcreater=ibm_db.execute(jobcreater_loggedin_sql_prepared,jobcreater_loggedin_sql_parameters)
    username=user_jobcreater[3]
    username1=username[0]
    task_sql="SELECT * FROM tasks WHERE Employer_Identity=?" ," ORDER BY Task_Date_Of_Post DESC"
    task_sql_prepared=ibm_db.prepare(gidconnection,task_sql)
    task_sql_parameters=loggedin_jobcreater
    task_status=ibm_db.execute(task_sql_prepared,task_sql_parameters).ibm_db.fetch_assoc()
    return render_template("jobcreaterhomepage.html",username1=username1,username=username,taskStatus=task_status)

@gidapp.route("/gidcreatetask", methods=["GET", "POST"])
@login_required
def createtask():
    """function to manage posting and updating of tasks by employers"""
    if request.method == "POST":
        Personel_identity=session["user_id"]
        Task_category=request.form["taskcategory"]
        Task_name= request.form["taskname"]
        Task_description=request.form["taskdescription"]
        Task_requirements=request.form["required"]
        Task_Gps_location_Long=0.50000
        Task_Gps_location_Lat=0.50000
        Task_budget_amount=request.form["estimatedbudget"]
        Task_currency=request.form["currency"]
        Task_Date_Of_Post=request.form["taskpostdate"]
        Task_Deadline=request.form["taskdeadline"]
        tasks_posting_sql="INSERT INTO todo_tasks (Task_Id_No,Personel_Employer_Identity,Task_Category,Task_Name,Task_Description,Task_Requirements,Task_Gps_Location_Long,Task_Gps_Location_Lat,Task_Budget_Amount,Task_Budget_Currency,Task_Date_Of_Post,Task_Deadline)"
        tasks_sql_prepared=ibm_db.prepare(gidconnection,tasks_posting_sql)
        tasks_sql_parameters=Personel_identity,Task_category,Task_name,Task_description,Task_requirements,Task_Gps_location_Long,Task_Gps_location_Lat,Task_budget_amount,Task_currency,Task_Date_Of_Post,Task_Deadline
        ibm_db.execute(tasks_sql_prepared,tasks_sql_parameters)
        return redirect("/gidjobcreaterhomepage")
    else:
        return render_template("createtask.html")

@gidapp.route("/gidpay", methods=["GET", "POST"])
@login_required
def finacial_transactions():
    pass

#CONTINUE FROM HERE AS OF 1:35 PM JUNE 11TH 2021
@gidapp.route("/gidbidding", methods=["GET", "POST"])
@login_required
def taskbidding():
    """function to manage task bidding process"""
    if request.method=="POST":
        bidder=session["user_id"]
        taskId=request.form["TaskId"]
        employerId=request.form["EmployerIdentity"]
        return f"<h1><em>bidder {bidder}, Your bid on task {taskId} by {employerId} is under processing <a href=""/personnelhomepage"">Back to Home</a></em></h1>"
    else:
        pass
    
@gidapp.route("/gidnotification", methods=["GET", "POST"])
@login_required
def notification():
    pass

@gidapp.route("/giduserhistory", methods=["GET", "POST"])
@login_required
def userhistory():
    pass

@gidapp.route("/gidlogout")
def logout():
    """Clear the current session to log out the current user to redirect the user to login page"""
    session.clear()
    return redirect("/")
"""gidweb WSGI server"""
if __name__ == "__main__":
    gidapp.debug=True
    waitress.serve(gidapp,port=PORT)
"""©whiterhino inc."""
