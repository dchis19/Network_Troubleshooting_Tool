from subprocess import Popen, PIPE
import sys
import re
import turtle
from turtle import Screen
from turtle import title
import time

TURTLE_SIZE = 20

'''
Author: Daniel Chisner
Date Updated: 2023 March 30

This project provides general network troubleshooting and monitoring. Three options exist. 

1) Allows users conduct a traceroute out of the LAN/II MEF WAN and ping Google's 8.8.8.8 server. The IPs of the 
routers are then stored in an array and used to generate a list of connections on the turtle screen to assist in 
visualizing where network traffic is failing/going

2) A simple ping test using the IP of a user's preference

3) A list of IPs are routinely pinged to see their connectivity and demonstrate when networks may be down at the 
distant end to assist in monitoring in the Systems Control room. 
'''

#Takes the turtle to the left corner of the screen
def goToCorner(t, screen):
    return t.goto(TURTLE_SIZE/2 - screen.window_width()/2, screen.window_height()/2 - TURTLE_SIZE/2-50)

#Lifts turtle to stop it from drawing on screen
def up(t):
    return t.penup()

#Enables turtle to draw on screen
def down(t):
    return t.pendown()

#Search for designated value (Linear search is used as N is small)
def linearSearch(arr, x):
    for i in range(0,len(arr)):
        if arr[i] == x:
            return i
    return -1

#Checks turtle location on screen. If too far right, the turtle moves to the left of the screen
#If turtle is not too far right, then the turtle moves 140 spots to the right on the screen
def checkTurtleLocation(t, screen, test, kind):
    up(t)
    if t.xcor() >= (screen.window_width()/2 -200):
        if kind == "Trace":
            down(t)
            for _ in range(3):
                t.forward(110)
                t.right(90)
            t.right(90)
        t.goto(TURTLE_SIZE/2 - screen.window_width()/2, t.ycor() - 140)
        test = False 
    if test == True:
        if kind == "Trace":
            down(t)
        t.forward(140)
    down(t)
    return t, test

#Created a colored box on the screen
def colorBox(t, screen, word, color, lst, test, kind):
    style = ('Courier', 10, 'bold')
    t.fillcolor(color)
    t, test = checkTurtleLocation(t, screen, test, kind)
    test = True
    t.begin_fill()
    for _ in range(4):
        if _ == 1:
            t.write(word, align= "right", font=style)
        if _ == 2:
                t.write(lst[0], align= "right", font=style)
        t.forward(110)
        t.right(90)
    t.end_fill()
    return t, test

#Run traceroute and represent the route on turtle. 
#*************************************************************************
#NOTE (SEE POPEN COMMAND ON LINE 93): 
#      1) CHANGE TRACEROUTE TO CORRECT COMMAND IF CHANGING TO WINDOWS!!!! Currently set up for Mac
#      2) OPTIONAL: MAX HOPS SET TO 20 TO ENABLE FASTER TIME OUT IF REQUIRED
#************************************************************************
def testTraceRoute(host=None):
    temp = []
    listOfIPs = []
    namesOfIPs = []
    pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})') #pattern to find IP format
    output1 = ""
    p = Popen(['traceroute', '-m', '20', host], stdout=PIPE) #traceroute command 
    while True: 
        try:
            output = p.stdout.read() #read output and store it
            output1 = output.decode() #convert output to readable format
            if not line:
                break
        except:
            break
    temp = pattern.findall(output1) #Finds all IPs in the output
    for i in range(0,len(temp)): #Append just the IPs to listOfIPs array
        n = len(listOfIPs)-1
        if i == 0:
            listOfIPs.append(temp[i])
        if temp[i] != listOfIPs[n]:
            listOfIPs.append(temp[i])
    file1 = open('listOfIPsALL.txt', 'r')
    lines = file1.readlines()

    #remove paragraph "\n" from each string in lines array
    for n in range(0,len(lines)):
        string = lines[n].replace('\n', '')
        lines[n] = string

    #Searches the file containing all known IPs and stores the name if found based on IP matching
    #between the traceroute and the IP file. 
    for m in range(0, len(lines)):
        temp = pattern.findall(lines[m])
        indexOfLines = linearSearch(listOfIPs,temp[0])
        if indexOfLines != -1:
            lines[indexOfLines] = lines[indexOfLines].replace(temp[0], '')
            namesOfIPs.append(lines[indexOfLines])
        else:
            namesOfIPs.append(" ")

    screen = Screen() #Create screen
    t = turtle.Turtle() #Create turtle as "t"
    turtle.title("Display of Trace Route to 8.8.8.8")
    test = False
    kind = "Trace"
    for i in range(0,len(listOfIPs)):
        if i == 0:
            up(t)
            goToCorner(t, screen)
            down(t)
        lst = []
        lst.append(listOfIPs[i])
        t, test = colorBox(t, screen, namesOfIPs[i], "green", lst, test, kind) #crete a green box to resemble a router
        if i == 0:
            up(t)
            t.forward(10)
            down(t)
            test = True
        lst.pop()
    screen.mainloop() #keeps screen open until closed

