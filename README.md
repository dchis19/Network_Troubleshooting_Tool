Author: Daniel Chisner
Date Modified: 2023 March 30
Python Version: Python 3.10.0

# Network_Troubleshooting_Tool
This program enables faster troubleshooting and a visualization of issues on the network. 

To utilize the program, you must install Python3 then Tkinter onto your host device. 

To download Tkinter use "pip install tk" (delete the quotations marks when attempting to download) in the command line. 

    pip install tk

There are three features to this program, 
  1) Traceroute which generates the route to Google's 8.8.8.8 server and displays the route as a series of boxes for each hop/IP the traffic goes through.
  2) Standard ping which takes a users IP address they would like to ping.
  3) Continuous monitoring based on a list of IPs provided in the listOfIPsCONSTANT.txt file. This generates boxes based on ping results. If a connection
     fails, a red box is shown on the screen along with the site and IP address. If a successful connection was made, the box is shown as green. The
     pings are repeated every 5 minutes. 
     
BEFORE USE: 
  FOR BOTH BELOW STATEMENTS USE THE FOLLOWING FORMAT IN THE .TXT FILES:
      Name of Location or Router or Server: IP Adress
      
      Example:
          Google: 8.8.8.8
          
  1) If using the constant monitoring feature, please change the IP and associated name on the listOfCONSTANT.txt file. 
  2) Update the listOfIPsALL.txt file with every possible known IP that traffic may go through. This will enable a names to be displayed on the
     traceroute making troubleshooting simpler. 
     

NOTE ON TRACEROUTE: 
  1) The IP is set to 8.8.8.8 and must be manually changed in the .py file. This is to intentionally to reduce user error and to ensure the user is
     connecting to a well managed/redundant connection. 
  2) The max hops is set to 20 and must be manually changed in the .py file. 

