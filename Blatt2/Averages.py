import numpy as np
import matplotlib.pyplot as plt
import ReadData

#initializes axes
def init_axes(ax1,x,rain,temperature):
        #ax1 for temperature
        ax1.plot(x,temperature,color="red")
        ax1.tick_params('y',colors="red")
        ax1.set_xlabel("Zeitpunkt")
        ax1.set_ylabel("Temperatur")
        #ax2 with same x-axes for rain
        ax2=ax1.twinx()
        ax2.tick_params('y',colors="blue")
        ax2.plot(x,rain,"-",color="blue")
        ax2.set_ylabel("Niederschlag")
        return (ax1,ax2)

#plots standard average
def plotAverage(x,temperature,rain):
        fig1=plt.figure()
        fig1.canvas.set_window_title("Average")
        ax1=fig1.add_subplot(111)
        (ax1,ax2)=init_axes(ax1,x,rain,temperature)
        x=[start,end]
        av_temp=np.average(temperature)
        av_temp_arr=[av_temp,av_temp]
        av_rain=np.average(rain)
        av_rain_arr=[av_rain,av_rain]
        ax1.plot(x,av_temp_arr,":",color="firebrick")
        ax2.plot(x,av_rain_arr,":",color="royalblue")

#divides input into intervalls and calculates/plots average over these intervalls
def plotAverage_withIntervalls(x,temperature,rain,intervalls):
        fig2=plt.figure() 
        fig2.canvas.set_window_title('Averages with '+str(intervalls)+' Intervalls')
        ax1=fig2.add_subplot(111)
        (ax1,ax2)=init_axes(ax1,x,rain,temperature)
        #TO-DO: Implement-Average using intervalls

#plots all Graphs
def plotGraphs(temperature,rain,start,end):
        x=np.linspace(start,end,end-start)
        plotAverage(x,temperature,rain)
        plotAverage_withIntervalls(x,temperature,rain,3)
        plt.show()     

if __name__ == "__main__":
	start=0
	end=320
	(temperature,rain)=ReadData.getData(start,end)
	plotGraphs(temperature,rain,start,end)
