import threading
# Our own cache implementation
# All our methods must be thread safe

class Cache:
    cache = {}

    cacheLock = threading.Lock()
    def __init__(self):
        self.cache = {}
   
    #Get method for the cache
    def get(self, key):
        print("Cache get!")
        self.cacheLock.acquire()
        if key in self.cache:
            self.cacheLock.release()
            return self.cache[key]
        else:
            self.cacheLock.release()
            return 0

    #Put method for the cache
    def put(self, key, value):
        self.cacheLock.acquire()
        if key not in self.cache:
            self.cache[key] = value
        self.cacheLock.release()
        return key

    #Remove from cache
    def erase(self, key):
        self.cacheLock.acquire()
        print("Calling cache delete for",key)
        if key in self.cache:
            print("Removing key: ",key)
            del self.cache[key]
        self.cacheLock.release()
        return 
