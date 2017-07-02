import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as random

# define random start values for position and velocity
pendulum_pos = [[random.uniform(-1, 1)], [random.uniform(-1, 1)]]
pendulum_vel = [[random.uniform(-1, 1)], [random.uniform(-1, 1)]]

# define grid for euler integration
dist = 0.02

fig, ax = plt.subplots()
fig.canvas.set_window_title("Harmonic Oszillator")
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
origin = ax.plot(0, 0, "x", color="red")
pos, = ax.plot([], [], "o", color="black")
curve, = ax.plot([], [], "-", color="blue")
v, = ax.plot([], [], "-", color="green")

x_pos = pendulum_pos[0]
y_pos = pendulum_pos[1]
x_vel = pendulum_vel[0]
y_vel = pendulum_vel[1]
v_x = np.array([])
v_y = np.array([])


# x'(i+1)=x'(i)+h*x''(i)   mit x''(i)=-c*x(i) für c=D/m
#  x(i+1)=x(i)+h*x(i)
# calculate the i-th step of euler iteration
def iteration_step(i):
    global x_vel, y_vel, x_pos, y_pos
    # calculate new velocity
    x_vel_new = x_vel[i - 1] + dist * (-3 * x_pos[i - 1])
    y_vel_new = y_vel[i - 1] + dist * (-3 * y_pos[i - 1])
    # calculate velocity vector for drawing
    v_x_new = [x_pos[i - 1], x_pos[i - 1] + x_vel[i - 1]]
    v_y_new = [y_pos[i - 1], y_pos[i - 1] + y_vel[i - 1]]
    # calculate new position
    x_pos_new = x_pos[i - 1] + dist * x_vel[i - 1]
    y_pos_new = y_pos[i - 1] + dist * y_vel[i - 1]
    return [x_vel_new, y_vel_new, v_x_new, v_y_new, x_pos_new, y_pos_new]


# calls euler-iteration and sets values
def iterate(i):
    global x_vel, y_vel, x_pos, y_pos, v_x, v_y
    global pendulum_pos, pendulum_vel
    values = iteration_step(i)
    x_vel = np.append(x_vel, values[0])
    y_vel = np.append(y_vel, values[1])
    v_x = np.append(v_x, values[2])
    v_y = np.append(v_y, values[3])
    x_pos = np.append(x_pos, values[4])
    y_pos = np.append(y_pos, values[5])
    pendulum_pos = [x_pos, y_pos]
    pendulum_vel = [x_vel, y_vel]


def init():
    v.set_data([], [])
    curve.set_data([], [])
    pos.set_data([], [])
    return curve, pos


# step of animation
def step(i):
    global pendulum_pos, pendulum_vel, v_x, v_y
    # set all previous points
    curve.set_data(pendulum_pos[0][0:i - 1], pendulum_pos[1][0:i - 1])
    # set actual position
    pos.set_data(pendulum_pos[0][i - 1], pendulum_pos[1][i - 1])
    iterate(i)
    # draw corresponding velocity vector
    v.set_data(v_x[2 * (i - 1):2 * i], v_y[2 * (i - 1):2 * i])
    return v, curve, pos


# create animation
ani = animation.FuncAnimation(fig, step, np.arange(0, 100000), interval=15, blit=True, init_func=init)
plt.show()
