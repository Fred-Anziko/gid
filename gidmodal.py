import ibm_db
import psycopg2

########MODAL/DATABASE########BEGINS
#connection to the PostgreSQL giddatabase.db file

gidconnection= ibm_db.connect("DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-15.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=wtg44875;PWD=x0@jrhzljmp7996f;","","")
#except:
#     gidconnection=psycopg2.connect(dbname="giddatabase", user="postgres", password="Afeku demetrio2020")
##creat Database tables in giddatabase begins##
#gidcursor=gidconnection.cursor()
# Create employers table
"""{
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
}"""
try:
    gidemployee_sql="CREATE TABLE employer(Employer_Id_No INTEGER PRIMARY KEY, Employer_First_Name TEXT,Employer_Last_Name TEXT,Employer_User_Name TEXT UNIQUE NOT NULL,Employer_Password TEXT NOT NULL,Employer_Tel_No TEXT,Employer_Email_Address TEXT,Employer_Country TEXT,Employer_City_Of_Residence TEXT,Employer_Gps_Location REAL NOT NULL,Employer_Date_Of_RegistrationTIMESTAMP NOT NULL)"
    ibm_db.exec_immediate(gidconnection,gidemployee_sql)
except:
    pass

# Create tasks table for holding task posting and updating details
try:
    gidtasks_sql="CREATE TABLE tasks(Task_Id_No INTEGER PRIMARY KEY,Employer_Identity INTEGER NOT NULL,Task_Category TEXT,Task_Name TEXT,Task_Description TEXT,Task_Requirements TEXT,Task_Gps_Location REAL,Task_Budget_Amount REAL,Task_Budget_Currency TEXT,Task_Date_Of_Post TIMESTAMP NOT NULL,Task_Deadline DATE, FOREIGN KEY (Employer_Identity) REFERENCES employers (Employer_Id_No))"
    ibm_db.exec_immediate(gidconnection,gidtasks_sql)
except:
    pass

# Create personnel table
try:
    gidpersonnels_sql="CREATE TABLE personnels(Personnel_Id_No INTEGER PRIMARY KEY,Personnel_First_Name TEXT,Personnel_Last_Name TEXT,Personnel_User_Name TEXT UNIQUE NOT NULL, Personnel_Password TEXT NOT NULL, Personnel_Tel_No TEXT, Personnel_Email_address TEXT,Personnel_Country TEXT,Personnel_City_Of_Residence TEXT, Personnel_Qualifications TEXT,Personnel_Experiences TEXT,Personnel_Skills TEXT,Personnel_Gps_Location REAL NOT NULL,Personnel_Date_Of_Registration TIMESTAMP NOT NULL)"
    ibm_db.exec_immediate(gidconnection,gidpersonnels_sql)
except:
    pass
##creat Database tables in giddatabase ends##
