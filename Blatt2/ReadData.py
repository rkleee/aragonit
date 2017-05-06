import numpy as np

#loads data from given file
def loadData(fileName):
        return np.loadtxt(fileName,comments="#",skiprows=3)

#returns data[start:end] from given colum
def getDataSegment(data,start,end,colum):
        return data[start:end:,colum]

#returns temperature and data-values from start-end
def getData(start,end):
        #colum index for temperature
	TX=6
	#colum index for rain
	RR=12
	#load data from file
	data=loadData("data.txt")
	temperature=getDataSegment(data,start,end,TX)
	rain=getDataSegment(data,start,end,RR)
	return (temperature,rain)
