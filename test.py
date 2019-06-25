
   """

   Application: OSPEX in Python

   Started date: 11/03/2019

   Creators: Liaisian Abdrakhmanova, Abdallah Hamini

   Organization: LESIA, Observatory of Paris, France
  
   Graphical User Interface: GUI was created using tkinter library

   Usage: information to test the program provided in Requirements file

   Status = 'Development'

   """
    
    
    
import pylab
from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt, figure
import pandas as pd
from matplotlib.pyplot import imshow, text

hdulist = fits.open("hsi_spectrum_20020213_081052.fits" )
hdulist.info()
header1 = hdulist[1].header
header3 = hdulist[3].header
data1 = hdulist[1].data
data2 = hdulist[2].data


Rate = data1.RATE
Time = data1.TIME - 2
Livetime = data1.LIVETIME
Time_del = data1.TIMEDEL
Channel = data1.CHANNEL
E_min = data2.E_MIN
Area = header3[24]
Date_start = header3[17]
Date_end = header3[18]

E1 = E_min[3]-E_min[0]
E2 = E_min[9]-E_min[3]
E3 = E_min[22]-E_min[9]
E4 = E_min[40]-E_min[22]
E5 = E_min[57]-E_min[40]
E6 = E_min[76]-E_min[57]
E_mean = np.mean(E_min)

#RATE
m = len(Time)
DataNew = np.zeros(shape=(m,6))
for i in range(m):
    DataNew[i,0] = sum(Rate[i, 0:3])
    DataNew[i,1] = sum(Rate[i, 3:9])
    DataNew[i,2] = sum(Rate[i, 9:22])
    DataNew[i, 3] = sum(Rate[i, 22:40])
    DataNew[i, 4] = sum(Rate[i, 40:57])
    DataNew[i, 5] = sum(Rate[i, 57:77])

#COUNTS
DataNew2 = np.zeros(shape=(m,6))
for i in range(m):
    DataNew2[i,0] = DataNew[i,0] * Time_del[i]
    DataNew2[i,1] = DataNew[i,1] * Time_del[i]
    DataNew2[i,2] = DataNew[i,2] * Time_del[i]
    DataNew2[i,3] = DataNew[i,3] * Time_del[i]
    DataNew2[i,4] = DataNew[i,4] * Time_del[i]
    DataNew2[i,5] = DataNew[i,5] * Time_del[i]



#FLUX
DataNew3 = np.zeros(shape=(m,6))
for i in range(m):
    DataNew3[i,0] = DataNew[i,0] /(Area*E1)
    DataNew3[i,1] = DataNew[i,1] /(Area*E2)
    DataNew3[i,2] = DataNew[i,2] /(Area*E3)
    DataNew3[i,3] = DataNew[i,3] /(Area*E4)
    DataNew3[i,4] = DataNew[i,4] /(Area*E5)
    DataNew3[i,5] = DataNew[i,5] /(Area*E6)

# Time format conversion
TimeNew = pd.to_datetime(Time, unit='s')

## Time Profile Plotting
# 1. Rate vs Time

df = pd.DataFrame(DataNew, index=TimeNew, columns=['3-6keV(Data with Bk)', '6-12keV(Data with Bk)', '12-25keV(Data with Bk)', '25-49keV(Data with Bk)', '49-100keV(Data with Bk)', '100-250keV(Data with Bk)'])
line1 = pylab.Line2D(range(10), range(10), marker='o', color="goldenrod")
plt.legend((line1, loc=2))
df.plot(figsize=(14,9), drawstyle='steps-post') #steps-post, steps-mid
plt.yscale('log')
plt.text(6, 5,'matplotlib', ha='center', va='center')
plt.xlabel('Start Time(13-February-02 08:10:52)')
plt.ylabel('Rate(counts/s)')
plt.title('SPEX HESSI Rate vs Time')
#plt.savefig('RateVsTime.png', format = 'png')


df2 = pd.DataFrame(DataNew2, index=TimeNew, columns=['3-6keV(Data with Bk)', '6-12keV(Data with Bk)', '12-25keV(Data with Bk)', '25-49keV(Data with Bk)', '49-100keV(Data with Bk)', '100-250keV(Data with Bk)'])
df2.plot(figsize=(14, 9), drawstyle='steps-post')
plt.yscale('log')
plt.xlabel('Start Time(13-February-02 08:10:52)')
plt.ylabel('Counts(counts)')
plt.title('SPEX HESSI Counts vs Time')
plt.show()
#plt.savefig('CountsVsTime.png', format = 'png')


df3 = pd.DataFrame(DataNew3, index=TimeNew, columns=['3-6keV(Data with Bk)', '6-12keV(Data with Bk)', '12-25keV(Data with Bk)', '25-49keV(Data with Bk)', '49-100keV(Data with Bk)', '100-250keV(Data with Bk)'])
df3.plot(figsize=(14, 9), drawstyle='steps-post')
plt.yscale('log')
plt.xlabel('Start Time(13-February-02 08:10:52)')
plt.ylabel('Counts(counts/s cm(-2) keV(-1)')
plt.title('SPEX HESSI Flux vs Time')
plt.show()
#plt.savefig('FluxVsTime.png', format = 'png')


## Plot Spectrum
# 1. Rate
n = len(E_min)
DataNew4 = np.zeros(shape=(n))
for i in range(n):
    DataNew4[i] = np.mean(Rate[:, i])
plt.plot(E_min, DataNew4, drawstyle='steps-post')
plt.yscale('log')
plt.xscale('log')
plt.show()


#Counts
DataNew5 = np.zeros(shape=(n))
for i in range(n):
    DataNew5[i] = np.mean(Rate[:,i]*Time_del[:])
plt.plot(E_min,DataNew5, drawstyle='steps-post')
plt.yscale('log')
plt.xscale('log')
plt.show()


DataNew6 = np.zeros(shape=(n))
for i in range(n):
    DataNew6[i] = np.mean(Rate[:,i]/(Area*E_mean))
plt.plot(DataNew6, drawstyle='steps-post')
plt.yscale('log')
plt.xscale('log')
plt.show()



##Plot Spectrogram

# Rate
plt.axis([TimeNew[0],TimeNew[147], 1, 1000])
X, Y = np.meshgrid(TimeNew, E_min)
plt.pcolormesh(TimeNew, Y, np.transpose(Rate), cmap='gray_r')
plt.colorbar()
plt.yscale('log')
plt.xlabel('Start Time(13-February-02 08:10:52)')
plt.ylabel('keV')
plt.title('SPEX HESSI Count Rate Spectrogram')
plt.show()

#Counts
plt.axis([TimeNew[0],TimeNew[147], 1, 1000])
X, Y = np.meshgrid(TimeNew, E_min)
plt.pcolormesh(X, Y, np.transpose(Rate)*(Time_del), cmap='gray_r')
plt.colorbar(orientation = 'horizontal')
plt.yscale('log')
plt.xlabel('Start Time(13-February-02 08:10:52)')
plt.ylabel('keV')
plt.title('SPEX HESSI Counts Spectrogram')
plt.show()

#Flux
plt.axis([TimeNew[0],TimeNew[147], 1, 1000])
X, Y = np.meshgrid(TimeNew, E_min)
plt.pcolormesh(X, Y, np.transpose(Rate)/(Area*len(E_min)), cmap='gray_r')
plt.colorbar()
plt.yscale('log')
plt.xlabel('Start Time(13-February-02 08:10:52)')
plt.ylabel('keV')
plt.title('SPEX HESSI Flux Spectrogram')
plt.show()

