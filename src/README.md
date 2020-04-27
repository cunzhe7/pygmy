# 677 Lab 3

This directory should contain your source code. Be sure to include comments in your code for us to understand it.
Running the code - 
This assumes that you have flask installed which can be done using `pip3 install --user flask`
There are three ways to run this code using three different scripts present in the project folder, a level before the src directory - 
 - We have provided the primary runscript which is run_remote_edlab. It helps setup the ssh key which should be set without an rsa file and no passphrase i.e. press enter when prompted to enter either and leave them blank. Logs for all the servers can be found under lab-2-li-patel/logs/serverName.log. The primary runscript also runs all the tests before starting the actual client so that it can be confirmed that the tests are running. 
 - The other two runscripts are back up runscripts that need to be run in the case the primary runscript fails. 

1. Run with ssh-keygen - To do this run `bash run_remote_edlab.sh` from the lab-3-lab-3-li-patel directory to ensure the client runs. 
    - This is the primary runscript and can be run both on your local machine as well as edlab, it will detect your environment and act accordingly. 
    - This script prompts you for the rsa file name and passphrase for ssh-keygen. Just press enter for both, don't input anything. 
    - Enter Y for a yes/no question in case it asks. 
    - It will copy the keys to the servers, it will prompt you to enter your password, please enter that. 
    - It will proceed to copy and run the files on different servers. Since there is no port discovery the ports we use are static and have to be free. The port in question is 35401 as assigned to us. 
    - The tests will then run to ensure all the servers are running fine. 
    - The client runs on this machine as followed by the tests. 
2. Run the script from local `bash run_remote_edlab.sh`
    - This script will start a client on your local machine and run the servers on edlab. 
    - It is the same as above but prompts for username. 
    
Notes to consider - 
1. Please make sure that the scripts have correct permissions and you don't get the permission denied error. 
