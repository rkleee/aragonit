import numpy as np
import matplotlib.pyplot as plt

#loads data from given file
def loadData(fileName):
        return np.loadtxt(fileName,comments="#",skiprows=3)

#returns data[start:end] from given colum
def getDataSegment(data,start,end,colum):
        return data[start:end:,colum]

#calulates m,b for m*x+b for regression on x and y
def linearRegression(x,y):
        n=len(x)
        average_x=np.sum(x)/n
        average_y=np.sum(y)/n
        scalar_term=np.inner(x,y)
        squared_sum=np.sum(x**2)
        m=(n*average_x*average_y-scalar_term)/(n*average_x*average_x-squared_sum)
        return (m,average_y-m*average_x)

#evaluates m*x+b at all positions x
def linearFunction(m,b,x):
        return m*x+b

#plots the graphs
def plotGraphs(temperature,rain,start,end):
	#----Aufgabe 1.1 Darstellung des Datensatzes-------
        linestyle="-"
        temperature_color="red"
        rain_color="blue"
        #define x-asis from start to end
        x=np.linspace(start,end,end-start)
        #use subplots
        OriginalData,ax1=plt.subplots()
        #ax1 for temperature
        ax1.plot(x,temperature,linestyle,color=temperature_color)
        ax1.tick_params('y',colors=temperature_color)
        ax1.set_xlabel("Zeitpunkt")
        ax1.set_ylabel("Temperatur")
        #ax2 with same x-axes for rain
        ax2=ax1.twinx()
        ax2.tick_params('y',colors=rain_color)
        ax2.plot(x,rain,"-",color=rain_color)
        ax2.set_ylabel("Niederschlag")
        #----Aufgabe 1.4 lineareRegression (erster Teil)------
        (m_temp,b_temp)=linearRegression(x,temperature)
        (m_rain,b_rain)=linearRegression(x,rain)
        boundary_points=np.array([start,end])
        ax1.plot(boundary_points,linearFunction(m_temp,b_temp,boundary_points),":",color="firebrick")
        ax2.plot(boundary_points,linearFunction(m_rain,b_rain,boundary_points),":",color="royalblue")
        #----Aufgabe 1.4 (letzter Teil) für allgemeine Polynome-----
        #degree of interpolated polynomial
        degree=5
        #interpolate polynomial with data
        coeff_temperature=np.polyfit(x,temperature,degree)
        coeff_rain=np.polyfit(x,rain,degree)
        p_temperature=np.poly1d(coeff_temperature)
        p_rain=np.poly1d(coeff_rain)
        #calculate polynomial at all positions
        values_temperature=p_temperature(x)
        values_rain=p_rain(x)
        #draw curves
        ax1.plot(x,values_temperature,"--",color="darksalmon")
        ax2.plot(x,values_rain,"--",color="steelblue")
        plt.show()

if __name__ == "__main__":
	#colum index for temperature
	TX=6
	#colum index for rain
	RR=12
	#load data from file
	data=loadData("data.txt")
	#extract data
	start=50
	end=350
	temperature=getDataSegment(data,start,end,TX)
	rain=getDataSegment(data,start,end,RR)
	plotGraphs(temperature,rain,start,end)
	
