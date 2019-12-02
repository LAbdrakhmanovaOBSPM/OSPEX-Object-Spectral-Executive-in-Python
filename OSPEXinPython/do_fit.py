"""

  Application: Data processing software for RHESSI and STIX instruments

  Start date: 11/03/2019

  Creators: Liaisian Abdrakhmanova, Abdallah Hamini, Aichatou Aboubacar

  Organization: LESIA, Observatory of Paris, France
  
  Graphical User Interface: GUI was created using tkinter library

  Usage: information to test the program provided in Requirements file

  Status = 'Development'

"""


#import the libraries
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
    """ 

    Class to perform a spectrum fitting

    """
    #create a new window called 'SPEX Fit Options'
    fname=None
    def __init__(self, root):
        self.top2 = Toplevel()
        self.top2.title('SPEX Fit Options') #title of the window
        self.top2.geometry("1000x600") #size of the new window
        Label(self.top2,
              text="Fit Options", #place the text at the top of the window  
              fg="red", #in red
              font="Helvetica 12 bold italic").pack() #with specific text font

        self.root = root
        self.sepBkVar = IntVar()

        self.lbl1 = Label(self.top2, text="Choose Fit Function Model:", fg='blue', font=("Helvetica", 11, "bold")) #name the listbox
        self.lbl1.place(relx=0.07, rely=0.07) # set the position on window

        self.lbl2 = Label(self.top2, text="Information:", fg='blue', font=("Helvetica", 11,"bold")) #name the scrollbar
        self.lbl2.place(relx=0.65, rely=0.07) #set the position
        
        """ 
        On the left: place a list of text alternatives (listbox)
        The user can choose(highlight) one of the options
        Options(functions):
        1) One Dimensional Power Law 
        2) 1-D Broken Power Law 
        """

        self.lbox = Listbox(self.top2, selectmode=EXTENDED, highlightcolor = 'red', bd = 4, selectbackground = 'grey')
        self.lbox.place(relx=0.05, rely=0.15, relheight=0.45, relwidth=0.25)

        """ 
        On the right: place an 'entry text' Scrollbar widget (scrollbar)
        When user highlight the function, displays the text information about function description and input parameters
        """

        self.scroll = Scrollbar(self.top2, command=self.lbox.yview)
        self.scroll.place(relx=0.3, rely=0.15, relheight=0.45, relwidth=0.02)
        self.lbox.config(yscrollcommand=self.scroll.set)

        # New frame at the bottom. Locate there 'Plot Units' and 'Do Fit' widgets
        self.frameFit = LabelFrame(self.top2, relief=RAISED, borderwidth=10) #determine the border of the frame and size
        self.frameFit.place(relx=0.05, rely=0.63, relheight=0.25, relwidth=0.85) # the frame position

        self.PlotUnits5 = Label(self.frameFit, text="Plot Units: ", fg='blue', font=("Helvetica", 11, "bold")) #lay out new text file 
        self.PlotUnits5.place(relx=0.04, rely=0.4)

        # Add button for Units: Rate, Counts, Flux
        # Allows user to make a choice between three parameters
        self.Component_choicesFit = ('Rate', 'Counts', 'Flux')
        self.var = StringVar(self.frameFit)
        self.var.set(self.Component_choicesFit[0])
        self.selection = OptionMenu(self.frameFit, self.var, *self.Component_choicesFit)
        self.selection.place(relx=0.15, rely=0.38, relheight=0.23, relwidth=0.15)

        self.DoFit5_Button = Button(self.frameFit, text="Do Fit", command=self._selective_fit) #place a "Do Fit" button 
        self.DoFit5_Button.place(relx=0.65, rely=0.38, relheight=0.23, relwidth=0.15) #locate

        self.refreshButton5 = Button(self.top2, text="Refresh") #add Refresh button at the buttom
                                                                #resets original view
        self.refreshButton5.place(relx=0.4, rely=0.94)

        self.closeButton5 = Button(self.top2, text="Close", command=self.destroy5) #add Close button
                                                                                   #Close "Fit Options" window


        """Next, we fill scrollbar with information related to each function
        """
        self.closeButton5.place(relx=0.5, rely=0.94)

        self.models = ['PowerLaw1D', 'BrokenPowerLaw1D'] #function names, put them in listbox
        for p in self.models:
            self.lbox.insert(END, p)
        self.lbox.bind("<<ListboxSelect>>", self.onSelect)
        self.list = {'PowerLaw1D': {'One dimensional power law model','\n\n',
                                    'PowerLaw1D(amplitude=1, x_0=1, alpha=1, **kwargs)'}, #if user choose PowerLaw1D, display
                     'BrokenPowerLaw1D': {'One dimensional power law model with a break',
                                          'BrokenPowerLaw1D(amplitude=1, x_break=1,',
                                          ' alpha_1=1, alpha_2=1, **kwargs)'}} #if user choose BrokenPowerLaw1D, display
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

    def _selective_fit(self):

       """
        Selection depending on Plot Units and Function Model

       """
       # load chosen file in Select Input section 
       fname = Fitting.fname

       if fname is None: # if file not choosen, print
         print('Please, choose input file')

       else:
        hdulist = fits.open(fname) 
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

        # Define the range for Low and High energies
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

        # Predefine Input Data in x and y
        # We equate three components to y1, y2, y3. The value of x is the same for all cases
        x = E_min

        y1 = CountRate
        y2 = Counts
        y3 = Flux

        

