import sqlite3  
import csv       
import db_builder

f = "discobandit.db"
db = sqlite3.connect(f)
c = db.cursor()

def avg():
    ids = 0
    avgdict = {}
    for rowc in c.execute('SELECT * FROM courses;'):
        if(rowc[2] != ids):
            count = 0
            sum = 0
            ids = rowc[2]
        sum += rowc[1]
        count += 1
        avg = sum//count
        avgdict[ids] = avg
    print(avgdict)
    return avgdict
        
def adddata(dict):
    c.execute("CREATE TABLE peeps_avg(name TEXT, id INTEGER, avg INTEGER);")
    commandlist = []
    for rowp in c.execute('SELECT * FROM peeps;'):
        name = rowp[0]
        ids = rowp[2]
        avg = dict[ids]
        print("name:%s, id:%d, avg:%d" %(name,ids,avg))
        commandlist.append("INSERT INTO peeps_avg VALUES('%s', %d, %d);"\
                           %(name,ids,avg))
    for command in commandlist:
        c.execute(command)
        
def updateavg(ids):
    count = 0
    sum = 0
    for row in c.execute("SELECT * FROM courses WHERE id = %d"%(ids)):
        count += 1
        sum += row[1]
    avg = sum // count                      
    command = "UPDATE peeps_avg SET avg = %d WHERE id = %d;"%(ids,avg)
    c.execute(command)

def addrows(
    
adddata(avg())

db.commit()
db.close()
