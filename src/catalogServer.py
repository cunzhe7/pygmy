from flask import Flask, request
import sqlite3
import urllib.request
from sqlite3 import Error
from flask import json
import os
import time
import threading
import logging 
import sys
from Book import Book

logging.basicConfig(filename='./lab-3-lab-3-li-patel/logs/catalogserver.log',level=logging.DEBUG)
db_name = "trial"
app = Flask(__name__)

frontend = "http://elnux1.cs.umass.edu:35402/"
clb = "http://elnux3.cs.umass.edu:35403/"

DELETE_BOOKS="DROP TABLE IF EXISTS BOOKS;"
CREATE_BOOKS="CREATE TABLE IF NOT EXISTS BOOKS (id integer primary key, name text NOT NULL, topic text NOT NULL, quantity INTEGER NOT NULL, price INTEGER NOT NULL);"
INSERT_SQL=sql = ''' INSERT INTO BOOKS(name,topic,quantity,price)
              VALUES(?,?,?,?) '''
INSERT_SQL_UPDATE=sql = ''' INSERT INTO BOOKS(id, name,topic,quantity,price)
              VALUES(?,?,?,?,?) '''

"""
    This file needs to create two parts query and update - 
        1. Query by topic and 
        2. Query by item number 
    It needs to perform update in case orderz server decides to call buy.
        1. Perform update on database. 
"""
def create_connection(db_file):
    """Create connection to sqlite db"""
    print(db_file)
    try:
        conn = sqlite3.connect(db_name)
        print(sqlite3.version)

        c = conn.cursor()
        # Delete the database if it exists
        c.execute(DELETE_BOOKS)
        c.execute(CREATE_BOOKS)

        # Initialize the Database with books name, quantity and price
        count = 0
        c.execute(INSERT_SQL, ( "How to get a good grade in 677 in 20 minutes a day","distributed systems",1000,100))
        c.execute(INSERT_SQL, ("RPCs for Dummies","distributed systems",1000,1000))
        c.execute(INSERT_SQL, ("Xen and the Art of Surviving Graduate School","graduate school",1000,1000))
        c.execute(INSERT_SQL, ("Cooking for the Impatient Graduate Student","graduate school",1000,1000))
        c.execute(INSERT_SQL, ("How to finish Project 3 on time","graduate school",1000,1000))
        c.execute(INSERT_SQL, ("Why theory classes are so hard.","distributed systems",1000,1000))
        c.execute(INSERT_SQL, ("Spring in the Pioneer Valley","graduate school",1000,1000))

        c.execute("SELECT * FROM BOOKS")
        rows = c.fetchall()

        for row in rows:
            print(row)
        conn.commit()
    except Error as e:
        print(e)
    
    finally:
        if conn:
            conn.close()

#Restore the current state to the state returned by the leader. 
def update_db(data):
    print("Updating",db_name)
    print(data)
    try:
        conn = sqlite3.connect(db_name)
        print(sqlite3.version)

        c = conn.cursor()
        # Delete the database if it exists
        c.execute(DELETE_BOOKS)
        c.execute(CREATE_BOOKS)

        # Initialize the Database with books name, quantity and price
        for row in data:
            values = data[row]
            c.execute(INSERT_SQL_UPDATE, (row,values[0], values[1], values[2], values[3]))
        

        c.execute("SELECT * FROM BOOKS")
        rows = c.fetchall()

        for row in rows:
            print(row)
        conn.commit()
    except Error as e:
        print(e)
    
    finally:
        if conn:
            conn.close()


def restock(db_file):
    # Restock the book periodically, but only restock sold out book
    while True:
        time.sleep(5)
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        sql = "SELECT * FROM BOOKS WHERE ID IN (1,2,3,4)"
        c.execute(sql)
        result = c.fetchall()
        # Check the stock for all books
        for i in range(4):
            # If the stock is 0, restock the book
            if result[i][3] == 0:
                c.execute("UPDATE BOOKS SET quantity = 100 WHERE ID ={}".format(i+1))
            # If the stock is negative, which should never happen, raise error message. 
            elif result[i][3] < 0:
                print("Something Wrong! Negative Stock!")
        c.fetchall()
        conn.commit()
        conn.close()
        print("Restocked!")

