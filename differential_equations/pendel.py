from numpy import sin,cos
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as random

fig,ax=plt.subplots()
fig.canvas.set_window_title("Federpendel")
ax.set_xlim([-2,2])
ax.set_ylim([-2,2])
origin=ax.plot(0,0,"x",color="red")
lot,=ax.plot([0,0],[0,-2],"-",color="red")
pos,=ax.plot([],[],"o",color="black")
curve,=ax.plot([],[],"-",color="blue")

start_x=random.uniform(0,1)
start_y=random.uniform(-1,0)
start_vel_x=random.uniform(0,10)
start_vel_y=random.uniform(-10,0)
#define random start values for position and velocity
pendel_pos=[[start_x],[start_y]]
pendel_vel=[[3],[-3]]
l=sqrt(start_x**2+start_y**2)
factor=-9.81/l
#define grid for euler integration
t=np.arange(0,10000,0.01)
dist=t[1]-t[0]
c=1

x_pos=pendel_pos[0]
y_pos=pendel_pos[1]
x_vel=pendel_vel[0]
y_vel=pendel_vel[1]

#basic version of euler iteration 
# a'(i+1)=a'(i)+h*a''(i)   mit a''(i)=-g/l*sin(a(i))
#  a(i+1)=a(i)+h*a'(i)
print(len(t))                     
for i in range(len(t)):
        x_vel.append(c*(x_vel[i-1]+dist*factor*sin(x_pos[i-1])))
        y_vel.append(c*(y_vel[i-1]+dist*factor*sin(y_pos[i-1])))
        x_pos.append(x_pos[i-1]+dist*x_vel[i-1])
        y_pos.append(y_pos[i-1]+dist*y_vel[i-1])
        #Dämpfungs-Faktor sinkt sehr langsam (proportional zu -sqrt(i)/c)
        c=(1-sqrt(i)/8000)   

#reconstruct positons from alpha
pendel_pos=[l*sin(x_pos),-l*cos(y_pos)]
pendel_vel=[x_vel,y_vel]

def init ():
        curve.set_data([],[])
        pos.set_data([],[])
        return curve,pos

# step of animation
def step(i):
        #construct line with 
        curve.set_data([0,pendel_pos[0][i]],[0,pendel_pos[1][i]])
        #set actual positon
        pos.set_data(pendel_pos[0][i],pendel_pos[1][i])
        return curve,pos
#create animation
ani=animation.FuncAnimation (fig,step,np.arange(1, len(t)),interval=50,blit=True,init_func =init)
plt.show ()
