import ibm_db
import psycopg2

########MODAL/DATABASE########BEGINS
gidconnection=False
#connection to the DB2 database for gidweb on IBM cloud
try:
    gidconnection= ibm_db.pconnect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=wtg44875;PWD=x0@jrhzljmp7996f;","","")
except:
    print( "No connection:" , ibm_db.conn_errormsg())
else:
    print ("Connection established.")
#except:
#     gidconnection=psycopg2.connect(dbname="giddatabase", user="postgres", password="Afeku demetrio2020")
##creat Database tables in giddatabase begins##
#gidcursor=gidconnection.cursor()


"""DB2 CONNECTION PARAMETERS ON IBM CLOUD FOUNDRY
  "db": "BLUDB",
  "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=wtg44875;PWD=x0@jrhzljmp7996f;",
  "host": "dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net",
  "hostname": "dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net",
  "https_url": "https://dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net:8443",
  "jdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net:50000/BLUDB",
  "parameters": {
    "role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager"
  },
  "password": "x0@jrhzljmp7996f",
  "port": 50000,
  "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=wtg44875;PWD=x0@jrhzljmp7996f;Security=SSL;",
  "ssljdbcurl": "jdbc:db2://dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net:50001/BLUDB:sslConnection=true;",
  "uri": "db2://wtg44875:x0%40jrhzljmp7996f@dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net:50000/BLUDB",
  "username": "wtg44875"
"""
"""Create employers table
try:
    gidemployee_sql="CREATE TABLE employer(Employer_Id_No INTEGER PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY(START WITH 1, INCREMENT BY 1), Employer_First_Name VARCHAR(25),Employer_Last_Name VARCHAR(25),Employer_User_Name VARCHAR(25) UNIQUE NOT NULL,Employer_Password VARCHAR(25) NOT NULL,Employer_Tel_No VARCHAR(25),Employer_Email_Address VARCHAR(25),Employer_Country CHAR,Employer_City_Of_Residence VARCHAR(25),Employer_Gps_Location DECIMAL(10,2) NOT NULL,Employer_Date_Of_Registration TIMESTAMP NOT NULL)"
    ibm_db.exec_immediate(gidconnection,gidemployee_sql)
except:
    print( "Transaction couldn't be completed:" , ibm_db.stmt_errormsg())
else:
    print ("Transaction complete.")


Create tasks table for holding task posting and updating details
try:
    gidtasks_sql="CREATE TABLE tasks(Task_Id_No INTEGER PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY(START WITH 1, INCREMENT BY 1),Employer_Identity INTEGER NOT NULL,Task_Category VARCHAR(25),Task_Name VARCHAR(25),Task_Description VARCHAR(250),Task_Requirements VARCHAR(250),Task_Gps_Location DECIMAL(10,2),Task_Budget_Amount DECIMAL(10,2),Task_Budget_Currency VARCHAR(25),Task_Date_Of_Post TIMESTAMP NOT NULL,Task_Deadline DATE)" # FOREIGN KEY (Employer_Identity) REFERENCES employers (Employer_Id_No))"
    ibm_db.exec_immediate(gidconnection,gidtasks_sql)
except:
    print( "Transaction couldn't be completed:" , ibm_db.stmt_errormsg())
else:
    print ("Transaction complete.")
Create personnel table
try:
    gidpersonnels_sql="CREATE TABLE personnels(Personnel_Id_No INTEGER PRIMARY KEY NOT NULL GENERATED ALWAYS AS IDENTITY(START WITH 1, INCREMENT BY 1),Personnel_First_Name VARCHAR(25),Personnel_Last_Name VARCHAR(25),Personnel_User_Name VARCHAR(25) UNIQUE NOT NULL, Personnel_Password VARCHAR(25) NOT NULL, Personnel_Tel_No VARCHAR(25), Personnel_Email_address VARCHAR(25),Personnel_Country VARCHAR(25),Personnel_City_Of_Residence VARCHAR(25), Personnel_Qualifications VARCHAR(250),Personnel_Experiences VARCHAR(250),Personnel_Skills VARCHAR(25),Personnel_Gps_Location DECIMAL(10,2) NOT NULL,Personnel_Date_Of_Registration TIMESTAMP NOT NULL)"
    ibm_db.exec_immediate(gidconnection,gidpersonnels_sql)
except:
    print( "Transaction couldn't be completed:" , ibm_db.stmt_errormsg())
else:
    print ("Transaction complete.")"""
