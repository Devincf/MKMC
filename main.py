import sys
from time import sleep
import time
import pyautogui
from pynput.mouse import Listener


recordName = ""
playbackName = ""

eventlist = []
firstTimeEvent = True
last_timeevt = 0


def on_click(x,y,button,pressed):
    global firstTimeEvent,last_timeevt
    
    if pressed == True:
        #print(x, " - ", y, " pressed  " , pressed)
        evt = []
        evt.append(x)
        evt.append(y)
        if firstTimeEvent == True:
            firstTimeEvent = False
            evt.append(0)
            last_timeevt = time.time()
        else:
            evt.append(time.time() - last_timeevt)
            last_timeevt = time.time()
        eventlist.append(evt)
        print ("(",evt[0], ",", evt[1], " ,", evt[2],"),")

        if len(eventlist) > 5:
            f = open("macro.txt","a+")
            f.write("%s=%d:%d:%d" % (recordName, eventlist[0][0],eventlist[0][1],eventlist[0][2] ) )
            for i in range(1,len(eventlist)):
                f.write("|%d:%d:%s" % (eventlist[i][0],eventlist[i][1],str(round(eventlist[i][2], 5)) ) )
            f.write("\r\n")
            f.close()
            sys.exit()

    pass

def do_event(levelList):
    for evt in levelList:
        pyautogui.moveTo(evt[0],evt[1])
        sleep(evt[2])
        pyautogui.click()
    pass

def does_macro_exist(name):
    f = open("macro.txt","r")
    lines = f.readlines()
    for line in lines:
        temp = line.split('=')
        if temp[0] == name:
            f.close()
            return temp[1]
    f.close()
    return False
    pass

if len(sys.argv) <= 1:
    print("See usage!")
    sys.exit()

if sys.argv[1] == "run":
    #Execute Macro
    if len(sys.argv) <= 2:
        print("Please specify the macro to be executed")
        sys.exit()
    playbackName = sys.argv[2]
    macro = does_macro_exist(playbackName)
    if macro == False:
        print("Macro:", playbackName, "doesnt exist, please see usage for more!")
        sys.exit()
    macro_list = []
    for segment in macro.split('|'):
        segment_values = segment.split(':')
        macro_list.append([int(segment_values[0]),int(segment_values[1]),float(segment_values[2])])
    do_event(macro_list)


elif sys.argv[1] == "rec":
    #Record new Macro
    if len(sys.argv) <= 2:
        print("Please specify the macro name")
        sys.exit()
    recordName = sys.argv[2]
    if does_macro_exist(recordName) != False:
        print("Macro", recordName, "already exists, please see usage for more!")
        sys.exit()
    with Listener(on_click=on_click) as listener:
        listener.join()
else:
    print("See usage!")
    sys.exit()