#Return the current state of the server to maintain consistency. 
@app.route("/getCurrentState")
def getCurrentState():
    print("Getting current state")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    books = {}
    c.execute("SELECT * FROM BOOKS")

    result = c.fetchall()
    conn.close()
    print("Finished executing")
    for row in result: 
        print(row[0], row[1], row[2], row[3], row[4])
        books[row[0]] = []
        books[row[0]].append(row[1])
        books[row[0]].append(row[2])
        books[row[0]].append(row[3])
        books[row[0]].append(row[4])
        
    print(books)
    return json.jsonify(items = books)



    

@app.route("/search/")
@app.route("/search/<topic>")
def search(topic = "*"):
    print("searching for {}".format(topic))
   
    print(request.remote_addr)
    print(request.environ)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Run select query based on topic
    logging.info("Obtained search request from " + str(request.remote_addr))
    if topic == "*":
        c.execute("SELECT * FROM BOOKS")
    else:
        c.execute("SELECT * FROM BOOKS WHERE topic=\""+ str(topic) + "\"")
    result = c.fetchall()
    conn.close()
    # Process the result into required format
    ret = {}
    for row in result:
        print(row)
        ret[row[1]] = row[0]
    return json.jsonify(items = ret)


@app.route("/lookup/<itemnumber>")
def lookup(itemnumber):
    print("Looking up")
    print(request)
    # Lookup will lookup sqlite for the item
    print("looking up for item#{}".format(itemnumber))
    logging.info("Obtained lookup request from " + str(request.remote_addr))
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "SELECT * FROM BOOKS WHERE ID="+itemnumber
    c.execute(sql)
    result = c.fetchall()
    conn.close()
    return json.jsonify(items = result)

@app.route("/update/<itemnumber>/<quantity>")
def update(itemnumber, quantity):
    print("updating for item:{}".format(itemnumber))
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Make sure we don't make the stock negative
    # sql = "UPDATE BOOKS SET quantity = CASE WHEN (quantity >= "+quantity+")" + "THEN quantity -"+ quantity + " ELSE quantity END " +" WHERE ID="+itemnumber
    sql = "UPDATE BOOKS SET quantity = quantity - {} WHERE ID = {}".format(quantity,itemnumber)    
    c.execute(sql)
    sql2 = "SELECT quantity FROM BOOKS WHERE ID="+itemnumber
    c.execute(sql2)
    # Do checking after update, if the stock is negative, don't commit that change
    result = c.fetchall()
    if result[0][0] < 0:
        conn.close()
        return "False"
    # If the stock is non-negative which means this update is valid, commit it 
    else:
        logging.info("Sold Item :" + str(itemnumber) + " and quantity: " + str(quantity) + "to ip address: " + str(request.remote_addr))
        print("Removing from ditributed cache")
        
        response = urllib.request.urlopen(frontend+"remove%20"+itemnumber).read().decode()
        print(response)
        conn.commit()
        
        print(response)
        print("Removed from cache")
        conn.close()
    return "True"

@app.route("/")
def live():
    return "Alive"    


hostname = 'elnux3.cs.umass.edu'
portnum = '35401'

if len(sys.argv) >= 2:
    print("Applying hostname and port")
    hostname = sys.argv[1]
    portnum = sys.argv[2]
    print("Updating hostname and port: ", hostname, portnum)

book = Book("","","","","")
db_name += hostname + str(portnum) + ".db"
# Initialize database
create_connection(db_name)

# Initialize restock thread
restockthread = threading.Thread(target = restock, args = (db_name,))
restockthread.start()

response = urllib.request.urlopen(clb+"add%20"+hostname+"%20"+portnum).read().decode()

#Update the database to make it consistent
if response != "True":
        result = json.loads(response)
        update_db_data = result["items"]
        print(update_db)
        update_db(update_db_data)

#Activate the instance by registering with the load balancer - two phase commit. 
response = urllib.request.urlopen(clb+"activate%20"+hostname+"%20"+portnum).read().decode()

app.run(host=hostname, port=portnum, threaded=True)
