from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as random

fig, ax = plt.subplots()
fig.canvas.set_window_title("Federpendel")
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
origin = ax.plot(0, 0, "x", color="red")
lot, = ax.plot([0, 0], [0, -2], "-", color="red")
pos, = ax.plot([], [], "o", color="black")
curve, = ax.plot([], [], "-", color="blue")

# norm length of pendulum to 1
factor = -9.81
# define grid for euler integration
t = np.arange(0, 10000, 0.01)
dist = t[1] - t[0]

alpha_vel = [random.uniform(-3, 3)]
alpha = [random.uniform(0, 180)]
pendulum_pos = [sin(alpha), -cos(alpha)]


# basic version of euler iteration
# a'(i+1)=a'(i)+h*a''(i)   mit a''(i)=-g/l*sin(a(i))
#  a(i+1)=a(i)+h*a'(i)                    
def iteration_step(i: int):
    global pendulum_pos
    alpha_vel.append(alpha_vel[i - 1] + dist * factor * sin(alpha[i - 1]))
    alpha.append(alpha[i - 1] + dist * alpha_vel[i - 1])
    # reconstruct positions from alpha
    pendulum_pos = [sin(alpha), -cos(alpha)]


def init():
    curve.set_data([], [])
    pos.set_data([], [])
    return curve, pos


# step of animation
def step(j: int):
    # construct line with
    curve.set_data([0, pendulum_pos[0][j]], [0, pendulum_pos[1][j]])
    # set actual position
    pos.set_data(pendulum_pos[0][j], pendulum_pos[1][j])
    iteration_step(j)
    return curve, pos


# create animation
ani = animation.FuncAnimation(fig, step, np.arange(0, len(t)), interval=50, blit=True, init_func=init)
plt.show()
