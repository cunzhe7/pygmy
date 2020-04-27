from flask import Flask
from http import client
import urllib.request
import logging 
from cache import Cache

logging.basicConfig(filename='./lab-3-lab-3-li-patel/logs/frontendServer.log',level=logging.DEBUG)


clb = "http://elnux3.cs.umass.edu:35403/"
olb = "http://elnux3.cs.umass.edu:35404/"

app = Flask(__name__)
cache = Cache()

#Call search on catalog server
def search(topic):
    val = cache.get(topic)
    if val != 0:
        return val
    
    print("Client searching: {}".format(str(topic)))
    logging.info("Client searching: {}".format(str(topic)))
    #endpoint = catalogLoadbalancer.getEndpoint()
    val = urllib.request.urlopen(clb+"search%20"+topic).read().decode()
    cache.put(topic, val)
    return val

#Call lookup on catalog server
def lookup(item):
    print("Lookup request")
    print(item)
    val = cache.get(item)
    print("Got val from cache : ", val) 
    if val != 0:
        return val
    print("Client looking up: book#{}".format(item))
    logging.info("Client looking up: book#{}".format(item))
    
    
    val = urllib.request.urlopen(clb+"lookup%20"+item).read().decode()
    cache.put(item, val)
    return val

#Call buy on order server
def buy(item,quantity):
    print("Client buying: book#{} with quantity: {}".format(item, quantity))
    logging.info("Client buying: book#{} with quantity: {}".format(item, quantity))

    return urllib.request.urlopen(olb+"buy%20"+item+"%20"+quantity).read().decode()


def removeCacheKey(key):
    print("Remove request for key: ", key)
    cache.erase(key)
    return key

@app.route("/")
def instruction():
    print("front end hit")
    return "Hello there, you can search, lookup, or buy!"

@app.route("/<request>")
def handle(request):
    # process the input string and make it to list
    operation = str(request).split(' ')
    # Checking the first element of the list to decide on operation
    if operation[0]=="search":
        # Checking input availability
        if len(operation) < 2 or operation[1] == "":
            return search("")
        # Process the catagory name again
        topic = '%20'.join(operation[1:])
        # Search with the topic
        return search(topic)
    elif operation[0] == "lookup":
        if len(operation) < 2 or operation[1] == "":
            return "What do you want to lookup?"
        item = operation[1]
        try:
            int(item)
        except ValueError:
            return "Wrong value!"
        return lookup(item)
    elif operation[0] == "remove":
        key = operation[1]
        print("Remove request key is: ", key)
        removeCacheKey(key)
        return "True"
    elif operation[0] == "buy":
        # We implemented buy with quantity for testing
        if len(operation) not in range(2,4) or operation[1] == "":
            return "What do you want to buy?"
        item = operation[1]
        # if quantity flied was entered, the the quantity
        if len(operation) > 2:
            quantity = operation[2]
        # else the default quantity to buy it 1
        else:
            quantity = str(1)
        # Check if the input is available
        try:
            int(quantity+item)
        except ValueError:
            return "Wrong value!"
        # Prevent client from adding stocks
        if int(quantity) <= 0:
            return "Wrong quantity"
        return buy(item, quantity)
    # if the operation is not defined, return error message 
    else:
        return "we don't have that service"


#orderLoadbalancer = loadBalancer(["http://elnux7.cs.umass.edu:35401/", "http://elnux7.cs.umass.edy:35402/"])

app.run(host='elnux1.cs.umass.edu', port=35402, threaded=True)
