from pyfirmata import Arduino, util
import time
import keyboard

board = Arduino("COM5")

it = util.Iterator(board)
it.start()

# constants
HIGH = 1
LOW = 0

# set up motor pins
in1 = board.digital[5]
in2 = board.digital[6]
enableA = board.digital[7]

# set up forward motor direction
in1.write(HIGH)
in2.write(LOW)

'''
r -> run
s -> stop
f -> forwards
b -> backwards
q -> quit
'''
while True:
    if keyboard.is_pressed('r'):
        enableA.write(HIGH)
        time.sleep(0.5)
    elif keyboard.is_pressed('s'):
        enableA.write(LOW)
        time.sleep(0.5)
    elif keyboard.is_pressed('f'):
        in1.write(HIGH)
        in2.write(LOW)
        time.sleep(0.5)
    elif keyboard.is_pressed('b'):
        in1.write(LOW)
        in2.write(HIGH)
        time.sleep(0.5)
    elif keyboard.is_pressed('q'):
        break