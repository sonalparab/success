import sqlite3  
import csv       
import db_builder

f = "discobandit.db"
db = sqlite3.connect(f)
c = db.cursor()

def avgs():
    #start id at 0, since no id is 0
    ids = 0
    avgdict = {}
    #iterate through each row of courses
    for rowc in c.execute('SELECT * FROM courses;'):
        #since the courses are in order by id, if the id changes, reset count and sum
        if(rowc[2] != ids):
            count = 0
            sum = 0
            ids = rowc[2]
        sum += rowc[1]
        count += 1
        avg = sum//count
        avgdict[ids] = avg
    #print(avgdict)
    return avgdict
        
def adddata(dict):
    #create the peeps_avg table
    c.execute("CREATE TABLE peeps_avg(name TEXT, id INTEGER, avg INTEGER);")
    commandlist = []
    #iterate through each row of peeps
    for rowp in c.execute('SELECT * FROM peeps;'):
        name = rowp[0]
        ids = rowp[2]
        avg = dict[ids]
        #add the commands to a list to avoid interfering with the cursor
        commandlist.append("INSERT INTO peeps_avg VALUES('%s', %d, %d);"\
                           %(name,ids,avg))
    #execute the commands
    for command in commandlist:
        c.execute(command)

#prints the name, id, and avg for each person
def printavgs():
     for rowp in c.execute('SELECT * FROM peeps_avg;'):
        name = rowp[0]
        ids = rowp[1]
        avg = rowp[2]
        print("name:%s, id:%d, avg:%d" %(name,ids,avg))

def updateavg(ids):
    count = 0
    sum = 0
    #iterate through the rows of courses that have the given id to recalculate the avg
    for row in c.execute("SELECT * FROM courses WHERE id = %d"%(ids)):
        count += 1
        sum += row[1]
    avg = sum // count
    command = "UPDATE peeps_avg SET avg = %d WHERE id = %d;"%(avg,ids)
    c.execute(command)

#helper function to add a new row to the courses table
def add(code,mark,ids):
    c.execute("INSERT INTO courses VALUES ('%s',%s,%s);"%(code,mark,ids))

#helper function to check if a row from the csv already exists in the table
def exists(code,mark,ids):
    for rowc in c.execute("SELECT * FROM courses;"):
        if(rowc[0] == '%s'%(code) and rowc[1] == mark and rowc[2] == ids):
            return True
    return False
    
def addrows():
    #opens file that has new grades added
    reader = csv.DictReader(open('courses2.csv','rU'))
    #iterate through each row in the file
    for row in reader:
        code = row['code']
        mark = int(row['mark'])
        ids = int(row['id'])
        #if the row from the csv is not in the table, add it to table and update the
        # student's avg
        if (not(exists(code,mark,ids))):
            add(code,mark,ids)
            updateavg(ids)

            
adddata(avgs())
print("Original avgs")
printavgs()
print
addrows()
print("New avgs")
printavgs()


db.commit()
db.close()
