from loadBalancer import loadBalancer
from flask import Flask 
import urllib.request
import threading
import logging 
class orderLoadBalancer(loadBalancer):
    def __init__(self):
        super().__init__()
    
    #Buy request specialization for order load balancer
    def buy(self, request):
        endpoint = self.getEndpoint()
        request = request.replace(" ", "/")
        request_final = endpoint+request
        print(request_final)
        return urllib.request.urlopen(request_final).read().decode()



def main():
    loadBalancerImpl = orderLoadBalancer()
    heartbeatThread = threading.Thread(target = loadBalancerImpl.heartbeat)
    heartbeatThread.start()
 
    app = Flask(__name__)
    @app.route("/<request>")
    def handle(request):
        print("Entered request")
        operation = str(request).split(' ')[0]
        if operation == 'add':
            print("Found method")
            host = str(request).split(' ')[1]
            port = str(request).split(' ')[2]
            return loadBalancerImpl.addInstance(host, port)
        elif operation == 'buy':
            return loadBalancerImpl.buy(request)
        else:
            return loadBalancerImpl.request(request)

    app.run(host='elnux3.cs.umass.edu', port=35404, threaded=True)


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
