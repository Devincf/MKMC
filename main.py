import sys
from time import sleep
import time
from pynput.mouse import Button, Listener as MouseListener,     Controller as MouseController
from pynput.keyboard import Key, Listener as KeyboardListener,  Controller as KeyboardController


recordName = ""
playbackName = ""

eventlist = []
firstTimeEvent = True
last_timeevt = 0

mouse = MouseController()
keyboard = KeyboardController()

key_listener = 0
mouse_listener = 0

def on_mouse_click(x,y,button,pressed):
    global firstTimeEvent,last_timeevt
    
    if pressed == True:
        #print(x, " - ", y, " pressed  " , pressed)
        evt = []
        evt.append("m")
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
    pass

def finalizeMacro():
    print("finalizing")
    f = open("macro.txt","a+")
    f.write("%s=" % recordName)
    for event in eventlist:
        print(event)
        if event[0] == 'm':
            f.write("m:%d:%d:%s|" %(event[1], event[2], str(round(event[3],5)) ))
        else:
            f.write("k:%s:%s:%s|" %(str(event[1]), event[2], str(round(event[3],2)) ))

    f.write("\r\n")
    f.close()

    mouse_listener.stop()
    key_listener.stop()
    pass

def addKey(key,press_type):
    global firstTimeEvent,last_timeevt
    evt = []
    evt.append("k")
    evt.append(key)
    evt.append(press_type)
    if firstTimeEvent == True:
        firstTimeEvent = False;
        evt.append(0)
        last_timeevt = time.time()
    else:
        evt.append(time.time() - last_timeevt)
        last_timeevt = time.time()
        
    eventlist.append(evt)
    pass

def on_keyboard_press(key):
    if key == Key.esc:
        finalizeMacro()
    addKey(key,'0')

def on_keyboard_release(key):
    addKey(key,'1')

def getKeyFromStr(key):
    if key == "Key.enter":
        return Key.enter
    elif key == "Key.shift":
        return Key.shift
    elif key == "Key.backspace":
        return Key.backspace
    elif key == "Key.ctrl_l":
        return Key.ctrl_l
    elif key == "Key.alt_l":
        return Key.alt_l
    elif key == "Key.tab":
        return Key.tab
    elif key == "Key.ctrl_r":
        return Key.ctrl_r
    elif key == "Key.alt_r":
        return Key.alt_r	
    elif key == "Key.space":
        return ' '
    else:
        return key.replace("'", "")

def do_event(levelList):
    for evt in levelList:
        print(evt)
        if evt[0] == 'm':
            if evt[3] != 0:
                sleep(evt[3])
            #pyautogui.moveTo(evt[1],evt[2])
            mouse.position = (evt[1], evt[2])
            mouse.press(Button.left)
            mouse.release(Button.left)
            #pyautogui.click()
        elif evt[0] == 'k':
            key = getKeyFromStr(evt[1])
            if evt[3] != 0:
                sleep(evt[3])
            if evt[2] == '0':
                keyboard.press(key)
            else:
                keyboard.release(key)

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
    quit()

if sys.argv[1] == "run":
    #Execute Macro
    if len(sys.argv) <= 2:
        print("Please specify the macro to be executed")
        quit()
    playbackName = sys.argv[2]
    macro = does_macro_exist(playbackName)
    if macro == False:
        print("Macro:", playbackName, "doesnt exist, please see usage for more!")
        quit()
    macro_list = []
    macros = macro.split('|')
    macros.pop() #remove last entry which is the newline
    for segment in macros:
        segment_values = segment.split(':')
        if segment_values[0] == 'm':
            macro_list.append([segment_values[0], int(segment_values[1]),int(segment_values[2]),float(segment_values[3])])
        else:
            macro_list.append([segment_values[0], segment_values[1],segment_values[2], float(segment_values[3])])
    do_event(macro_list)


elif sys.argv[1] == "rec":
    #Record new Macro
    if len(sys.argv) <= 2:
        print("Please specify the macro name")
        quit()
    recordName = sys.argv[2]
    if does_macro_exist(recordName) != False:
        print("Macro", recordName, "already exists, please see usage for more!")
        quit()
    
    key_listener = KeyboardListener(on_press=on_keyboard_press, on_release=on_keyboard_release)
    key_listener.start()

    mouse_listener = MouseListener(on_click=on_mouse_click)
    mouse_listener.start()

    mouse_listener.join()
    key_listener.join()
        
else:
    print("See usage!")
    quit()



