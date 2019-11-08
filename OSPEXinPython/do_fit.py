from tkinter import *
from astropy.io import fits
import numpy as np
from matplotlib import pyplot as plt, figure
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import warnings
from astropy.modeling import models, fitting
import plotting


class Fitting:
    def __init__(self, root):
        self.top2 = Toplevel()
        self.top2.title('SPEX Fit Options')
        self.top2.geometry("1000x600")
        Label(self.top2,
              text="Fit Options",
              fg="red",
              font="Helvetica 12 bold italic").pack()

        # Create new frame
        # #self.frame3 = LabelFrame(self.top2, relief=RAISED, borderwidth=1)
        # #self.frame3.place(relx=0.05, rely=0.04, relheight=0.9, relwidth=0.9)
        # #Text on the top of the fram
        # #self.FitOptions = Label(self.frame3, text="Choose Fit Function Components and Set Parameters")
        # #self.FitOptions.place(relx=0.35, rely=0.065)
        # #self.Choice = Label(self.frame3, text="Choose : ")
        # #self.Choice.place(relx=0.15, rely=0.15)
        # #Listbox test

        self.lbl1 = Label(self.top2, text="Choose Fit Function Model:", fg='blue', font=("Helvetica", 11, "bold"))
        self.lbl1.place(relx=0.07, rely=0.07)
        self.lbl2 = Label(self.top2, text="Information:", fg='blue', font=("Helvetica", 11,"bold"))
        self.lbl2.place(relx=0.65, rely=0.07)

        self.lbox = Listbox(self.top2, selectmode=EXTENDED, highlightcolor = 'red', bd = 4, selectbackground = 'grey')
        self.lbox.place(relx=0.05, rely=0.15, relheight=0.45, relwidth=0.25)
        self.scroll = Scrollbar(self.top2, command=self.lbox.yview)
        self.scroll.place(relx=0.3, rely=0.15, relheight=0.45, relwidth=0.02)
        self.lbox.config(yscrollcommand=self.scroll.set)

        # New frame at the bottom
        self.frameFit = LabelFrame(self.top2, relief=RAISED, borderwidth=10)
        self.frameFit.place(relx=0.05, rely=0.63, relheight=0.25, relwidth=0.85)

        self.PlotUnits5 = Label(self.frameFit, text="Plot Units: ", fg='blue', font=("Helvetica", 11, "bold"))
        self.PlotUnits5.place(relx=0.04, rely=0.4)

        # Add button for units: Rate, Counts, Flux
        self.Component_choicesFit = ('Rate', 'Counts', 'Flux')
        self.var = StringVar(self.frameFit)
        self.var.set(self.Component_choicesFit[0])
        self.selection = OptionMenu(self.frameFit, self.var, *self.Component_choicesFit)
        self.selection.place(relx=0.15, rely=0.38, relheight=0.23, relwidth=0.15)

        self.DoFit5_Button = Button(self.frameFit, text="Do Fit", command=self._selective_fit)
        self.DoFit5_Button.place(relx=0.65, rely=0.38, relheight=0.23, relwidth=0.15)

        self.refreshButton5 = Button(self.top2, text="Refresh")
        self.refreshButton5.place(relx=0.4, rely=0.94)

        self.closeButton5 = Button(self.top2, text="Close", command=self.destroy5)
        self.closeButton5.place(relx=0.5, rely=0.94)

        self.models = ['PowerLaw1D', 'BrokenPowerLaw1D']
        for p in self.models:
            self.lbox.insert(END, p)
        self.lbox.bind("<<ListboxSelect>>", self.onSelect)
        self.list = {'PowerLaw1D': {'One dimensional power law model','\n\n',
                                    'PowerLaw1D(amplitude=1, x_0=1, alpha=1, **kwargs)'},
                     'BrokenPowerLaw1D': {'One dimensional power law model with a break',
                                          'BrokenPowerLaw1D(amplitude=1, x_break=1,',
                                          ' alpha_1=1, alpha_2=1, **kwargs)'}}
        self.list_selection = Listbox(self.top2, highlightcolor = 'red', bd = 4)
        self.list_selection.place(relx=0.45, rely=0.15, relheight=0.45, relwidth=0.45)

    def onSelect(self, event):
        widget = event.widget
        selection=widget.curselection()
        files_avalibe = []

        if selection:
            for s_i in selection:
                selected_i = self.models[s_i]
                files_avalibe += self.list[selected_i]
                print(files_avalibe)

                self.update_file_list(files_avalibe)

    def update_file_list(self, file_list):
        self.list_selection.delete(0, END)
        for i in file_list:
            self.list_selection.insert(END, i)

    def findfiles(self, val):
        sender = val.widget

    def destroy5(self):
        self.top2.destroy()

    # FIXME: essentially contains a copy of the content of Fit Power Law.py - redo it for a separate class
    def _selective_fit(self):
        """
        Selection depending on Plot Units and Function Model

        :return:
        """
        # Local file specified for file
        # Ideally, operations should be performed on the file that was loaded in the Select Input part

        hdulist = fits.open("C:/Users/a_lesya007/PycharmProjects/SpectralDataAnalysisPackage/hsi_spectrum_20020220_080000.fits")
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
        E_max = data2.E_MAX
        Area = header3[24]
        E_mean = np.mean(E_min)

        """Define Spectrum Units: Rate, Counts, Flux"""

        n = len(E_min)
        deltaE = np.zeros(shape=(n))
        for i in range(n):
            deltaE[i] = E_max[i] - E_min[i]

        # Next, we determine the PLot Units components

        # Rate
        CountRate = np.zeros(shape=(n))
        for i in range(n):
            CountRate[i] = np.mean(Rate[:, i])

        # Counts
        Counts = np.zeros(shape=(n))
        for i in range(n):
            Counts[i] = np.mean(Rate[:, i] * Time_del[:])

        # Flux
        Flux = np.zeros(shape=(n))
        for i in range(n):
            Flux[i] = np.mean(Rate[:, i] / (Area * deltaE[i] - 2))

        # Initial guess
        N = len(E_min[7:18])
        print(N)
        sigma = 1.0

        # Predefine Input Data in x and y.
        # Here we equate the three components to y1, y2, y3. The value of x is the same for all cases. Further we work only with them
        x = E_min

        y1 = CountRate
        y2 = Counts
        y3 = Flux

        error = 0.05
        y_err = sigma / np.random.rand(N)

        # -------------------------Define Fitters---------------
        
        # Fitter creates a new model for х, у, with finding the best fit values
        

        fitg1 = fitting.LevMarLSQFitter()
        fitg2 = fitting.SLSQPLSQFitter()
        fitg3 = fitting.SimplexLSQFitter()
        print(fitg1)


        """-----------------------Fitting the data using astropy.modeling------------------------------"""

        """
        PowerLaw1D(amplitude=1, x_0=1, alpha=1, **kwargs)

        One dimensional power law model.

        Parameters:	

            amplitude : float. Model amplitude at the reference point

            x_0 : float. Reference point

            alpha : float. Power law index

        """

        # Determine the default parameters for PowerLaw1D
        PowerLaw1D = models.PowerLaw1D(amplitude=0.00729868, x_0=1.72324, alpha=0)
        # Apply LevMarLSQFitter
        gPLFlux = fitg1(PowerLaw1D, x[7:18], y3[7:18], weights=1.0 / y3[7:18])
        print(gPLFlux)


        BrokenPowerLaw1D = models.BrokenPowerLaw1D(amplitude=0.0653331, x_break=1.7, alpha_1=0, alpha_2=0)

        # Apply LevMarLSQFitter
        gBPLFlux = fitg1(BrokenPowerLaw1D, x[7:18], y3[7:18], weights=1.0 / y3[7:18])
        print(gBPLFlux)

        # If user selected the Rate in Plot Units and PowerLaw1D in Choose Fit Function Model, plot:
        if (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 0):
            gPLRate = fitg1(PowerLaw1D, x[7:18], y1[7:18], weights=1.0 / y1[7:18])
            print(gPLRate)

            plt.plot(x[7:18], y1[7:18], drawstyle='steps-post', label="Rate")
            plt.plot(x[7:18], gPLRate(x[7:18]), drawstyle='steps-post', color='red',
                     label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.legend(loc=2)
            plt.title('Rate Fitting using LevMarLSQFitter')
            plt.show()
            # print('RATE & PowerLaw1D')

        # If user selected Rate in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model, plot:
        elif (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 1):
            gBPLRate = fitg1(BrokenPowerLaw1D, x[7:18], y1[7:18], weights=1.0 / y1[7:18])
            print(gBPLRate)

            plt.plot(x[7:18], y1[7:18], drawstyle='steps-post', label="Rate")
            plt.plot(x[7:18], gBPLRate(x[7:18]), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.legend(loc=2)
            plt.title('Rate Fitting using LevMarLSQFitter')
            plt.show()
            # print('RATE & BrokenPowerLaw1D')

        # If user selected Counts in Plot Units and PowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 0):
            gPLCounts = fitg1(PowerLaw1D, x[7:18], y2[7:18], weights=1.0 / y2[7:18])
            print(gPLCounts)

            plt.plot(x[7:18], y2[7:18], drawstyle='steps-post', label="Counts")
            plt.plot(x[7:18], gPLCounts(x[7:18]), drawstyle='steps-post', color='red', label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.legend(loc=2)
            plt.title('Counts Fitting using LevMarLSQFitter')
            plt.show()
            # print('COUNTS & PowerLaw1D')

        # If user selected Counts in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 1):
            gBPLCounts = fitg1(BrokenPowerLaw1D, x[7:18], y2[7:18], weights=1.0 / y2[7:18])
            print(gBPLCounts)

            plt.plot(x[7:18], y2[7:18], drawstyle='steps-post', label="Counts")
            plt.plot(x[7:18], gBPLCounts(x[7:18]), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.legend(loc=2)
            plt.title('Counts Fitting using LevMarLSQFitter')
            plt.show()
            # print('COUNTS & BrokenPowerLaw1D')

        # If user selected Flux in Plot Units and PowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 0):
            plt.plot(x[7:18], y3[7:18], drawstyle='steps-post', label="Flux")
            plt.plot(x[7:18], gPLFlux(x[7:18]), drawstyle='steps-post', color='red', label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.legend(loc=2)
            plt.title('Flux Fitting using LevMarLSQFitter')
            plt.show()
            # print('FLUX & PowerLaw1D')

        # If user selected Flux in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 1):
            """
            BrokenPowerLaw1D(amplitude=1, x_break=1, alpha_1=1, alpha_2=1, **kwargs)

            One dimensional power law model with a break.

            Parameters:	

                amplitude : float. Model amplitude at the break point.

                x_break : float. Break point.

                alpha_1 : float. Power law index for x < x_break.

                alpha_2 : float. Power law index for x > x_break.
            """
            BrokenPowerLaw1D = models.BrokenPowerLaw1D(amplitude=0.0653331, x_break=1.7, alpha_1=0, alpha_2=0)

            # Apply LevMarLSQFitter
            gBPLFlux = fitg1(BrokenPowerLaw1D, x[7:18], y3[7:18], weights=1.0 / y3[7:18])
            print(gBPLFlux)

            plt.plot(x[7:18], y3[7:18], drawstyle='steps-post', label="Flux")
            plt.plot(x[7:18], gBPLFlux(x[7:18]), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.legend(loc=2)
            plt.title('Flux Fitting using LevMarLSQFitter')
            plt.show()
            # print('FLUX & BrokenPowerLaw1D')

        # Calculate the Reduced Chi - square
        def calc_reduced_chi_square(fit, x, y, yerr, N, n_free):
            """
            fit (array) values for the fit
            x,y,yerr (arrays) data
            N total number of points
            n_free number of parameters we are fitting
            """
            return 1.0 / (N - n_free) * sum(((fit - y) / y_err) ** 2)

        reduced_chi_squared = calc_reduced_chi_square(gPLFlux(x[7:18]), x[7:18], y3[7:18], y3[7:18], N, 3)
        print('Reduced Chi Squared with LinearLSQFitter: {}'.format(reduced_chi_squared))
