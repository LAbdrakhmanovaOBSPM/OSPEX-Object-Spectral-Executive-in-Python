from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt, figure
import pandas as pd
from datetime import timedelta
from matplotlib.pyplot import imshow, text
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from astropy.modeling import models, fitting
from sklearn.metrics import mean_squared_error
from math import *
from astropy.modeling.models import custom_model
from astropy.modeling.fitting import LevMarLSQFitter
from scipy.optimize import curve_fit
import matplotlib.dates as mdates
import background


class BackgPlots():

    fname=None
    def __init__(self):
        
        bkgTimeIntv = ""

    def plot(self, timeInterv, unit, energyBinIndex, polyDeg):
        if background.BackgroundWindow.fname is not None:
            hdulist = fits.open(background.BackgroundWindow.fname)
            hdulist.info()
            header1 = hdulist[1].header
            header3 = hdulist[3].header
            data1 = hdulist[1].data
            data2 = hdulist[2].data
            Rate = data1.RATE
            Time = data1.TIME
            Time2 = data1.TIME - 2
            time_len = len(Time)
            Livetime = data1.LIVETIME
            Time_del = data1.TIMEDEL
            Channel = data1.CHANNEL
            E_min = data2.E_MIN
            E_max = data2.E_MAX
            Area = header3[24]
            E_mean = np.mean(E_min)
            Accum_Time = np.sum(Time_del)
            Date_start = header3[17]
            E1 = E_min[3] - E_min[0]
            E2 = E_min[9] - E_min[3]
            E3 = E_min[22] - E_min[9]
            E4 = E_min[40] - E_min[22]
            E5 = E_min[57] - E_min[40]
            E6 = E_min[76] - E_min[57]

            unitData = None

            """Define Spectrum Units: Rate, Counts, Flux"""
            n = len(E_min)
            deltaE = np.zeros(shape=(n))
            for i in range(n):
                deltaE[i] = E_max[i] - E_min[i]
            #Rate

            CountRate = np.zeros(shape=(n))
            for i in range(n):
                CountRate[i] = np.mean(Rate[:, i])

            #Counts
            Counts = np.zeros(shape=(n))
            for i in range(n):
                Counts[i] = np.mean(Rate[:,i]*Accum_Time)

            #Flux
            Flux = np.zeros(shape=(n))
            for i in range(n):
                Flux[i] = np.mean(Rate[:,i]) / (Area*deltaE[i]-2)


            x = E_min
            y = Flux


            ####################" background ############################
             
            # Define the Rate for "Plot Time Profile"

            dataRate = np.zeros(shape=(time_len, 6))
            for i in range(time_len):
                dataRate[i, 0] = sum(Rate[i, 0:3])
                dataRate[i, 1] = sum(Rate[i, 3:9])
                dataRate[i, 2] = sum(Rate[i, 9:22])
                dataRate[i, 3] = sum(Rate[i, 22:40])
                dataRate[i, 4] = sum(Rate[i, 40:57])
                dataRate[i, 5] = sum(Rate[i, 57:76])


            # Define the Counts for "Plot Time Profile"

            dataCounts = np.zeros(shape=(time_len, 6))
            for i in range(time_len):
                dataCounts[i, 0] = sum(Rate[i, 0:3]) * Time_del[i]
                dataCounts[i, 1] = sum(Rate[i, 3:9]) * Time_del[i]
                dataCounts[i, 2] = sum(Rate[i, 9:22]) * Time_del[i]
                dataCounts[i, 3] = sum(Rate[i, 22:40]) * Time_del[i]
                dataCounts[i, 4] = sum(Rate[i, 40:57]) * Time_del[i]
                dataCounts[i, 5] = sum(Rate[i, 57:76]) * Time_del[i]


            # Define the Flux for "Plot Time Profile"

            dataFlux = np.zeros(shape=(time_len, 6))
            for i in range(time_len):
                dataFlux[i, 0] = sum(Rate[i, 0:3]) / (Area * E1)
                dataFlux[i, 1] = sum(Rate[i, 3:9]) / (Area * E2)
                dataFlux[i, 2] = sum(Rate[i, 9:22]) / (Area * E3)
                dataFlux[i, 3] = sum(Rate[i, 22:40]) / (Area * E4)
                dataFlux[i, 4] = sum(Rate[i, 40:57]) / (Area * E5)
                dataFlux[i, 5] = sum(Rate[i, 57:76]) / (Area * E6)
                   
            if unit == 'Rate':
                unitData =  dataRate[:,int(energyBinIndex)] #dRate 
            elif unit == 'Counts':
                unitData = dataCounts[:,int(energyBinIndex)]
            elif unit == 'Flux':
                unitData = dataFlux[:,int(energyBinIndex)]
                
            TimeNew2 = pd.to_datetime(Time2, unit='s')
            Time2Array = TimeNew2.to_numpy()
