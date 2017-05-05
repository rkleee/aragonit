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
        return np.array([m,average_y-m*average_x])

#creates system of equations and solves it using Matrix-Operations
def quadraticRegression(x,y):
        A=np.zeros(shape=(3,3));       
        res_a=np.inner(x**2,y)
        res_b=np.inner(x,y)
        res_c=np.sum(y)
        res=np.array([res_a, res_b, res_c])
        A[0]=[np.sum(x**4), np.sum(x**3), np.sum(x**2)]
        A[1]=[np.sum(x**3), np.sum(x**2), np.sum(x)]
        A[2]=[np.sum(x**2), np.sum(x),len(x)]
        return np.dot(np.linalg.inv(A),res)
        
#coeff [m,b] evaluates m*x+b
def linearFunction(coeff,x):
        return coeff[0]*x+coeff[1]

#coeff=[a,b,c]  evaluates a*x^2+b*x+c
def quadraticFunction(coeff,x):
        return coeff[0]*x**2+coeff[1]*x+coeff[2]

#plots the graphs
def plotGraphs(temperature,rain,start,end):
	#----Aufgabe 1.1 Darstellung des Datensatzes-------
        #define x-asis from start to end
        x=np.linspace(start,end,end-start)
        #use subplots
        OriginalData,ax1=plt.subplots()
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
        #----Aufgabe 1.4 lineareRegression (erster Teil)------
        coeff_temperature=linearRegression(x,temperature)
        coeff_rain=linearRegression(x,rain)
        boundary_points=np.array([start,end])
        values_temperature=linearFunction(coeff_temperature,boundary_points)
        values_rain=linearFunction(coeff_rain,boundary_points)
        ax1.plot(boundary_points,values_temperature,":",color="firebrick")
        ax2.plot(boundary_points,values_rain,":",color="royalblue")
        #----Aufgabe 1.4 quadratische Regression (zweiter Teil)-----
        coeff_temperature=quadraticRegression(x,temperature)
        coeff_rain=quadraticRegression(x,rain)
        values_temperature=quadraticFunction(coeff_temperature,x)
        values_rain=quadraticFunction(coeff_rain,x)
        ax1.plot(x,values_temperature,"-.",color="darkorange")
        ax2.plot(x,values_rain,"-.",color="teal")
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
	end=400
	temperature=getDataSegment(data,start,end,TX)
	rain=getDataSegment(data,start,end,RR)
	plotGraphs(temperature,rain,start,end)
	
