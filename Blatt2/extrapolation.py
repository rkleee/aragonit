import numpy as np
import matplotlib.pyplot as plt

#loads data from given file
def loadData(fileName):
        return np.loadtxt(fileName,comments="#")

#returns data[start:end] from given colum
def getDataSegment(data,start,end,colum):
        return data[start:end:,colum]

#plots the graphs
def plotGraphs(temperature,rain,start,end):
        linestyle="-"
        temperature_color="red"
        rain_color="blue"
        #define x-asis from start to end
        x=np.linspace(start,end,end-start)
        #use subplots
        fig,ax1=plt.subplots()
        #ax1 for temperature
        ax1.plot(x,temperature,linestyle,color=temperature_color)
        ax1.tick_params('y',colors=temperature_color)
        ax1.set_xlabel("Zeitpunkt")
        #ax2 with same x-axes for rain
        ax2=ax1.twinx()
        ax2.tick_params('y',colors=rain_color)
        ax2.plot(x,rain,"-",color=rain_color)
        #----------------
        #select every selections.th point from the data
        selection=10
        #selected x_values
        x_interpol=np.arange(0,end-start,selection)
        #degree of interpolated polynomial
        degree=3
        #interpolate polynomial with selected data
        coeff_temperature=np.polyfit(x_interpol,temperature[x_interpol],degree)
        p_temperature=np.poly1d(coeff_temperature)
        #calculate polynomial at all positions (be carefull to use offset)
        values_temperature=p_temperature(x-start)
        #plot interpolated values
        ax1.plot(x,values_temperature,"--",color="darksalmon")
        #analog
        coeff_rain=np.polyfit(x_interpol,rain[x_interpol],degree)
        p_rain=np.poly1d(coeff_rain)
        values_rain=p_rain(x-start)
        ax2.plot(x,values_rain,"--",color="steelblue")
        plt.show()

if __name__ == "__main__":
	#colum index for temperature
	TX=6
	#colum index for rain
	RR=13
	#load data from file
	data=loadData("data.txt")
	#extract data
	start=100
	end=225
	temperature=getDataSegment(data,start,end,TX)
	rain=getDataSegment(data,start,end,RR)
	plotGraphs(temperature,rain,start,end)
	
