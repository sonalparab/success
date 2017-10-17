import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

def populate(file):
    reader = csv.reader(open(file,'rU'))
    #get the table name
    name = file.split('.csv')[0]
    #get the table fields
    row = next(reader)
    field0 = row[0]
    field1 = row[1]
    field2 = row[2]
    command = "CREATE TABLE " + name + " ("
    command += field0 + " TEXT,"
    command += field1 + " INTEGER,"
    command += field2 + " INTEGER"
    command += ");"
    #print command
    c.execute(command)
    reader = csv.DictReader(open(file,'rU'))
    #add the table values
    for row in reader:
        command = "INSERT INTO " + name + " VALUES ("
        command += "'" + row[field0] + "', "
        command += row[field1] + ","
        command += row[field2]
        command += ");"
        #print command
        c.execute(command)
    

#command = ""          #put SQL statement in this string
#c.execute(command)    #run SQL statement

populate("courses.csv")
populate("peeps.csv")

#==========================================================
db.commit() #save changes
db.close()  #close database


