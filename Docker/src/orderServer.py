from flask import Flask
import sys
import urllib.request
import json
import logging 
import random
# logging.basicConfig(filename='./lab-3-lab-3-li-patel/logs/frontendServer.log',level=logging.DEBUG)

clb = "http://127.0.0.1:35403/"
olb = "http://127.0.0.1:35404/"
app = Flask(__name__)

@app.route("/buy/<itemnumber>/<quantity>")
def buy(itemnumber, quantity):
    print("selling item #{}".format(itemnumber))
    logging.info("selling item #{}".format(itemnumber))

    #Lookup book on catalog server
    item = json.loads(query(itemnumber))
    if item['items'] != []:
        #Check if the item is in stock
        stock = item['items'][0][3]
        name = item['items'][0][1]
        print("Stock is: " + str(stock) + " before selling")
        if stock >= int(quantity):
            #Update with the database, non-atomic
            bought = update(itemnumber, quantity)
            if bought == "True":
                logging.info("Fulfilling order for book: {} with quantity {}".format(name, quantity))
                return "Bought book: {} with quantity {}!".format(name,quantity)
            else:
                logging.info("Unable to buy book: {}".format(name))
                return "Bought failed because book is not available!"
        else:
            #Handle edge cases
            logging.info("Book not in stock")
            return "We don't have that many in stock!"
    else:
        #Handle validations
        return "We don't sell that!"
    
@app.route("/")
def live():
    return "Alive"    



def query(inum): # Lookup query
    return urllib.request.urlopen(clb+"lookup%20"+inum).read().decode()

def update(inum, quantity): # Update catalog server
    return urllib.request.urlopen(clb+"update%20"+inum+"%20"+quantity).read().decode()



hostname = '127.0.0.1'
portnum = str(random.randint(35400,40000))

if len(sys.argv) >= 2:
    print("Applying hostname and port")
    hostname = sys.argv[1]
    portnum = sys.argv[2]
    print("Updating hostname and port: ", hostname, portnum)


urllib.request.urlopen(olb+"add%20"+hostname+"%20"+portnum)        
app.run(host=hostname ,port=portnum, threaded=True)
