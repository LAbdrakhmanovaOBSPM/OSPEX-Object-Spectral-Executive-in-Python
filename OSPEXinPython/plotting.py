"""

   Application: OSPEX in Python

   Start date: 11/03/2019

   Creators: Liaisian Abdrakhmanova, Abdallah Hamini, Aichatou Aboubacar

   Organization: LESIA, Observatory of Paris, France
  
   Graphical User Interface: GUI was created using tkinter library

   Usage: information to test the program provided in Requirements file

   Status = 'Development'

"""
 
import numpy as np
import pandas as pd
from astropy.io import fits
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#from matplotlib import rcParams
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['DejaVu Sans']
from datetime import timedelta


class Input():
   
    """
    Class to load the parameters from input data and plot Spectrum, Time Profile and Spectrogram
       
    Called Units: Rate, Counts, Flux
   
    """
  
    def __init__(self, file):
        data1, data2, header3, header1 = self.__load_data(file) 

        """

        When open the .fits file, the returned object, called hdulist, behaves like a Python list and each element maps

        to a Header - Data Unit(HDU). We are primarily interested in RATE extension which contains the spectral data.

        Extracted object has two important attributes: data, which behaves like an array, can be used to access to the numerical data;

        and header, which behaves like a dictionary, can be used to access to the header information

        """

        # Define the parameters from HEADER and DATA
        # access by keywords
        self.rate = data1.RATE # count rate data in each energy channel
        self.Time = data1.TIME # array of Time(in seconds) corresponds to the observed flare
        self.Time2 = data1.TIME - 2 # FIXME: used to scale the X - axis in Time profile and Spectrogram plots - 2 seconds difference
        self.Time_del = data1.TIMEDEL # accumulation time
        self.Channel = data1.CHANNEL # energy channels
        self.E_min = data2.E_MIN # array of Low energies
        self.E_max = data2.E_MAX # array of High energies
        self.time_len = len(self.Time) # time length (time bins) 
        self.Area = header3[24] # load the area from header 
        self.Date_start = header3[17] # load start date from header
        self.Date_end = header3[18] # load end date from header
        self.E1 = self.E_min[3] - self.E_min[0] # highlight energy range from 3 to 6 kEv
        self.E2 = self.E_min[9] - self.E_min[3] # highlight energy range from 6 to 12 kEv
        self.E3 = self.E_min[22] - self.E_min[9] # highlight energy range from 12 to 25 kEv
        self.E4 = self.E_min[40] - self.E_min[22] # highlight energy range from 25 to 49 kEv
        self.E5 = self.E_min[57] - self.E_min[40] # highlight energy range from 49 to 100 kEv
        self.E6 = self.E_min[76] - self.E_min[57] # highlight energy range from 100 to 250 kEv
        self.sum = sum(self.Time_del) # observed event duration (in seconds)
        self.detectors = str(header1[25])[10:] # load the names of used detectors 

        # Time format conversion for Time - 2, 2 seconds difference
        # conversion from seconds to hours/minutes/seconds
        self.TimeNew2 = pd.to_datetime(self.Time2, unit='s')

    def __load_data(self, file):   #load the input file choosen in 'Select Input' section
        hdulist = fits.open(file) # read the data
        hdulist.info() # display the content of the read file
        return hdulist[1].data, hdulist[2].data, hdulist[1].header, hdulist[3].header  #read the Data and Header contents from input file