#################################################### Define Fitters ######################################################
        
        # Fitter creates a new model for x and у, with finding the best fit values
        fitg1 = fitting.LevMarLSQFitter()
        print(fitg1)

        """ 
        Levenberg - Marquandt algorithm for non - linear least - squares optimization

        The algorithm works by minimizing the squared residuals, defined as:
            
                Residual^2 = (y - f(t))^2 ,
 
        where y is the measured dependent variable;

        f(t) is the calculated value

        The LM algorithm is an iterative process, guessing at the solution of the best minimum


         """

#################################################### Fitting the data using astropy.modeling ###############################

        """
        PowerLaw1D(amplitude=1, x_0=1, alpha=1, **kwargs)

        One dimensional power law model.

        Parameters:	

            amplitude : float. Model amplitude at the reference point

            x_0 : float. Reference point

            alpha : float. Power law index

        """

        # Determine the default parameters for PowerLaw1D
        PowerLaw1D = models.PowerLaw1D(amplitude=1, x_0=3, alpha=50)
        # Apply LevMarLSQFitter
        gPLFlux = fitg1(PowerLaw1D, x, y3, weights=1.0 / y3) # value for weights from IDL
        print(gPLFlux)


        BrokenPowerLaw1D = models.BrokenPowerLaw1D(amplitude=1, x_break=3, alpha_1=400, alpha_2=1.93, fixed = {'alpha_1': True, 'alpha_2': True})

        # Apply LevMarLSQFitter
        gBPLFlux = fitg1(BrokenPowerLaw1D, x, y3, weights=1.0 / y3)
        print(gBPLFlux)

        # If user select the Rate in Plot Units and PowerLaw1D in Choose Fit Function Model, plot:
        if (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 0):
            gPLRate = fitg1(PowerLaw1D, x, y1, weights=1.0 / y1)
            print(gPLRate)

            plt.plot(x, y1, drawstyle='steps-post', label="Rate")
            plt.plot(x, gPLRate(x), drawstyle='steps-post', color='red',
                     label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.legend(loc=2)
            plt.title('Rate Fitting using LevMarLSQFitter')
            plt.show()
            # print('RATE & PowerLaw1D')

        # If user select Rate in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model, plot:
        elif (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 1):
            gBPLRate = fitg1(BrokenPowerLaw1D, x, y1, weights=1.0 / y1)
            print(gBPLRate)

            plt.plot(x, y1, drawstyle='steps-post', label="Rate")
            plt.plot(x, gBPLRate(x), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.legend(loc=2)
            plt.title('Rate Fitting using LevMarLSQFitter')
            plt.show()
            # print('RATE & BrokenPowerLaw1D')

        # If user select Counts in Plot Units and PowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 0):
            gPLCounts = fitg1(PowerLaw1D, x, y2, weights=1.0 / y2)
            print(gPLCounts)

            plt.plot(x, y2, drawstyle='steps-post', label="Counts")
            plt.plot(x, gPLCounts(x), drawstyle='steps-post', color='red', label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.legend(loc=2)
            plt.title('Counts Fitting using LevMarLSQFitter')
            plt.show()
            # print('COUNTS & PowerLaw1D')

        # If user select Counts in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 1):
            gBPLCounts = fitg1(BrokenPowerLaw1D, x, y2, weights=1.0 / y2)
            print(gBPLCounts)

            plt.plot(x, y2, drawstyle='steps-post', label="Counts")
            plt.plot(x, gBPLCounts(x), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.legend(loc=2)
            plt.title('Counts Fitting using LevMarLSQFitter')
            plt.show()
            # print('COUNTS & BrokenPowerLaw1D')

        # If user select Flux in Plot Units and PowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 0):
            plt.plot(x, y3, drawstyle='steps-post', label="Flux")
            plt.plot(x, gPLFlux(x), drawstyle='steps-post', color='red', label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.legend(loc=2)
            plt.title('Flux Fitting using LevMarLSQFitter')
            plt.show()
            # print('FLUX & PowerLaw1D')

        # If user select Flux in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model:
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

            # Apply Levenberg - Marquandt algorithm
            gBPLFlux = fitg1(BrokenPowerLaw1D, x, y3, weights=1.0 / y3)
            print(gBPLFlux)

            plt.plot(x, y3, drawstyle='steps-post', label="Flux")
            plt.plot(x, gBPLFlux(x), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.legend(loc=2)
            plt.title('Flux Fitting using LevMarLSQFitter')
            plt.show()
            # print('FLUX & BrokenPowerLaw1D')

        # Calculate the Reduced Chi - square, test version
        # Initial guess
        N = len(E_min) #total number of points
        print(N)
        sigma = 1.0
        y_err = sigma / E_min

        def calc_reduced_chi_square(fit, x, y, yerr, N, n_free):
            """
            fit (array) values for the fit
            x,y,y_err (arrays) data
            N total number of points
            n_free number of parameters we are fitting
            """
            return 1.0 / (N - n_free) * sum(((fit - y) / y_err) ** 2)

        reduced_chi_squared = calc_reduced_chi_square(gPLFlux(x), x, y3, y3, N, 3) # calculate for Flux
        print('Reduced Chi Squared with LinearLSQFitter: {}'.format(reduced_chi_squared))
