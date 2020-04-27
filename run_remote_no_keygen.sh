#!/bin/bash
echo "Copying required files to the server"
scp src/catalogServer.py $USER@elnux3.cs.umass.edu:~/
scp src/orderServer.py $USER@elnux7.cs.umass.edu:~/
scp src/frontendServer.py $USER@elnux1.cs.umass.edu:~/

echo "Running catalog server on elnux3"
ssh $USER@elnux3.cs.umass.edu 'nohup python3 catalogServer.py > foo.out 2> foo.err < /dev/null &'

echo "Running order server on elnux 7"  
ssh $USER@elnux7.cs.umass.edu 'nohup python3 orderServer.py > foo.out 2> foo.err < /dev/null &'  

echo "Running front end server on elnux1"
ssh $USER@elnux1.cs.umass.edu 'nohup python3 frontendServer.py > foo.out 2> foo.err < /dev/null &'

echo "Running client"
python3 src/client1.py

