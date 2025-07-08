import keyboard
import time
import pyautogui as pya

q = 'How fast would you like to click in seconds ex 1.0 or miliseconds ex .1 or nano seconds ex .05 or lese website will freeze'
print(q)
lastDigit = None
print('Previous input was probably .009 for the spacebar clicker')
delay = float(input('>> '))
print('You have 3 seconds to navigate to your webpage')
time.sleep(1)
print('3')
time.sleep(1)
print('2')
time.sleep(1)
print('1')
time.sleep(1)
print('Go')
numbs = 0
run = True

while run:
    if keyboard.is_pressed('q'):
        print("You pressed q")
        print('The spacebar was clicked', numbs,'times')
        run = False
        break
    keyboard.press_and_release('space')
    #pya.click()
    numbs = numbs + 1
    print("Clicked", numbs,'times')
    time.sleep(delay)
