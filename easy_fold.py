

# import pyautogui

# pyautogui.alert('This is the message to display.') 

from glob import glob
from logging import fatal
from pynput import mouse, keyboard

from time import sleep

fishk = keyboard.Controller()
fishm = mouse.Controller()

from threading import Thread

DEBUG = True

def myprint(text, **kwargs):
    if DEBUG:
        print(text, **kwargs)

def on_move(x, y):
    myprint('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    myprint('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    myprint('Scrolled {0}'.format((x, y, dx, dy)))

# Collect events until released

if 0:
    pass
    # def on_press(key):
    #     try:
    #         myprint('alphanumeric key {0} pressed'.format(key.char))
    #     except AttributeError:
    #         myprint('special key {0} pressed'.format(key))

    # def on_release(key):
    #     myprint('{0} released'.format(key))
    #     if key == keyboard.Key.esc:
    #         # Stop listener
    #         return False

    # # Collect events until released
    # with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: 
    #     listener.join()

    # ...or, in a non-blocking fashion:

shifted = False
virtual = False

pressing = False
def on_press(key):
    global shifted, virtual, mou, pressing
    if key == keyboard.Key.shift:
        if not virtual:
            # myprint("shift", end="")
            shifted = True


def on_release(key):
    # myprint('{0} released'.format(key))
    
    global shifted, virtual, mou
    if key == keyboard.Key.shift:
        if not virtual: 
            # myprint("unshift", end="")
            shifted = False



COMBINATION = {keyboard.Key.shift, keyboard.Key.ctrl}


EVENT_QUEUE = []


def thread1(): 
    global EVENT_QUEUE
    global fishk, fishm

    while True:
        if len(EVENT_QUEUE) > 0:
            dir = EVENT_QUEUE.pop(0)
            if len(EVENT_QUEUE) % 2 == 0:
                fishk.release(keyboard.Key.shift)
                fishm.click(mouse.Button.left, 1)
                fishk.press(keyboard.Key.shift)
                # fishk.type(f'{keyboard.Key.shift}{keyboard.Key.ctrl}[')
                fishk.press(keyboard.Key.shift)
                fishk.press(keyboard.Key.ctrl)
                if dir > 0:
                    fishk.type("[")
                elif dir < 0:
                    fishk.type("]")
                fishk.release(keyboard.Key.ctrl)
        if len(EVENT_QUEUE) > 10:   
            EVENT_QUEUE= EVENT_QUEUE[0:10]


running = False
def on_shift_scroll(x=0, y=0, dx=0, dy=0, key="A"):
    global shifted, virtual, fishk, fishm, running, mou, EVENT_QUEUE
    if shifted:

        dir = int(dy)
        EVENT_QUEUE.append(dir)
    
    # if running:
    #     return
    # running = True
    # fishk.press('a')
    # fishk.release('a')
    # running = False



key = keyboard.Listener(on_press=on_press, on_release=on_release)
key.start()
mou = mouse.Listener(on_scroll= lambda x, y, dx, dy:on_shift_scroll(x=x, y=y, dx=dx, dy=dy), suppress=False)
mou.start()

thread11 = Thread(target=thread1)
thread11.start()

while True:
    try:
        pass
    except KeyboardInterrupt as e:
        key.stop()
        mou.stop()
        break