################### 1. Time Profile Plotting ####################

    """

    Define the Rate for "Plot Time Profile"

    Rate  = array which has a count rate data to each energy channel

    There are 6 energy channels
    1: 3-6 kEV
    2: 6-12 keV
    3: 12-25 keV
    4: 25-49 keV
    5: 49-100 keV
    6: 100-250 keV 
    
    """
 
    def __get_rate_data(self):
        data = np.zeros(shape=(self.time_len, 6))
        for i in range(self.time_len):
            # determine the energy distribution for different channels relative to the time of observed data
            data[i, 0] = sum(self.rate[i, 0:3]) #energy channel = 3-6 kEV
            data[i, 1] = sum(self.rate[i, 3:9]) #6-12 keV
            data[i, 2] = sum(self.rate[i, 9:22]) #12-25 keV
            data[i, 3] = sum(self.rate[i, 22:40]) #25-49 keV
            data[i, 4] = sum(self.rate[i, 40:57]) #49-100 keV
            data[i, 5] = sum(self.rate[i, 57:76]) #100-250 keV
        return data #return Rate unit

    """
    Define the Counts for "Plot Time Profile"
      
    In order to perform the conversion between Rate and Counts, multiply accumulation time by Rate

    """

    def __get_counts_data(self):
        data = np.zeros(shape=(self.time_len, 6))
        for i in range(self.time_len):
            data[i, 0] = sum(self.rate[i, 0:3]) * self.Time_del[i]
            data[i, 1] = sum(self.rate[i, 3:9]) * self.Time_del[i]
            data[i, 2] = sum(self.rate[i, 9:22]) * self.Time_del[i]
            data[i, 3] = sum(self.rate[i, 22:40]) * self.Time_del[i]
            data[i, 4] = sum(self.rate[i, 40:57]) * self.Time_del[i]
            data[i, 5] = sum(self.rate[i, 57:76]) * self.Time_del[i]
        return data #return Counts unit

    """
    
    Define the Flux for "Plot Time Profile"

    In order to convert Rate to count flux, divide the Rate by Area and Energy bin width

    """

    def __get_flux_data(self):
        data = np.zeros(shape=(self.time_len, 6))
        for i in range(self.time_len):
            data[i, 0] = sum(self.rate[i, 0:3]) / (self.Area * self.E1)
            data[i, 1] = sum(self.rate[i, 3:9]) / (self.Area * self.E2)
            data[i, 2] = sum(self.rate[i, 9:22]) / (self.Area * self.E3)
            data[i, 3] = sum(self.rate[i, 22:40]) / (self.Area * self.E4)
            data[i, 4] = sum(self.rate[i, 40:57]) / (self.Area * self.E5)
            data[i, 5] = sum(self.rate[i, 57:76]) / (self.Area * self.E6)
        return data #return Flux unit

    

    # 1. Plot Time Profile for Rate, Counts, Flux
    def __time_profile_plotting(self, data, xlabel, title, show=True, name=None):
        df = pd.DataFrame(data, index=self.TimeNew2,
                          columns=['3-6keV(Data with Bk)', '6-12keV(Data with Bk)', '12-25keV(Data with Bk)',
                                   '25-49keV(Data with Bk)', '49-100keV(Data with Bk)', '100-250keV(Data with Bk)']) # add labels for each energy channel
        colors = ['gray','magenta','lime', 'cyan', 'yellow', 'red'] #choose the specific color for each energy channel 
        #df.style.set_properties(subset=['columns'], **{'height': '50px'})
        df.plot(figsize=(6, 6), drawstyle='steps-post', color = colors) # set the size of the figure 
        # define where the steps should be placed: 'steps-pre': The y value is continued constantly to the left from
        # every x position, i.e. the interval (x[i-1], x[i]] has the value y[i]
        # 'steps-post': The y value is continued constantly to the right from every x position, i.e. the interval [x[i], x[i+1]) has the value y[i]
        # 'steps-mid': Steps occur half-way between the x positions
        #plt.rc('legend', labelsize=6)

        
        plt.yscale('log') # set Y-axis in log
        plt.xlabel('Start time: ' + str(self.Date_start)) # load start time from header and display it in X - axis
        plt.ylabel(xlabel)
        plt.title(title)
        #plt.text(self.x_position, 166, 'Detectors: ' + self.detectors) #rate
        #plt.text(self.x_position, 664, 'Detectors: ' + self.detectors)  # counts
        #plt.text(self.x_position, 0.023, 'Detectors: ' + self.detectors) #flux
        if show:
            plt.show()
        if name:
            plt.savefig(name, format='png')

    # if user pick Rate in 'Plot Units' section, plot 'Time profile':
    def rate_vs_time_plotting(self):
        rate_data = self.__get_rate_data()
        self.__time_profile_plotting(rate_data, 'counts/s', 'SPEX HESSI Count Rate vs Time') # name Y -axis and title for Rate 

    # if Counts:
    def counts_vs_time_plotting(self):
        count_data = self.__get_counts_data()

        self.__time_profile_plotting(count_data, 'counts', 'SPEX HESSI Counts vs Time') # name Y -axis and title for Counts 

    # if Flux:
    def flux_vs_time_plotting(self):
        flux_data = self.__get_flux_data()
        self.__time_profile_plotting(flux_data, 'counts s^(-1) cm^(-2) keV^(-1)', 'SPEX HESSI Count Flux vs Time') # name Y -axis and title for Flux

