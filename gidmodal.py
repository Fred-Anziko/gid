# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 13:31:34 2021

@author: Anziko Fred
"""
def giddb2connection():
    """connection to the DB2 database for gidweb on IBM cloud foundry"""
    try:
        gidconnection= ibm_db.pconnect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-04.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=bds31662;PWD=0hdl2dpsqpmt@mpl;","","")
    except:
        print( "No connection:" , ibm_db.conn_errormsg())
        print("Database connection denied")
    else:
        print ("Database connection established.")
        return gidconnection

"""
gidconnection=giddb2connection()
Create personnel table
try:
    gid_personnel_sql="CREATE TABLE personnel(Personnel_Id_No INTEGER PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY(START WITH 1, INCREMENT BY 1), Personnel_First_Name VARCHAR(25),Personnel_Middle_Name VARCHAR(25),Personnel_Last_Name VARCHAR(25),Personnel_User_Name VARCHAR(25) NOT NULL,Personnel_Password VARCHAR(25) NOT NULL,Personnel_Tel_No VARCHAR(25),Personnel_Email_Address VARCHAR(25),Personnel_Country VARCHAR(25),Personnel_City_Of_Residence VARCHAR(25),Personnel_DOB DATE,Personnel_Gps_Location_Long DECIMAL(10,2),Personnel_Gps_Location_Lat DECIMAL(10,2),Personnel_Date_Of_Registration TIMESTAMP NOT NULL,Personnel_Facial_Reco BLOB)"
    ibm_db.exec_immediate(gidconnection,gid_personnel_sql)
except:
    print( "personnel table couldn't be completed:" , ibm_db.stmt_errormsg())
else:
    print ("personnel table completed.")


#Create todo_tasks table
try:

    gid_todotasks_sql="CREATE TABLE todo_tasks(Task_Id_No INTEGER PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY(START WITH 1, INCREMENT BY 1),Personel_Employer_Identity INTEGER NOT NULL,Task_Category VARCHAR(25),Task_Name VARCHAR(25),Task_Description VARCHAR(250),Task_Requirements VARCHAR(250),Task_Gps_Location_Long DECIMAL(10,2),Task_Gps_Location_Lat DECIMAL(10,2),Task_Budget_Amount DECIMAL(10,2),Task_Budget_Currency VARCHAR(25),Task_Date_Of_Post  TIMESTAMP NOT NULL,Task_Deadline DATE)"

    ibm_db.exec_immediate(gidconnection,gid_todotasks_sql)
except:
    print( "todo tasks couldn't be completed:" , ibm_db.stmt_errormsg())
else:
    print ("todo tasks table completed.")
#Create expert table
try:
    gid_expert_sql="CREATE TABLE experts(Personnel_Expert_Id_No INTEGER PRIMARY KEY NOT NULL,Expert_Purpose_And_Desires VARCHAR(250),Expert_Qualifications VARCHAR(250),Expert_Skills VARCHAR(250),Expert_Interests_And_Hobbies VARCHAR(250),Expert_Referee_Name VARCHAR(25),Expert_Referee_Contact VARCHAR(25),Expert_Facial_Reco BLOB)"
    ibm_db.exec_immediate(gidconnection,gid_expert_sql)
except:
    print( "expert table couldn't be completed:" , ibm_db.stmt_errormsg())
else:
    print ("expert table completed.")
#Create done_tasks table
try:

    gid_donetasks_sql="CREATE TABLE done_tasks(Task_Id_No INTEGER PRIMARY KEY NOT NULL,Personnel_Expert_Id_No INTEGER NOT NULL,Date_Task_Done TIMESTAMP NOT NULL)"

    ibm_db.exec_immediate(gidconnection,gid_donetasks_sql)
except:
    print( "done tasks table couldn't be completed:" , ibm_db.stmt_errormsg())
else:
    print ("done tasks table completed.")
"""   
