import psycopg2

########MODAL/DATABASE########BEGINS
#connection to the PostgreSQL giddatabase.db file
try:
    gidconnection=psycopg2.connect(dbname="giddatabase", user="anzikofred@gmail.com", password="Afeku demetrio2020", host="ibm", port="5432")
except:
     gidconnection=psycopg2.connect(dbname="giddatabase", user="postgres", password="Afeku demetrio2020")
##creat Database tables in giddatabase begins##
gidcursor=gidconnection.cursor()
# Create employers table

try:
    gidcursor.execute("""CREATE TABLE employers
                      (Employer_Id_No INTEGER PRIMARY KEY, 
                     Employer_First_Name TEXT, 
                     Employer_Last_Name TEXT,
                     Employer_User_Name TEXT UNIQUE NOT NULL,
                     Employer_Password TEXT NOT NULL,
                     Employer_Tel_No TEXT,
                     Employer_Email_Address TEXT,
                     Employer_Country TEXT,
                     Employer_City_Of_Residence TEXT,
                     Employer_Gps_Location REAL NOT NULL,
                     Employer_Date_Of_Registration TIMESTAMP NOT NULL)""")
except:
    pass

# Create tasks table for holding task posting and updating details
try:
    gidcursor.execute("""CREATE TABLE tasks
                     (Task_Id_No INTEGER PRIMARY KEY,
                     Employer_Identity INTEGER NOT NULL,
                     Task_Category TEXT,
                     Task_Name TEXT,
                     Task_Description TEXT,
                     Task_Requirements TEXT,
                     Task_Gps_Location REAL,
                     Task_Budget_Amount REAL,
                     Task_Budget_Currency TEXT,
                     Task_Date_Of_Post TIMESTAMP NOT NULL,
                     Task_Deadline DATE,
                     FOREIGN KEY (Employer_Identity) REFERENCES employers (Employer_Id_No))""")
except:
    pass

# Create personnel table
try:
    gidcursor.execute("""CREATE TABLE personnels
                     (Personnel_Id_No INTEGER PRIMARY KEY,
                     Personnel_First_Name TEXT,
                     Personnel_Last_Name TEXT,
                     Personnel_User_Name TEXT UNIQUE NOT NULL,
                     Personnel_Password TEXT NOT NULL,
                     Personnel_Tel_No TEXT,
                     Personnel_Email_address TEXT,
                     Personnel_Country TEXT,
                     Personnel_City_Of_Residence TEXT,
                     Personnel_Qualifications TEXT,
                     Personnel_Experiences TEXT,
                     Personnel_Skills TEXT,
                     Personnel_Gps_Location REAL NOT NULL,
                     Personnel_Date_Of_Registration TIMESTAMP NOT NULL)""")
except:
    pass
##creat Database tables in giddatabase ends##
