# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 13:31:34 2021

@author: Anziko Fred
"""
import psycopg2

def giddataconnection():
    """connection to the database for gid"""
    try:
        gidconnection=psycopg2.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-04.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=bds31662;PWD=0hdl2dpsqpmt@mpl;","","")
    except:
       print("Connection denied")
    else:
        print ("Connection established.")
        return gidconnection

gidconnection=gidataconnection()
gidcursor=gidconnection.cursor()

"""Create personnel tables"""
try:
    gidcursor.execute("CREATE TABLE personnel(Personnel_Id_No INTEGER PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY(START WITH 1, INCREMENT BY 1), Personnel_First_Name VARCHAR(25),Personnel_Middle_Name VARCHAR(25),Personnel_Last_Name VARCHAR(25),Personnel_User_Name VARCHAR(25) NOT NULL,Personnel_Password VARCHAR(25) NOT NULL,Personnel_Tel_No VARCHAR(25),Personnel_Email_Address VARCHAR(25),Personnel_Country VARCHAR(25),Personnel_City_Of_Residence VARCHAR(25),Personnel_DOB DATE,Personnel_Gps_Location_Long DECIMAL(10,2),Personnel_Gps_Location_Lat DECIMAL(10,2),Personnel_Date_Of_Registration TIMESTAMP NOT NULL,Personnel_Facial_Reco BLOB)")
except:
    print( "personnel table couldn't be completed:")
else:
    print ("personnel table completed.")


#Create todo_tasks table
try:

    gidcursor.execute("CREATE TABLE todo_tasks(Task_Id_No INTEGER PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY(START WITH 1, INCREMENT BY 1),Personel_Employer_Identity INTEGER NOT NULL,Task_Category VARCHAR(25),Task_Name VARCHAR(25),Task_Description VARCHAR(250),Task_Requirements VARCHAR(250),Task_Gps_Location_Long DECIMAL(10,2),Task_Gps_Location_Lat DECIMAL(10,2),Task_Budget_Amount DECIMAL(10,2),Task_Budget_Currency VARCHAR(25),Task_Date_Of_Post  TIMESTAMP NOT NULL,Task_Deadline DATE);")
except:
    print( "todo tasks table couldn't be completed:")
else:
    print ("todo tasks table completed.")
#Create expert table
try:
    gidcursor.execute("CREATE TABLE experts(Personnel_Expert_Id_No INTEGER PRIMARY KEY NOT NULL,Expert_Purpose_And_Desires VARCHAR(250),Expert_Qualifications VARCHAR(250),Expert_Skills VARCHAR(250),Expert_Interests_And_Hobbies VARCHAR(250),Expert_Referee_Name VARCHAR(25),Expert_Referee_Contact VARCHAR(25),Expert_Facial_Reco BLOB);")
except:
    print( "expert table couldn't be completed:")
else:
    print ("expert table completed.")
#Create done_tasks table
try:

    gidcursor.execute("CREATE TABLE done_tasks(Task_Id_No INTEGER PRIMARY KEY NOT NULL,Personnel_Expert_Id_No INTEGER NOT NULL,Date_Task_Done TIMESTAMP NOT NULL);")

except:
    print( "done tasks table couldn't be completed:")
else:
    print ("done tasks table completed.")