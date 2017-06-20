import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
        p=np.poly1d([4,3,0.75,-3])
        p_=np.poly1d([12,6,0.75])
        numIntervalls=10000
        start=-
        end=5
        grid=np.linspace(start,end,numIntervalls)
        h=(end-start)/(numIntervalls-1)
        approx1=[]
        y=p(grid)
        for i in range(len(y)-1):
                approx1.append((y[i]+y[i+1])/h)
        approx2=[]
        for i in range(1,len(y)-1):
                approx2.append((y[i-1]+y[i+1])/(2*h))
        max_val=[]
        min_val=[]
        max_x=[]
        min_x=[]
        k=0
        for i in range(1,len(approx1)-1):
                if approx1[i-1]< 0 and approx1[i+1]>0:
                        max_val.append(y[i])
                        max_x.append(grid[i])
                        print(i)
                elif approx1[i-1]>0 and approx1[i]<0:
                        min_val.append(y[i])
                        min_x.append(grid[i])
                        print(i)
        print(max_x)
        print(max_val)
        y_=p_(grid)
        plt.plot(grid,y,'--')
        plt.plot(grid,y_,'--')
        grid=np.delete(grid,-1)
        plt.plot(grid,approx1)
        grid=np.delete(grid,1)
        plt.plot(grid,approx2)
        plt.plot(max_x,max_val)
        plt.plot(min_x,min_val)
        plt.show()
        
   
