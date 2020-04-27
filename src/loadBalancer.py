import threading
import urllib.request 
from flask import Flask
import socket
import time
from Book import Book
import logging


class Instance:
    # Each class will have a host port and an update queue. 
    host = None
    port = None
    update_queue = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.update_queue = []
    
    def add_to_queue(self, update):
        self.update_queue.append(update)
    
    def returnInstance(self):
        return "http://"+self.host+":"+self.port+"/"

    

"""
This is a thread safe load balancer class
"""
class loadBalancer:
    #Will have a list of active and dead instances. 
    instances = []
    roundRobin = 0
    numEndpoints = 0
    safetyLock = None
    
    def __init__(self):
        # Instantiate the loadbalancer with all URLs
        self.instances = []
        self.numEndpoints = len(self.instances)
        self.safetyLock = threading.Lock()

    #Round robin algorithm to return endpoint. 
    def getEndpoint(self):
        endpoint = self.instances[self.roundRobin % len(self.instances)].returnInstance()
        self.roundRobin += 1
        return endpoint
    
    #Update protocol for a consistent state in case we want to use the update queue. 
    #Can be done in place of our current algorithm but not being used. 
    def apply_updates(self, instance):
        while len(instance.update_queue) != 0:
            request = instance.update_queue.pop()
            request = request.replace(" ", "/")
            endpoint = instance.returnInstance()
            request_final = endpoint + request
            print(request_final)
            val = urllib.request.urlopen(request_final).read().decode()

    #Second phase of the two phase commit where the instance sends an activate request after reaching a consistent state. 
    def activateInstance(self, host, port):
        self.safetyLock.acquire()
        instance = Instance(host, port)
        print("Activating instance: ", instance.returnInstance())
        for existing_instance in self.instances:
            if existing_instance.returnInstance() == instance.returnInstance():
                self.safetyLock.release()
                return "True"
        self.instances.append(instance)
        self.safetyLock.release()
        return "True"

    #Method to add a new instance to the load balancer leader. 
    def addInstance(self, host, port):
        self.safetyLock.acquire()
        instance = Instance(host, port)
        
        for existing_instance in self.instances:
            if existing_instance.returnInstance() == instance.returnInstance():
                self.safetyLock.release()
                return "True"
       
        print("Adding hostname and portnum: ", host, port)
        self.instances.append(instance)
        self.numEndpoints += 1
        self.safetyLock.release()
        return "True"

    #Generic load balancer request for lookup and search calls.
    def request(self, request):
        print("Entered load balancer request")
        self.safetyLock.acquire()
        endpoint = self.getEndpoint()
        request = request.replace(" ","/",1)
        request = request.replace(" ","%20") 
        request_final = endpoint+request
        request_final = request_final.strip()
        logging.info("Making a request to: " + request_final)
        print("Request is:", request_final)
        
        # fault tolerance if 1 server is down and it hasn't been detected by the load balancer. 
        try:
            val = urllib.request.urlopen(request_final).read().decode()
        except socket.error:
            endpoint = self.getEndpoint()
            request_final = endpoint+request
            logging.info("Making a second request to: " + request_final)
            val = urllib.request.urlopen(request_final).read().decode()

        print(val)
        self.safetyLock.release()
        return val

    #Heartbeat function to detect if backend servers are down. It runs on a seperate thread every 1 second. 
    def heartbeat(self):
        while True:
            for endpoint in range(len(self.instances)):
                endp = self.instances[endpoint]
                #print("Instance: ", endp.returnInstance())
                try:
                    livemessage = urllib.request.urlopen(endp.returnInstance()).read().decode()
                except socket.error:
                    if endp in self.instances:
                        print("Removing from instances: ", endp.returnInstance(), endpoint)
                        self.safetyLock.acquire()
                        del self.instances[endpoint]
                        self.safetyLock.release()
                        break
                #if(livemessage=="Alive"):
                    #print("Alive")

            time.sleep(0.1)


class catalogLoadBalancer(loadBalancer):
    def __init__(self):
        super().__init__()

    def addInstance(self, host, port):
        self.safetyLock.acquire()
        instance = Instance(host, port)
        
        #Performing check for duplicate add. 
        for existing_instance in self.instances:
            if existing_instance.returnInstance() == instance.returnInstance():
                self.safetyLock.release()
                return "True"

        #If an instance already exists get the current state and replicate it to maintain consistency among instances. 
        if len(self.instances) > 0:
            endpoint = self.getEndpoint()
            request_final = endpoint+"getCurrentState"
            print(request_final)
            val = urllib.request.urlopen(request_final).read().decode()
            print(val)
            self.safetyLock.release()
            return val

        #logging.info("Obtained search request from " + str(request.remote_addr))
        logging.info("Added new instance at " + host + str(port))
        print("Adding hostname and portnum: ", host, port)
        self.instances.append(instance)
        self.numEndpoints += 1
        self.safetyLock.release()
        return "True"
    
    #Critical section update performed to all active catalog server instances
    def update(self, request):
        #Update the catalog server
        self.safetyLock.acquire()
        count = 0 
        
        #If there are no active instances return false
        if len(self.instances) <= 0:
            print("No instances registered")
            return "False"
        
        #Send request to all instances
        for instance in self.instances:
            instance.update_queue.append(request)
        

        for instance in self.instances:
            request = instance.update_queue.pop()
            request = request.replace(" ", "/")
            endpoint = instance.returnInstance()
            request_final = endpoint + request
            logging.info(request_final)
            print(request_final)
            val = urllib.request.urlopen(request_final).read().decode()
            if val == "True":
                count += 1
                
        
        #Handling case where no server could perform the update
        if count > 0:
            self.safetyLock.release()
            return "True"
        else:
            self.safetyLock.release()
            return "False"


def main(loadBalancerImpl):
    heartbeatThread = threading.Thread(target = loadBalancerImpl.heartbeat)
    heartbeatThread.start()
 
    app = Flask(__name__)
    

    @app.route("/<request>")
    def handle(request):
        print("Entered request", request)
        operation = str(request).split(' ')[0]
        if operation == 'add':
            print("Found method")
            host = str(request).split(' ')[1]
            port = str(request).split(' ')[2]
            return loadBalancerImpl.addInstance(host, port)
        elif operation == 'activate':
            print("Found method")
            host = str(request).split(' ')[1]
            port = str(request).split(' ')[2]
            return loadBalancerImpl.activateInstance(host, port)
            
        elif operation == 'update':
            return loadBalancerImpl.update(request)
        else:
            return loadBalancerImpl.request(request)
    
    #app.run(host='elnux3.cs.umass.edu', port=35403, threaded=True)
       
    app.run(host='elnux3.cs.umass.edu', port=35403, threaded=True)
    

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
    logging.basicConfig(filename='./lab-3-lab-3-li-patel/logs/catalogLoadBalancer.log',level=logging.DEBUG)
    loadBalancerImpl = catalogLoadBalancer()
    
    main(loadBalancerImpl)
