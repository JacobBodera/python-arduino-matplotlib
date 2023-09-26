from pyfirmata import Arduino, util
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

open("output.txt", "w").close()

# initialize location of board
# NOTE: may differ depending on system
board = Arduino("COM5")

# set up iterator to periodically read from board
it = util.Iterator(board)
it.start()

# set up analog pin (A0) as input from the board
analog_input = board.get_pin('a:0:i')

# scope length is the length of history that can be seen at once
scope_length = 50
# x is the time in 100s of ms, y is the potentiometer value ranging from 0 to 1
x_vals = [0]*(scope_length)
y_vals = [0]*(scope_length)

# create subplot
fig, ax = plt.subplots()

# get time of start of program
start_time = datetime.now()

def animate(i):
    # only store data from current value to {scope_length} values before
    x_vals.append(i)
    x_vals.pop(0)
    y_vals.append(analog_input.read())
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

    with open("output.txt", "a") as f:
        f.write(f"{round(difference.total_seconds(), 2)}, {y_vals[len(y_vals) - 1]}\n")

    # display potentiometer value and time on the plot
    ax.annotate(text=f"Current Value: {str(y_vals[len(y_vals) - 1])}", xycoords="figure pixels", xytext=(5, 5), xy=(5, 5))
    ax.annotate(text=f"Time: {round(difference.total_seconds(), 2)}s", xycoords="figure pixels", xytext=(250, 5), xy=(100, 5))
    ax.plot(x_vals,y_vals)

# run animator to call animate function every 100ms
ani = FuncAnimation(plt.gcf(), animate, interval=100, cache_frame_data=False)

plt.tight_layout()
plt.show()
