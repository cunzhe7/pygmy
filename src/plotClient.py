import time
from matplotlib import pyplot
import urllib.request
import random

random.seed(17)

fs = "http://127.0.0.1:5002/"


timeList = []

for i in range(1000):
    t1 = time.time()
    print(urllib.request.urlopen(fs+"buy%20{}".format(random.randint(1,3))).read().decode())
    timeList.append(time.time()-t1)

meanValue = sum(timeList) / 1000
pyplot.plot(timeList)
pyplot.xlabel("Frequency")
pyplot.ylabel("Time (s)")
pyplot.title("client average response time: {}".format(meanValue))
pyplot.show()