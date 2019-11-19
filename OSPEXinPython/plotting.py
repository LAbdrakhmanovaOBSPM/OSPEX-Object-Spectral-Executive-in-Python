"""

   Application: OSPEX in Python

   Started date: 11/03/2019

   Creators: Liaisian Abdrakhmanova, Abdallah Hamini

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
from datetime import timedelta


class Input:
   
    """
    Class for loading the parameters and plotting Spectrum, Time Profile and Spectrogram
       
    Called Units: Rate, Counts, Flux
   
    """
    
    def __init__(self, file):
        data1, data2, header3, header1 = self.__load_data(file)

        # Define the parameters from HEADER and DATA
        self.rate = data1.RATE
        self.Time = data1.TIME
        self.Time2 = data1.TIME - 2
        self.Livetime = data1.LIVETIME
        self.Time_del = data1.TIMEDEL
        self.Channel = data1.CHANNEL
        self.E_min = data2.E_MIN
        self.E_max = data2.E_MAX
        self.time_len = len(self.Time)
        self.Area = header3[24]
        self.Date_start = header3[17]
        self.Date_end = header3[18]
        self.E1 = self.E_min[3] - self.E_min[0]
        self.E2 = self.E_min[9] - self.E_min[3]
        self.E3 = self.E_min[22] - self.E_min[9]
        self.E4 = self.E_min[40] - self.E_min[22]
        self.E5 = self.E_min[57] - self.E_min[40]
        self.E6 = self.E_min[76] - self.E_min[57]
        self.E_mean = np.mean(self.E_min)
        self.sum = sum(self.Time_del)
        self.detectors = str(header1[25])[10:]


        # Time format conversion (from sec to h/m/sec/)
        #self.TimeNew = pd.to_datetime(self.Time, unit='s')

        # Time -2
        self.TimeNew2 = pd.to_datetime(self.Time2, unit='s')

        self.TimeNew22 = np.array(self.TimeNew2)
        self.x_position = str(self.TimeNew2[70])


        #
        self.t1 = pd.to_timedelta(self.Time2, unit='s')
        #self.t1 = map(self.t1, float)

        self.t2 = np.array([str(timedelta(seconds=s)) for s in self.Time])

    def __load_data(self, file):
        hdulist = fits.open(file)
        hdulist.info()
        return hdulist[1].data, hdulist[2].data, hdulist[1].header, hdulist[3].header

    # Define the Rate for "Plot Time Profile"
    def __get_rate_data(self):
        data = np.zeros(shape=(self.time_len, 6))
        for i in range(self.time_len):
            data[i, 0] = sum(self.rate[i, 0:3])
            data[i, 1] = sum(self.rate[i, 3:9])
            data[i, 2] = sum(self.rate[i, 9:22])
            data[i, 3] = sum(self.rate[i, 22:40])
            data[i, 4] = sum(self.rate[i, 40:57])
            data[i, 5] = sum(self.rate[i, 57:76])
        return data

    # Define the Counts for "Plot Time Profile"
    def __get_counts_data(self):
        data = np.zeros(shape=(self.time_len, 6))
        for i in range(self.time_len):
            data[i, 0] = sum(self.rate[i, 0:3]) * self.Time_del[i]
            data[i, 1] = sum(self.rate[i, 3:9]) * self.Time_del[i]
            data[i, 2] = sum(self.rate[i, 9:22]) * self.Time_del[i]
            data[i, 3] = sum(self.rate[i, 22:40]) * self.Time_del[i]
            data[i, 4] = sum(self.rate[i, 40:57]) * self.Time_del[i]
            data[i, 5] = sum(self.rate[i, 57:76]) * self.Time_del[i]
        return data

    # Define the Flux for "Plot Time Profile"
    def __get_flux_data(self):
        data = np.zeros(shape=(self.time_len, 6))
        for i in range(self.time_len):
            data[i, 0] = sum(self.rate[i, 0:3]) / (self.Area * self.E1)
            data[i, 1] = sum(self.rate[i, 3:9]) / (self.Area * self.E2)
            data[i, 2] = sum(self.rate[i, 9:22]) / (self.Area * self.E3)
            data[i, 3] = sum(self.rate[i, 22:40]) / (self.Area * self.E4)
            data[i, 4] = sum(self.rate[i, 40:57]) / (self.Area * self.E5)
            data[i, 5] = sum(self.rate[i, 57:76]) / (self.Area * self.E6)
        return data

    # 1. Plot Time Profile for Rate, Counts, Flux

    def __time_profile_plotting(self, data, xlabel, title, show=True, name=None):
        df = pd.DataFrame(data, index=self.TimeNew2,
                          columns=['3-6keV(Data with Bk)', '6-12keV(Data with Bk)', '12-25keV(Data with Bk)',
                                   '25-49keV(Data with Bk)', '49-100keV(Data with Bk)', '100-250keV(Data with Bk)'])
        colors = ['gray','magenta','lime', 'cyan', 'yellow', 'red']
        #df.style.set_properties(subset=['columns'], **{'height': '50px'})
        df.plot(figsize=(8, 8), drawstyle='steps-post', color = colors)
        # Define where the steps should be placed: 'steps-pre': The y value is continued constantly to the left from
        # every x position, i.e. the interval (x[i-1], x[i]] has the value y[i] 'steps-post': The y value is
        # continued constantly to the right from every x position, i.e. the interval [x[i], x[i+1]) has the value y[
        # i] 'steps-mid': Steps occur half-way between the x positions.
        #plt.rc('legend', labelsize=6)
        plt.yscale('log')
        plt.xlabel('Start time: ' + str(self.Date_start))
        plt.ylabel(xlabel)
        plt.title(title)
        #plt.text(self.x_position, 166, 'Detectors: ' + self.detectors) #rate
        #plt.text(self.x_position, 664, 'Detectors: ' + self.detectors)  # counts
        #plt.text(self.x_position, 0.023, 'Detectors: ' + self.detectors) #flux
        if show:
            plt.show()
        if name:
            plt.savefig(name, format='png')

    # RATE vs Time
    def rate_vs_time_plotting(self):
        rate_data = self.__get_rate_data()
        self.__time_profile_plotting(rate_data, 'counts/s', 'SPEX HESSI Count Rate vs Time')

    # COUNTS vs Time
    def counts_vs_time_plotting(self):
        count_data = self.__get_counts_data()

        self.__time_profile_plotting(count_data, 'counts', 'SPEX HESSI Counts vs Time')

    # FLUX vs Time
    def flux_vs_time_plotting(self):
        flux_data = self.__get_flux_data()
        self.__time_profile_plotting(flux_data, 'counts s^(-1) cm^(-2) keV^(-1)', 'SPEX HESSI Count Flux vs Time')

    # 2. Plot Spectrum
    def __plot_spectrum(self, typ):
        n = len(self.E_min)
        data = np.zeros(shape=n)
        # Define Rate for "Plot Spectrum"
        if typ == 'rate':
            for i in range(n):
                data[i] = np.mean(self.rate[:, i])
                plt.rcParams["figure.figsize"] = [8, 8]
                plt.text(21.25, 28.1881, 'Detectors: ' + self.detectors,
                         fontdict={'fontsize': 9, 'fontweight': 'medium'})
                plt.text(14.0,23.95, self.Date_start + ' to ' + self.Date_end,
                         fontdict={'fontsize': 9, 'fontweight': 'medium'})
                plt.xlabel('Energy(keV)')
                plt.ylabel('counts/s')
                plt.title('SPEX HESSI Count Rate vs Energy')
        # Define Counts for "Plot Spectrum"
        elif typ == 'counts':
            for i in range(n):
                data[i] = np.mean(self.rate[:, i] * self.sum)
                plt.rcParams["figure.figsize"] = [8, 8]
                plt.text(16.57, 71384, 'Detectors: ' + self.detectors, fontdict={'fontsize': 9, 'fontweight': 'medium'})
                plt.text(14, 65440, self.Date_start + ' to ' + self.Date_end,
                         fontdict={'fontsize': 9, 'fontweight': 'medium'})
                plt.xlabel('Energy(keV)')
                plt.ylabel('counts')
                plt.title('SPEX HESSI Counts vs Energy')
        # Define Flux for "Plot Spectrum"
        elif typ == 'flux':
            deltaE = np.zeros(shape=(n))
            for i in range(n):
                deltaE[i] = self.E_max[i] - self.E_min[i]

            for i in range(n):
                data[i] = np.mean(self.rate[:, i]) / (self.Area * deltaE[i]-2)
                plt.rcParams["figure.figsize"] = [8, 8]
                plt.text(17.095, 0.1019, 'Detectors: ' + self.detectors, fontdict={'fontsize': 9, 'fontweight': 'medium'})
                plt.text(13.132, 0.088, self.Date_start + ' to ' + self.Date_end,
                         fontdict={'fontsize': 9, 'fontweight': 'medium'})
                plt.xlabel('Energy(keV)')
                plt.ylabel('counts s^(-1) cm^(-2) keV^(-1)')
                plt.title('SPEX HESSI Count Flux vs Energy')
        else:
            print('error')
            return

        plt.plot(self.E_min, data, drawstyle='steps-post')
        plt.yscale('log')
        plt.xscale('log')
        plt.show()

    # Plot Spectrum for Rate, Counts, Flux
    # Spectrum for Rate
    def plot_spectrum_rate(self):
        self.__plot_spectrum('rate')

    # Spectrum for Counts
    def plot_spectrum_counts(self):
        self.__plot_spectrum('counts')

    # Spectrum for Flux
    def plot_spectrum_flux(self):
        self.__plot_spectrum('flux')

    # 3. Plot Spectrogram
    def __plot_spectrogram(self, typ):
        tick = np.array([str(timedelta(seconds=s)) for s in self.Time2])
        #X, Y = np.meshgrid(tick, self.E_min)
        # Define Rate for Plot Spectrogram
        if typ == 'rate':
            plt.pcolormesh(tick, self.E_min, np.transpose(self.rate), cmap='gray_r')
            # plt.xticks(np.arange(min(self.TimeNew), max(self.TimeNew), 1.0))
            plt.xlabel('Start Time: ' + self.Date_start)
            plt.ylabel('keV')
            plt.title('SPEX HESSI Count Rate Spectrogram')

        # Define Counts for Plot Spectrogram
        elif typ == 'counts':
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
            plt.pcolormesh(tick, self.E_min, np.transpose(self.rate) / (self.Area * deltaE[i]), cmap='gray_r')
            plt.xlabel('Start Time: ' + self.Date_start)
            plt.ylabel('keV')
            plt.title('SPEX HESSI Count Flux Spectrogram')


        else:
            print('error')
            return
        #plt.axis([self.TimeNew2[0], self.TimeNew2[-1], 1, 1000])

        # plt.xsticks(rotation = 90)
        T = len(tick)/5
        plt.colorbar()
        plt.yscale('log')
        plt.yticks([1, 1000])
        plt.xticks(np.arange(len(tick), step = T)) # for 1st data: step = 30 # , rotation = 90)
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
    plots = Input(".fits")
    plots.rate_vs_time_plotting()
    plots.counts_vs_time_plotting()
    plots.flux_vs_time_plotting()
    plots.plot_spectrum_rate()
    plots.plot_spectrum_counts()
    plots.plot_spectrum_flux()
    plots.plot_spectrogram_rate()
    plots.plot_spectrogram_counts()
    plots.plot_spectrogram_flux()