############################# 2. Spectrum plotting #################

    """ 

    As a photons come in over the time and with different energies, the spectrum of counts is built up

    Spectrum = function of energies for Rate/Counts/Flux 

    """

    def __plot_spectrum(self, typ):
        n = len(self.E_min)
        data = np.zeros(shape=n) 
        if typ == 'rate':
            plt.figure()
            for i in range(n):
                data[i] = np.mean(self.rate[:, i]) # determine Rate for "Plot Spectrum"
                plt.rcParams["figure.figsize"] = [6, 6] # plot window size
                plt.text(21.25, 28.1881, 'Detectors: ' + self.detectors, # display the information about detectors, set the text position on the plot
                         fontdict={'fontsize': 7}) 
                plt.text(14.0,23.95, self.Date_start + ' to ' + self.Date_end, # + start & end date of observed event, load directly from header
                         fontdict={'fontsize': 7}) # set text size and font 
                plt.xlabel('Energy(keV)') # label X - axis
                plt.ylabel('counts/s') # Label Y - axis
                plt.title('SPEX HESSI Count Rate vs Energy') # plot title
        elif typ == 'counts':
            plt.figure()
            for i in range(n):
                data[i] = np.mean(self.rate[:, i] * self.sum) #determine Counts for "Plot Spectrum"
                plt.rcParams["figure.figsize"] = [6, 6]
                plt.text(16.57, 69294, 'Detectors: ' + self.detectors, fontdict={'fontsize': 7})
                plt.text(14, 60805, self.Date_start + ' to ' + self.Date_end,
                         fontdict={'fontsize': 7})
                plt.xlabel('Energy(keV)')
                plt.ylabel('counts')
                plt.title('SPEX HESSI Counts vs Energy')
        elif typ == 'flux':
            plt.figure()
            deltaE = np.zeros(shape=(n))
            for i in range(n):
                deltaE[i] = self.E_max[i] - self.E_min[i] # energy range

            for i in range(n):
                data[i] = np.mean(self.rate[:, i]) / (self.Area * deltaE[i]-2) #determine Flux for "Plot Spectrum"
                plt.rcParams["figure.figsize"] = [6, 6]
                plt.text(17.095, 0.1019, 'Detectors: ' + self.detectors, fontdict={'fontsize': 7})
                plt.text(13.132, 0.088, self.Date_start + ' to ' + self.Date_end,
                         fontdict={'fontsize': 7})
                plt.xlabel('Energy(keV)')
                plt.ylabel('counts s^(-1) cm^(-2) keV^(-1)')
                plt.title('SPEX HESSI Count Flux vs Energy')
        else:
            print('error')
            return
        #plt.figure()
        plt.plot(self.E_min, data, drawstyle='steps-post') #Unit vs Energy
        plt.yscale('log')
        plt.xscale('log')
        plt.show()

    # Plot:
    #Spectrum for Rate
    def plot_spectrum_rate(self):
        self.__plot_spectrum('rate')

    #Spectrum for Counts
    def plot_spectrum_counts(self):
        self.__plot_spectrum('counts')

    #Spectrum for Flux
    def plot_spectrum_flux(self):
        self.__plot_spectrum('flux')

