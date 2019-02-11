import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
from time import sleep
import time
import pyautogui
from pynput.mouse import Listener

yellow = (246,183,70)
green = (92,220,114)
red = (246, 118, 105)

clicked = False
firstTime = True

def PixelAt(x, y):
  w = Gdk.get_default_root_window()
  pb = Gdk.pixbuf_get_from_window(w, x, y, 1, 1)
  return pb.get_pixels()

currentpos = pyautogui.position()
print(currentpos)

x_off = 22
y_off = 23

def ampelMeasurement():
    sleep(2)
    currentmeasurementcolor = ""
    measurementTimeStart = 0
    global clicked,firstTime,x_off,y_off
    while(True):
        #print("loop")
        currentcolor = tuple(PixelAt(int(768 + x_off),int(611 + y_off)))
        #print(currentcolor)
        if currentcolor == yellow:
            if currentmeasurementcolor != "yellow":
                print("last ", currentmeasurementcolor, " duration was ", time.time() - measurementTimeStart)
                currentmeasurementcolor = "yellow"
                measurementTimeStart = time.time()

            #print("is yellow")
        elif currentcolor == red:
            if currentmeasurementcolor != "red  ":
                print("last ", currentmeasurementcolor, " duration was ", time.time() - measurementTimeStart)
                currentmeasurementcolor = "red  "
                measurementTimeStart = time.time()
            #print("is red")
        elif currentcolor == green:
            if currentmeasurementcolor != "green":
                print("last ", currentmeasurementcolor, " duration was ", time.time() - measurementTimeStart)
                currentmeasurementcolor = "green"
                measurementTimeStart = time.time()
            #print("is green")
    return

def ampel():
    sleep(2)
    global clicked,firstTime,x_off,y_off
    while(True):
        #print("loop")
        currentcolor = tuple(PixelAt(int(768 + x_off),int(611 + y_off)))
        #print(currentcolor)
        if currentcolor == yellow:
            #print("is yellow")
            clicked = False
        elif currentcolor == red:
            #print("is red")
            sleep(0.48)
            if clicked == False and firstTime == False:
                #print(time.time() - last_time)
                #last_time = time.time()
                pyautogui.click(clicks=4,interval=0.02)
                clicked = True
                #print("click")
            elif firstTime == True:
                firstTime = False
                clicked = True
        elif currentcolor == green:
            #print("is green")
            clicked = False
    return



class ClickEvent(object):
    pass
eventlist = []


level1_EventList = [(611,858,0),(940,697,5)]
level2_EventList = [( 684 , 855  , 0 ),( 619 , 856  , 4.2),( 683 , 853  , 1),( 937 , 728  , 0.3),( 956 , 691  , 3.8)]
level3_EventList = [( 941 , 760  , 0 ),
( 906 , 773  , 1 ),
( 847 , 770  , 0.6 ),
( 813 , 786  , 0.4 ),
( 809 , 819  , 0.4 ),
( 780 , 832  , 0.4),
( 720 , 837  , 0.5),
( 677 , 850  , 0.4),
( 613 , 859  , 0.5),
( 684 , 854  , 1.8),
( 714 , 837  , 0.4),
( 767 , 838  , 0.5),
( 807 , 821  , 0.5),
( 821 , 786  , 0.4),
( 846 , 774  , 0.5),
( 901 , 772  , 0.4),
( 937 , 754  , 0.4),
( 958 , 693  , 0.5)]
level4_EventList = [( 933 , 790  , 0 ),
( 812 , 786  , 1.26),
( 809 , 850  , 1.11),
( 615 , 853  , 0.9),
( 814 , 850  , 2),
( 828 , 785  , 1.6),
( 943 , 788  , 0.9),
( 956 , 692  , 0.9)]

def do_event(levelList):
    global x_off,y_off
    for evt in levelList:
        pyautogui.moveTo(evt[0]+x_off,evt[1]+y_off)
        sleep(evt[2])
        pyautogui.click()
    pass

def do_events():
    sleep(2)
    do_event(level1_EventList)
    sleep(8)
    do_event(level2_EventList)
    sleep(8)
    do_event(level3_EventList)
    sleep(8)
    do_event(level4_EventList)
    sleep(6)
    #ampel()
    pass

#do_events()
ampel()
#ampelMeasurement()


firstTimeEvent = True
last_timeevt = 0
print("Initialized")

def on_click(x,y,button,pressed):
    global firstTimeEvent,last_timeevt
    if pressed == True:
        #print(x, " - ", y, " pressed  " , pressed)
        evt = ClickEvent
        evt.x = x
        evt.y = y
        if firstTimeEvent == True:
            firstTimeEvent = False
            evt.time = 0
            last_timeevt = time.time()
        else:
            evt.time = time.time() - last_timeevt
            last_timeevt = time.time()
        eventlist.append(evt)
        print ("(",evt.x, ",", evt.y, " ,", evt.time,"),")

    pass


with Listener(on_click=on_click) as listener:
    #listener.join()
    print("a")