#Conducts a ping test
def ping(host=None):
    p = Popen(['ping', host,'-c','1',"-W","2"])
    p.wait()
    if p.poll():
        return True
    else:
        return False

#Runs a ping every 5 minutes based on IPs in listOfIPsCONSTANT.txt file. If a conneection is made, the box
#is shown as green. Else, the box is drawn as red.
def continuous(lines,t):
    screen = Screen()
    t.reset() #Clears the screen of previous drawings
    t.hideturtle()
    t.speed(0) #set to fastest speed. DO NOT CHANGE
    up(t)
    goToCorner(t,screen) #Start in corner
    down(t)
    test = False

    #Reads lines from text file, extracts the IP, and calls a ping
    for line in lines:
      pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
      lst = pattern.findall(line)
      regex = r"([a-zA-Z])"
      match = re.findall(regex,line)
      word = ""
      kind = "continuous"
      for c in match:
        word = word + c

      #if ping fails, create a red square
      if ping(lst[0]) == True:
          t, test = colorBox(t, screen, word, "red", lst, test, kind)

      #else create a green square
      else: 
          t, test = colorBox(t, screen, word, "green", lst, test, kind)

#shows a timer in the cmd line and runs for the time passed into the function
def countdown(time_sec):
  while time_sec:
    mins, secs = divmod(time_sec, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    print(timeformat, end='\r')
    time.sleep(1)
    time_sec -= 1

if __name__ == '__main__':
  #while selection does not equal 1,2,3, the user is  asked for their input
  try:
      userInput = 0
      while userInput not in [1,2,3]:
          userInput = int(input("What would you like to test? \n\t(1)"
            "Full network connectivity out of II MEF? \n\t(2) To a II"
            "MEF/2d MAW router? \n\t(3) Monitor MWCS-28 site connectivity continuously?\n\n"))
          if userInput == 1:
            testTraceRoute('8.8.8.8')
          elif userInput == 2:
            ip = str(input("\n\nWhat is the IP you are trying to ping?"))
            if ping(ip) == True:
              print(f'\n\nFAILED TO CONNECT TO {ip}. TROUBLESHOOT NETWORK.')
            else: 
              print(f'\n\nConnected to {ip}. \nIf site is reporting problem, '
                'they should internally troubleshoot.')
          elif userInput == 3:
            t = turtle.Turtle()
            turtle.title("USE CTRL+C IN CMD LINE TO KILL PROGRAM")
            file1 = open('listOfIPsCONSTANT.txt', 'r')
            lines = file1.readlines()
            continuous(lines, t)
            for i in range(0,1000000000000): #Start 5 minute timer and run continuous method 1000000000000 times
              countdown(300) #300 seconds = 5 minutes
              continuous(lines, t)
  except:
      print("Sorry, there was an error with your input or input file. Please check these and make corrections.")