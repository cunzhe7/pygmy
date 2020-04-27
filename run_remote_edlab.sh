#!/bin/bash
hostname=`hostname`
echo $hostname
if  [[ $hostname == elnux* ]] ;then
	user=$USER
else 
	echo "Enter username to start edlab servers: "
	read user
fi

echo "Generating ssh keys for propagration\n"
echo "Press enter without typing anything when prompted for passphrase and rsa filename if prompted for y/n please press y\n"
ssh-keygen 

echo "Copying public keys to required servers"
ssh-copy-id $user@elnux1.cs.umass.edu  
ssh-copy-id $user@elnux3.cs.umass.edu  
ssh-copy-id $user@elnux7.cs.umass.edu
 
echo 'Running catalog load balancer'
ssh $user@elnux3.cs.umass.edu 'nohup python3 ~/lab-3-lab-3-li-patel/src/loadBalancer.py > ~/lab-3-lab-3-li-patel/logs/catalogServerLogs 2> foo.err < /dev/null &'

echo 'Running order load balancer'
ssh $user@elnux3.cs.umass.edu 'nohup python3 ~/lab-3-lab-3-li-patel/src/orderLoadBalancer.py > ~/lab-3-lab-3-li-patel/logs/catalogServerLogs 2> foo.err < /dev/null &'

echo "Running catalog server on elnux3\n"
ssh $user@elnux3.cs.umass.edu 'nohup python3 ~/lab-3-lab-3-li-patel/src/catalogServer.py elnux3.cs.umass.edu 35415 > ~/lab-3-lab-3-li-patel/logs/catalogServerLogs 2> foo.err < /dev/null &'


echo "Running catalog server on elnux3\n"
ssh $user@elnux3.cs.umass.edu 'nohup python3 ~/lab-3-lab-3-li-patel/src/catalogServer.py elnux3.cs.umass.edu 35416 > ~/lab-3-lab-3-li-patel/logs/catalogServerLogs 2> foo.err < /dev/null &'

echo "Running order server on elnux 7\n"  
ssh $user@elnux7.cs.umass.edu 'nohup python3 ~/lab-3-lab-3-li-patel/src/orderServer.py elnux7.cs.umass.edu 35415 > ~/lab-3-lab-3-li-patel/logs/orderServerLogs 2> foo.err < /dev/null &'  


echo "Running order server on elnux 7\n"  
ssh $user@elnux7.cs.umass.edu 'nohup python3 ~/lab-3-lab-3-li-patel/src/orderServer.py elnux7.cs.umass.edu 35416 > ~/lab-3-lab-3-li-patel/logs/orderServerLogs 2> foo.err < /dev/null &'  

echo "Running front end server on elnux1\n"
ssh $user@elnux1.cs.umass.edu 'nohup python3  ~/lab-3-lab-3-li-patel/src/frontendServer.py > ~/lab-3-lab-3-li-patel/logs/frontendServerLogs 2> foo.err < /dev/null &'

echo "Running tests to make sure everything works, these tests shouldn't fail: \n"

#python3 tests/frontendTests.py

echo "\n"
echo "Running client\n"
python3 src/client1.py

