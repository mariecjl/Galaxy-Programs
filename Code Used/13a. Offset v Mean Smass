import matplotlib.pyplot as plt

#THE BELOW SECTION COMMENTED OUT IS FOR ALL ORIGINAL GALAXIES 
#these are the calculated values for the Smass (the graph's x axis) and the weighted metallicity offset (the graph's y axis)
#the integer (1,2,3) indicates the values for the metallicity offset obtained for 2 bins, 3 bins and 5 bins respectively
# x1=[10.25,10.75]
# x2=[10.166666, 10.5, 10.666666]
# x3=[10.1,10.3,10.5,10.7,10.9]

# y1=[0.015762741179209425,0.06577257177303857]
# y2=[0.07421724324487987,0.005173846583654577,0.10429207185551709]
# y3=[0.07301971269048695,0.04508559046266942,0.00939978493524622,0.08636203001910743,0.15894965419996376]

#THE DATAPOINTS BELOW ARE THE WEIGHTED AVERAGES FOR THE HIGH-CONFIDENCE GALAXIES
x1=[10.25,10.75] #2 bins
x2=[10.166666, 10.5, 10.833333] #3 bins
x3=[10.125,10.375,10.625,10.875] #4 bins
x4=[10.3,10.5,10.7,10.9] #5 bins
#no value for 10.0-10.2 bc no uv nonclumpy datapoint in that bin

y1=[0.04245057041780073,0.10096161350683194]
y2=[0.020879747538382662,0.07223459653447419,0.1473026274272854]
y3=[-0.13238709024253342,0.04984146417234679,0.07824643673614134,0.1427494106616393]
y4=[0.054752762612573155,0.11953547655414144,0.07599018076219365,-0.02088182746137193]



#creating the plots (I originally did only scatterplot but then fond that the plot seemed too "blank" with only two or three datapoints so I also created a version where the dots are connected)
plt.plot(x1,y1,'-o', label="2 Bins")
#axis labels
plt.xlabel("Mean Smass")
plt.ylabel("Metallicity Offset (NonClumpy - Clumpy)")
#saving the plot
plt.savefig("Graph1.png")
#clearing the figure
#plt.clf()

#creating the plot for the histogram with 3 bins
plt.plot(x2,y2,'-o', label="3 Bins")
plt.xlabel("Mean Smass")
plt.ylabel("Metallicity Offset (NonClumpy - Clumpy)")
plt.savefig("Graph2.png")
#plt.clf()

#creating the plot for the histogram with 5 bins
plt.plot(x3,y3,'-o',label="4 Bins")
plt.xlabel("Mean Smass")
plt.ylabel("Metallicity Offset (NonClumpy - Clumpy)")

#creating the plot for the histogram with 5 bins
plt.plot(x4,y4,'-o',label="5 Bins")
plt.xlabel("Mean Smass")
plt.ylabel("Metallicity Offset (NonClumpy - Clumpy)")
plt.title("Metallicity Offsets for Various Binning")
plt.legend()
plt.savefig("Graph3.png")
