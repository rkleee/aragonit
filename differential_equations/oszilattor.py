from numpy import sin , cos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as random

fig,ax=plt.subplots()
ax.set_xlim([-2,2])
ax.set_ylim([-2,2])
origin=ax.plot(0,0,"x",color="red")
pos,=ax.plot([],[],"o",color="black")
curve,=ax.plot([],[],"-",color="blue")
text=ax.text(0.1,0.2,'',transform=ax.transAxes)

#define random start values for position and velocity
pendel_pos=[[random.uniform(-1,1)],[random.uniform(-1,1)]]
pendel_vel=[[random.uniform(-1,1)],[random.uniform(-1,1)]]

#define linspace for euler integration
t=np.linspace (0,100,10001)
dist=t[1]-t[0]
print(dist)

x_pos=pendel_pos[0]
y_pos=pendel_pos[1]
x_vel=pendel_vel[0]
y_vel=pendel_vel[1]

#basic version of euler iteration 
# x'(i+1)=x'(i)+h*x''(i)   mit x''(i)=-c*x(i) für c=D/m
#  x(i+1)=x(i)+h*x(i)                     
for i in range(len(t)):
       #
       x_vel.append(x_vel[i-1]+dist*(-3*x_pos[i-1]))
       y_vel.append(y_vel[i-1]+dist*(-3*y_pos[i-1]))
       x_pos.append(x_pos[i-1]+dist*x_vel[i-1])
       y_pos.append(y_pos[i-1]+dist*y_vel[i-1])
pendel_pos=[x_pos,y_pos]
pendel_vel=[x_vel,y_vel]

def init ():
        curve.set_data([],[])
        pos.set_data([],[])
        text.set_text('')
        return pos,text

# animationsschritt
def step(i):
        curve.set_data(pendel_pos[0][0:i],pendel_pos[1][0:i])
        pos.set_data([pendel_pos[0][i]],[pendel_pos[1][i]])
        text.set_text ("Schritt "+str(i))
        return curve,pos,text

ani=animation.FuncAnimation (fig,step,np.arange(1, len(t)),interval=25,blit=True,init_func =init)
plt.show ()
