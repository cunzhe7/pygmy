Docker images:
https://umass.box.com/s/ebk8d5f2mm5omjalwotz1mbaf8u9xyl1




To build by dockerfiles(alternative):

docker build -f Dockerfilefs --tag fs .
docker build -f Dockerfileclb --tag clb .
docker build -f Dockerfileolb --tag olb .
docker build -f Dockerfilecs --tag cs .
docker build -f Dockerfileos --tag os .


To load by save image files:

docker load < fs.tar.gz
docker load < clb.tar.gz
docker load < olb.tar.gz
docker load < cs.tar.gz
docker load < os.tar.gz

To run:
Once you have all images imported 


docker run -it -d --name olb1 --net=host  olb
docker run -it -d --name clb1 --net=host  clb
docker run -it -d --name fs1 --net=host fs
docker run -it -d --name cs1 --net=host cs
docker run -it -d --name cs2 --net=host cs
docker run -it -d --name os1 --net=host os
docker run -it -d --name os2 --net=host os



To stop all:
docker rm --force os2 os1 cs2 cs1 fs1 olb1 clb1

To Test:

start a seperate python container by:
docker run -it -a --name client1 --net=host python:alpine


paste the code and test by simple input like "buy 1", "lookup 1"

import urllib.request


fs = "http://127.0.0.1:35402/"

while True:
    operation = input()
    operation = operation.replace(' ', '%20')
    print(urllib.request.urlopen(fs+operation).read().decode())




docker build -f Dockerfilefs --tag fs .

frontend server port 35402 

docker build -f Dockerfileclb --tag clb .

clb port 35403 


docker build -f Dockerfileolb --tag olb .

olb port 35404 


docker build -f Dockerfilecs --tag cs .

catalog server random 


docker build -f Dockerfileos --tag os .

order server random



To save:

to compress:
docker save fs | gzip > fs.tar.gz

docker save -o fs.tar fs
docker save -o os.tar os
docker save -o cs.tar cs
docker save -o clb.tar clb
docker save -o olb.tar olb



docker save fs | gzip > fs.tar.gz
docker save os | gzip > os.tar.gz
docker save cs | gzip > cs.tar.gz
docker save clb | gzip > clb.tar.gz
docker save olb | gzip > olb.tar.gz


To load: 

docker import fs.tar


To run:
Once you have all images imported 


docker run -it -d --name olb1 --net=host  olb
docker run -it -d --name clb1 --net=host  clb
docker run -it -d --name fs1 --net=host fs
docker run -it -d --name cs1 --net=host cs
docker run -it -d --name cs2 --net=host cs
docker run -it -d --name os1 --net=host os
docker run -it -d --name os2 --net=host os






To stop all:
docker rm --force os2 os1 cs2 cs1 fs1 olb1 clb1


start another client by python3 basicClient.py
Docker Desktop for Mac can’t route traffic to containers. may need linux environment or another image to start basicClient.

Used another python:alpine container to be client, and run the basicClient. 



docker attach [name] to check messages