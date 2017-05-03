import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
	#colum index for temperature
	TX=6
	#colum index for rain
	RR=13
	#load data from file
	data=np.loadtxt("data.txt",comments="#")
	#extract data
	start=50
	end=70
	temperature=data[start:end:,TX]
	rain=data[start:end:,RR]
	#define x-asis from 0 to n and n intervalls
	x=np.linspace(0,len(rain),len(rain))
	#use subplots
	fig,ax1 =plt.subplots()
	#ax1 for temperature color red
	ax1.plot(x,temperature,"-r")
	ax1.tick_params('y',colors='r')
	ax1.set_xlabel("Zeitpunkt")
	#ax2 with same x-axes for rain color blue
	ax2=ax1.twinx()
	ax2.tick_params('y',colors='b')
	ax2.plot(x,rain,"-b")
	plt .show()