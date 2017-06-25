from numpy import sin , cos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as random

fig,ax=plt.subplots()
fig.canvas.set_window_title("Harmonic Oszillator")
ax.set_xlim([-2,2])
ax.set_ylim([-2,2])
origin=ax.plot(0,0,"x",color="red")
pos,=ax.plot([],[],"o",color="black")
curve,=ax.plot([],[],"-",color="blue")
v,=ax.plot([],[],"-",color="green")
text=ax.text(0.1,0.2,'',transform=ax.transAxes)

#define random start values for position and velocity
pendel_pos=[[random.uniform(-1,1)],[random.uniform(-1,1)]]
pendel_vel=[[random.uniform(-1,1)],[random.uniform(-1,1)]]

#define grid for euler integration
t=np.arange(0,100,0.005)
dist=t[1]-t[0]

x_pos=pendel_pos[0]
y_pos=pendel_pos[1]
x_vel=pendel_vel[0]
y_vel=pendel_vel[1]
v_x=np.array([])
v_y=np.array([])

#basic version of euler iteration 
# x'(i+1)=x'(i)+h*x''(i)   mit x''(i)=-c*x(i) für c=D/m
#  x(i+1)=x(i)+h*x(i)                     
for i in range(len(t)):
       #calculate new velocity
       x_vel=np.append(x_vel,x_vel[i-1]+dist*(-3*x_pos[i-1]))
       y_vel=np.append(y_vel,y_vel[i-1]+dist*(-3*y_pos[i-1]))
       #calculate velocity vector for drawing
       v_x=np.append(v_x,[x_pos[i-1],x_pos[i-1]+x_vel[i-1]])
       v_y=np.append(v_y,[y_pos[i-1],y_pos[i-1]+y_vel[i-1]])
       #calculate new postion
       x_pos=np.append(x_pos,x_pos[i-1]+dist*x_vel[i-1])
       y_pos=np.append(y_pos,y_pos[i-1]+dist*y_vel[i-1])

pendel_pos=[x_pos,y_pos]
pendel_vel=[x_vel,y_vel]

def init ():
        v.set_data([],[])
        curve.set_data([],[])
        pos.set_data([],[])
        text.set_text('')
        return curve,pos,text

# step of animation
def step(i):
        #draw corresponding velocity vector
        v.set_data(v_x[2*(i-1):2*i],v_y[2*(i-1):2*i])
        #set all previous points
        curve.set_data(pendel_pos[0][0:i],pendel_pos[1][0:i])
        #set actual positon
        pos.set_data([pendel_pos[0][i]],[pendel_pos[1][i]])
        text.set_text ("Schritt "+str(i))
        return v,curve,pos,text

#create animation
ani=animation.FuncAnimation (fig,step,np.arange(1, len(t)),interval=5,blit=True,init_func =init)
plt.show ()