########################### 3. Spectrogram Plotting ################

    """

    Spectrogram = function of Rate/Counts/Flux as a function of energy and time
    
    Parameters: x = tick(Time in h:m:s) and y(Energy bounds) are bounds, z is the value *inside* those bounds (Rate/Counts/Flux)

    """
    def __plot_spectrogram(self, typ):
        tick = np.array([str(timedelta(seconds=s)) for s in self.Time2]) # rewrite the time array in a new format: hours:minutes:seconds
        # pcolormesh function(below) doesn't work with pandas time conversion function(TimeNew), that's why we rewrite it again
        #X, Y = np.meshgrid(tick, self.E_min)
        # Define Rate for Plot Spectrogram
        if typ == 'rate':
            plt.figure()
            plt.pcolormesh(tick, self.E_min, np.transpose(self.rate), cmap='gray_r') # cmap = color of the content
            # plt.xticks(np.arange(min(self.TimeNew), max(self.TimeNew), 1.0))
            plt.xlabel('Start Time: ' + self.Date_start) # to name the X -axis load the start date from header
            plt.ylabel('keV') # Y - axis: Energy in keV
            plt.title('SPEX HESSI Count Rate Spectrogram') # title name

        # Define Counts for Plot Spectrogram
        elif typ == 'counts':
            plt.figure()
            plt.pcolormesh(tick, self.E_min, np.transpose(self.rate) * self.sum, cmap='gray_r')
            plt.xlabel('Start Time: ' + self.Date_start)
            plt.ylabel('keV')
            plt.title('SPEX HESSI Counts Spectrogram')

        # Define Flux for Plot Spectrogram
        elif typ == 'flux':
            n = len(self.E_min)
            deltaE = np.zeros(shape=(n))
            for i in range(n):
                deltaE[i] = self.E_max[i] - self.E_min[i]
            plt.figure()
            plt.pcolormesh(tick, self.E_min, np.transpose(self.rate) / (self.Area * deltaE[i]), cmap='gray_r')
            plt.xlabel('Start Time: ' + self.Date_start)
            plt.ylabel('keV')
            plt.title('SPEX HESSI Count Flux Spectrogram')

        else:
            print('error')
            return
        #plt.axis([self.TimeNew2[0], self.TimeNew2[-1], 1, 1000])

        # plt.xsticks(rotation = 90)
        T = len(tick)/5 # step interval in X - axis(time)
        #FIXME: 'step' calculation should be automated 
        plt.colorbar() # fix the colorbar (by default - vertically)
        plt.yscale('log') # specify in log
        plt.yticks([1, 1000]) # place plot content between 1 and 1000 in Y - axis
        plt.xticks(np.arange(len(tick), step = T)) # plot X -axis with given time and step = 8 minutes(08:00:00, 08:08:00, 08:16:00 and etc)
        # for 1st data: step = 30 # , rotation = 90)
        plt.show()

    # Plot Spectrogram
    # Spectrogram for Rate
    def plot_spectrogram_rate(self):
        self.__plot_spectrogram('rate')

    # Spectrogram for Counts
    def plot_spectrogram_counts(self):
        self.__plot_spectrogram('counts')

    # Spectrogram for Flux
    def plot_spectrogram_flux(self):
        self.__plot_spectrogram('flux')


# testing
if __name__ == '__main__':
    plots = Input(".fits") #any input file with .fits extension
    plots.rate_vs_time_plotting() #plot Count Rate vs Time
    plots.counts_vs_time_plotting() #plot Counts vs Time
    plots.flux_vs_time_plotting() #plot Count Flux vs Time
    plots.plot_spectrum_rate() #plot Count Rate vs Energy
    plots.plot_spectrum_counts() #plot Counts vs Energy
    plots.plot_spectrum_flux() #plot Flux vs Energy
    plots.plot_spectrogram_rate() #plot Count Rate Spectrogram
    plots.plot_spectrogram_counts() #plot Counts Spectrogram
    plots.plot_spectrogram_flux() #plot Flux Spectrogram
    plots.self.E_min