##            df = pd.DataFrame(dataRate, index=TimeNew2,
##                            columns=['3-6keV(Data with Bk)', '6-12keV(Data with Bk)', '12-25keV(Data with Bk)',
##                                      '25-49keV(Data with Bk)', '49-100keV(Data with Bk)', '100-250keV(Data with Bk)'])


            ################################## 08:05 to 08:07 ################################
            if len(timeInterv) > 0:
                if '-' in timeInterv or 'to' in timeInterv:
                    timeInterval = timeInterv.split('-') if '-' in timeInterv else timeInterv.split('to')
                    startTimeInterv = timeInterval[0].strip().split(':')
                    endTimeInterv = timeInterval[1].strip().split(':')
                    startIndex = int(((int(startTimeInterv[0])*3600 + int(startTimeInterv[1])*60) - (int(startTimeInterv[0]) * 3600 ))/4)
                    endIndex = int(((int(endTimeInterv[0])*3600 + int(endTimeInterv[1])*60) - (int(startTimeInterv[0]) * 3600))/4)

            #Time2bkg = Time2Array[startIndex:endIndex +1]

            ################### plot data with bkg ##########################################################################################
            colors = ['gray','magenta','lime', 'cyan', 'yellow', 'red']
            energyLab = ['3.0 to 6.0 keV', '6.0 to 12.0 keV', '12.0 to 25.0 keV', '25.0 to 49.0 keV',
                      '49.0 to 100.0 keV', '100.0 to 250.0 keV' ]
            xticksVal = TimeNew2.strftime('%H:%M') #TimeNew2.time
            
            plt.figure()
            plt.plot(TimeNew2.time, unitData, drawstyle='steps-post', color=colors[int(energyBinIndex)], label = str(energyLab[int(energyBinIndex)]) + ' (Data with Bk)')

            ####################### numpy poly plot bkg : poly1d ############################################################################
            bkgMethod = {0:'0Poly', 1:'1Poly', 2:'2Poly', 3:'3Poly', 4:'Exp', 5:'High E Profile', 6:'This E Profile'}
            #methodNum = list(bkgMethod.keys())
            print ('eeeeee', polyDeg,  bkgMethod[0], polyDeg == bkgMethod[1])
            if polyDeg == bkgMethod[0]:
               fitRslt = np.poly1d(np.polyfit(Time2[startIndex:endIndex +1], unitData[startIndex:endIndex +1], 0)) #,  w= 1.0/unitData[startIndex:endIndex +1]))
            elif polyDeg == bkgMethod[1]:
               fitRslt = np.poly1d(np.polyfit(Time2[startIndex:endIndex +1], unitData[startIndex:endIndex +1], 1))
            elif polyDeg == bkgMethod[2]:
               fitRslt = np.poly1d(np.polyfit(Time2[startIndex:endIndex +1], unitData[startIndex:endIndex +1], 2))
            elif polyDeg == bkgMethod[3]:
               fitRslt = np.poly1d(np.polyfit(Time2[startIndex:endIndex +1], unitData[startIndex:endIndex +1], 3))
                  
            plt.plot(TimeNew2.time, fitRslt(Time2), drawstyle='steps-post', color='green', label = str(energyLab[int(energyBinIndex)]) + ' (Bk)')



            ################## plot data - bkg ################################################################################################
 
            plt.plot(TimeNew2.time, unitData - fitRslt(Time2),drawstyle='steps-post', color="blue" , label = str(energyLab[int(energyBinIndex)]) + ' (Data - Bk')
            #plt.plot(Time2Array, np.sqrt(np.abs(unitData - fitRslt(Time2))),drawstyle='steps-post', label = "Polynomial1D, degree = 0")



            ############################ plot #####################################
            plotTitle = 'SPEX HESSI Counts vs Time' if 'Counts' in unit else 'SPEX HESSI Count ' + unit + ' vs Time'
            plt.xlabel('Start time: ' + str(Date_start))
            plt.ylabel('Counts/s cm(-2) keV(-1)')
            plt.yscale('log')
            ##plt.xscale('log')
            plt.title(plotTitle)
            #plt.legend()
            ax = plt.axes()
            legend = ax.legend(loc='upper right' )
            
            #ax.set_facecolor("black")
            #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

            plt.show()

        else:
            print(' No file name')



