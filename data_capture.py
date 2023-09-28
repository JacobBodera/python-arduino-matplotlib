'''
Name: Jacob Bodera
Created: September 15, 2023
'''

from pyfirmata import Arduino, util
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cv2 as cv
import keyboard
import serial.tools.list_ports

'''    CONSTANTS       '''
# scope length is the length of history that can be seen at once
SCOPE_LENGTH = 50
# time between animation frames
INTERVAL = 500
V_SUPPLY = 5.

open("output.txt", "w").close()


'''      FUNCTIONS      '''
def closeCamera(camera):
    del(camera)
    quit()

def findComPort():
    ports = list(serial.tools.list_ports.comports())
    arduinoComports = []
    numPorts = 0
    chosenPort = 0
    for p in ports:
        if 'Arduino' in p[1]:
            arduinoComports.append(p)
            numPorts += 1
    if numPorts == 0:
        print("----- NO COM FOUND -----")
        return 'None'
    elif numPorts == 1:
        print(f"Connecting to {str(arduinoComports[chosenPort][0])}")
        return str(arduinoComports[chosenPort][0])
    else:
        for index in range(len(arduinoComports)):
            print(arduinoComports[index][0])
        port = str(input('Enter the COM port you want to connect to (COM#): '))
        return port

def animate(i):
    # only store data from current value to {scope_length} values before
    x_vals.append(i)
    x_vals.pop(0)
    y_vals.append(analog_input.read()*V_SUPPLY)
    y_vals.pop(0)
    # figure settings
    ax.cla()
    ax.set_ylim(bottom=-0.1, top=1.1, auto=False)
    ax.set_title("Potentiometer Values Over Time")
    fig.set_figwidth(15)
    fig.set_figheight(7)

    # calculate time different from start of program to current time
    current_time = datetime.now()
    difference = current_time - start_time

    # outputting pressure vs time to file
    with open("output.txt", "a") as f:
        f.write(f"{round(difference.total_seconds(), 2)}, {y_vals[len(y_vals) - 1]}\n")

    value, image = camera.read()
    cv.imwrite('camera_images\\t-'+str(round(difference.total_seconds(), 2))+'.png', image)

    if keyboard.is_pressed('q'):
        closeCamera(camera)

    # display potentiometer value and time on the plot
    ax.annotate(text=f"Current Value: {str(y_vals[len(y_vals) - 1])}V", xycoords="figure pixels", xytext=(5, 5), xy=(5, 5))
    ax.annotate(text=f"Time: {round(difference.total_seconds(), 2)}s", xycoords="figure pixels", xytext=(250, 5), xy=(100, 5))
    ax.plot(x_vals,y_vals)


'''    BOARD & CAMERA SETUP     '''
# initialize location of board
board = Arduino(findComPort())
# set up iterator to periodically read from board
it = util.Iterator(board)
it.start()
# set up analog pin (A0) as input from the board
analog_input = board.get_pin('a:0:i')
# initialize to read from camera
camera = cv.VideoCapture(1)

# x is the time in 100s of ms, y is the potentiometer value ranging from 0 to 1
x_vals = [0]*(SCOPE_LENGTH)
y_vals = [0]*(SCOPE_LENGTH)

# create subplot
fig, ax = plt.subplots()

# get time of start of program
start_time = datetime.now()


# run animator to call animate function every 100ms
ani = FuncAnimation(plt.gcf(), animate, interval=INTERVAL, cache_frame_data=False)

plt.tight_layout()
plt.show()
