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
from astropy.modeling.models import custom_model
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
        self.lbl2.place(relx=0.44, rely=0.07) #set the position
        
        self.lbl3 = Label(self.top2, text="Set function components and x, y parameters:", fg='blue', font=("Helvetica", 11,"bold")) #name the scrollbar
        self.lbl3.place(relx=0.65, rely=0.07) #set the position
        def new_window(): # new window definition
            newwin = Toplevel(root)
            newwin.title('Function values') #title of the window
            newwin.geometry("600x400") #size of the new window
            display = Label(newwin, text="Choose function values: ", fg='blue', font=("Helvetica", 11,"bold"))
            display.place(relx=0.04, rely=0.07)
        self.Value_Button = Button(self.top2, text="Function value", command = new_window) #place a "Function value" button
        self.Value_Button.place(relx=0.75, rely=0.20, relheight=0.05, relwidth=0.13) #locate

        self.X_Label = Label(self.top2, text="Set X") #place a "Set X" button 
        self.X_Label.place(relx=0.65, rely=0.30, relheight=0.05, relwidth=0.13) #locate

        self.Y_Label = Label(self.top2, text="Set Y") #place a "Set Y" button 
        self.Y_Label.place(relx=0.65, rely=0.40, relheight=0.05, relwidth=0.13) #locate

        self.e1 = Entry(self.top2)
        self.e1.place(relx=0.75, rely=0.30, relheight=0.05,relwidth=0.20)               
        self.e2 = Entry(self.top2)
        self.e2.place(relx=0.75, rely=0.40, relheight=0.05,relwidth=0.20)

        def show_entry_fields():
            print("Set X: %s\nSet Y: %s" % (self.e1.get(), self.e2.get()))

        self.show_Button = Button(self.top2, text = "Show", command = show_entry_fields)
        self.show_Button.place(relx=0.75, rely=0.50)







        """ 
        On the left: place a list of text alternatives (listbox)
        The user can choose(highlight) one of the options
        Options(functions):
        1) One Dimensional Power Law 
        2) 1-D Broken Power Law
        3) Gaussian
        4) Polynomial
        5) Exponential
        6) Single Power Law Times an Exponetial
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

        self.models = ['PowerLaw1D', 'BrokenPowerLaw1D', 'Gaussian', 'Polynomial', 'Exponential', 'Single Power Law Times an Exponetial'] #function names
        for p in self.models:
            self.lbox.insert(END, p)
        self.lbox.bind("<<ListboxSelect>>", self.onSelect)
        self.list = {'PowerLaw1D': {'One dimensional power law model','\n\n',
                                    'amplitude – model amplitude at the reference energy', '\n',
                                    'x – reference energy', '\n', 'alpha – power law index'}, #if user choose PowerLaw1D, display
                     'BrokenPowerLaw1D': {'One dimensional power law model with a break','\n\n',
                                          'amplitude - model amplitude at the break energy', '\n',
                                          'alpha 1 – power law index for x<x_break', '\n',
                                          'alpha 2 – power law index for x>x_break'}, #if user choose BrokenPowerLaw1D, display
                     'Gaussian': {'Single Gaussian function(high quality), width in sigma', '\n', 
                                  'does not go through DRM','\n',
                                  'This function returns the sum of Gaussian and ', '\n', '2nd order Polynomial',
                                  'amplitude - integrated intensity, mean - centroid', '\n', 'stddev - sigma'}, #if user choose Gaussian, display
                     'Polynomial': {'Polynomial function with offset in x','\n',
                     'c0 - 0th order coefficient', '\n', 'c1 - 1st order coefficient', '\n', 'c2 - 2nd order coefficient', '\n',
                     'c3 - 3rd order coefficient', '\n', 'c4 - 4th order coefficient', '\n', 'c5 - x offset, such that function value at x = c5 is C0 '}, #Polynomial
                     'Exponential': {'Exponential function', '\n', 't0 - Normalization', '\n', 't1 - Pseudo temperature'}, #Exponential
                     'Single Power Law Times an Exponetial': {'Multiplication of Single Power Law and Exponential', '\n',
                     'p0 - normalization at epivot for power-law', '\n', 'p1 - negative power - law index', '\n',
                     'p2 - epivot (kEv) for power - law', '\n', 'e1 - normalization for exponential', '\n', 'e2 - pseudo temperature for exponential'}} 
                      #Single Power Law Times an Exponential
        self.list_selection = Listbox(self.top2, highlightcolor = 'red', bd = 4)
        self.list_selection.place(relx=0.33, rely=0.15, relheight=0.45, relwidth=0.30)

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
        """ x - independent variable, nominally energy in keV """

        y1 = CountRate
        y2 = Counts
        y3 = Flux
        """ y - Plot Unit """
        # def find_all_indexes(input_str, search_str):
        #     l1 = []
        #     length = len(input_str)
        #     index = 0
        #     while index < length:
        #         i = input_str.find(search_str, index)
        #         if i == -1:
        #             return l1
        #         l1.append(i)
        #         index = i + 1
        #     return l1
        # print(find_all_indexes(str(E_min), str(E_min[0:-1])))
        indexesX = np.where((x <= x[-1]) & (x >= x[0]))
        print(indexesX)
        indexesY1 = np.where((y3 < y3[-1]) & (y3 > y3[0]))
        print(indexesY1)
        # nX = int(input(self.e1.get()))
        # nY = int(input(self.e1.get()))
        # keyword_arrayX = []
        # keyword_arrayY = []
        # first_E_min = indexes[0]
        # last_E_min = indexes[-1]
        #
        # if first_E_min < arrayX[0] and last_E_min<arrayX[-1]:

#################################################### Define Fitters ######################################################
        
        # Fitter creates a new model for x and у, with finding the best fit values
        fitg1 = fitting.LevMarLSQFitter()
        #print(fitg1)

        """ 
        Levenberg - Marquandt algorithm for non - linear least - squares optimization

        The algorithm works by minimizing the squared residuals, defined as:
            
                Residual^2 = (y - f(t))^2 ,
 
        where y is the measured dependent variable;

        f(t) is the calculated value

        The LM algorithm is an iterative process, guessing at the solution of the best minimum


         """

#################################################### Fitting the data using astropy.modeling ###############################

        # Define a One dimensional power law model with initial guess
        PowerLaw1D = models.PowerLaw1D() #(amplitude=1, x_0=3, alpha=50, fixed = {'alpha': True})

        """
        PowerLaw1D(amplitude=1, x_0=1, alpha=1, **kwargs)

        One dimensional power law model.

        Parameters:	

            amplitude : float. Model amplitude at the reference point.

            x_0 : float. Reference point.

            alpha : float. Power law index.
        """
        
        # Define a One dimensional broken power law model 
        BrokenPowerLaw1D = models.BrokenPowerLaw1D(amplitude=1, x_break=3, alpha_1=400, alpha_2=1.93, fixed = {'alpha_1': True, 'alpha_2': True})

        """
        BrokenPowerLaw1D(amplitude=1, x_break=1, alpha_1=1, alpha_2=1, **kwargs)


        One dimensional power law model with a break.

        Parameters:	

            amplitude : float. Model amplitude at the break point.

            x_break : float. Break point.

            alpha_1 : float. Power law index for x < x_break.

            alpha_2 : float. Power law index for x > x_break.
        """   
        
        # Define a Gaussian model 
        ginit = models.Gaussian1D(1000, 6.7, 0.1, fixed = {'mean': True, 'stddev': True})
        #(1000, 6.7, 0.1)

        """
        One dimensional Gaussian model

        Parameters:

            amplitude: Amplitude of the Gaussian.
            
            mean: Mean of the Gaussian.

            stddev: Standard deviation of the Gaussian.
       
        Other Parameters:

            fixed : optional. A dictionary {parameter_name: boolean} of parameters to not be varied during fitting. True means the parameter is held fixed. 
            Alternatively the fixed property of a parameter may be used.

    
            tied: optional. A dictionary {parameter_name: callable} of parameters which are linked to some other parameter.

            The dictionary values are callables providing the linking relationship. Alternatively the tied property of a parameter may be used.

    
            bounds: optional. A dictionary {parameter_name: value} of lower and upper bounds of parameters. 
            Keys are parameter names. Values are a list or a tuple of length 2 giving the desired range for the parameter.
            Alternatively, the min and max properties of a parameter may be used.

            eqcons: optional. A list of functions of length n such that eqcons[j](x0,*args) == 0.0 in a successfully optimized problem.

        
            ineqcons: optional. A list of functions of length n such that ieqcons[j](x0,*args) >= 0.0 is a successfully optimized problem. 

        """
        p_init = models.Polynomial1D(2) # Define 2nd order Polynomial function
        #p_init.parameters = [1,1,1]

        """
        1D Polynomial model.
        
        
        Parameters:

            degree: Degree of the series.

        
            domain: Optional.

            window: Optional. If None, it is set to [-1,1] Fitters will remap the domain to this window.

        
            **params: Keyword. Value pairs, representing parameter_name: value.

        

        Other Parameters:

            fixed: optional. A dictionary {parameter_name: boolean} of parameters to not be varied during fitting. True means the parameter is held fixed. 
            Alternatively the fixed property of a parameter may be used.

            tied: optional. A dictionary {parameter_name: callable} of parameters which are linked to some other parameter.
            The dictionary values are callables providing the linking relationship.
            Alternatively the tied property of a parameter may be used.
   
            bounds: optional. A dictionary {parameter_name: value} of lower and upper bounds of parameters. Keys are parameter names. 
            Values are a list or a tuple of length 2 giving the desired range for the parameter. 
            Alternatively, the min and max properties of a parameter may be used.

            eqcons: optional.  A list of functions of length n such that eqcons[j](x0,*args) == 0.0 in a successfully optimized problem.

       
            ineqcons: optional. A list of functions of length n such that ieqcons[j](x0,*args) >= 0.0 is a successfully optimized problem.
        """

        Model = ginit + p_init 

        """ The Model(function) returns the sum of a Gaussian and 2nd order Polynomial """

        # Define 6th order Polynomial function
        Poly = models.Polynomial1D(5, window=[-10, 10], fixed = {'c3': True, 'c4': True})
        Poly.parameters = [1,1,1,1,1,50]
        
        # Define Exponential function
        @custom_model
        def func_exponential(x, t1 = 1., t2 = 1.):
            return (np.exp(t1 - x/t2))
        exp = func_exponential(t1=1., t2 = 1.)

        """
        Purpose: Exponential function

        Category: spectral fitting

        Inputs:
        t0 - Normalization
        t1 - Pseudo temperature

        Outputs:
        result of function, exponential
        """

        # Define Single Power Law Times an Exponential
        @custom_model
        def func_exponential_powerlaw(x, p0 = 1., p1 = 1., p2 = 1., e3 = 1.,e4 =1.):
            return ((p0*(x/p2)**p1)*(np.exp(e3-x/e4)))
        exp_powerlaw = func_exponential_powerlaw(p0=1., p1 = 3., p2= 50., e3= 1.,e4=1., fixed = {'p2': True})

        """
        Purpose: single power - law times an exponential

        Category: spectral fitting

        Inputs:
        p - first 3 parameters describe the single power - law, e - describes the exponential
 
        p0 = noramlization at epivot for power - law
        p1 = negative power - law index
        p2 = epivot (keV) for power - law

        e3 = normalization for exponential
        e4 = pseudo temperature for exponential

        Outputs:
        result of function, a power - law times an exponential
        """



######################### Define the functions for Rate ###############################

        # If user select the Rate in Plot Units and PowerLaw1D in Choose Fit Function Model, plot:
        if (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 0):
            gPLRate = fitg1(PowerLaw1D, x, y1, weights=1.0 / y1)
            print(gPLRate)
            plt.figure()
            plt.plot(x, y1, drawstyle='steps-post', label="Rate")
            plt.plot(x, gPLRate(x), drawstyle='steps-post', color='red', label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 100, ymin = 0.1) #FIXME: find a solution for general case
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.legend(loc=2)
            plt.title('Rate Fitting using 1D Power Law Model')
            plt.show()
            # print('RATE & PowerLaw1D')

        # If user select Rate in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model, plot:
        elif (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 1):
            gBPLRate = fitg1(BrokenPowerLaw1D, x, y1, weights=1.0 / y1)
            print(gBPLRate)
            plt.figure()
            plt.plot(x, y1, drawstyle='steps-post', label="Rate")
            plt.plot(x, gBPLRate(x), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 100, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.legend(loc=2)
            plt.title('Rate Fitting using 1D Broken Power Law Model')
            plt.show()
            # print('RATE & BrokenPowerLaw1D')

        # If user select Rate in Plot Units and Gaussian in Choose Fit Function Model:
        elif (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 2):
            gaussianRate = fitg1(Model,x,y1, weights = 1.0/y1)
            print(gaussianRate)
            plt.figure()
            plt.plot(x,y1,drawstyle='steps-post', label = "Rate")
            plt.plot(x,gaussianRate(x),drawstyle='steps-pre', label='Gaussian')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 100, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.title('Rate Fitting using Gaussian Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Rate in Plot Units and Polynomial in Choose Fit Function Model:
        elif (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 3):
            PolyRate = fitg1(Poly,x,y1, weights = 1.0/y1)
            print(PolyRate)
            plt.figure()
            plt.plot(x,y1,drawstyle='steps-post', label = "Rate")
            plt.plot(x,PolyRate(x),drawstyle='steps-pre', label='Polynomial')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 100, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.title('Rate Fitting using Polynomial Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Rate in Plot Units and Exponential in Choose Fit Function Model:
        elif (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 4):
            expRate = fitg1(exp, x, y1)
            print(expRate)
            plt.figure()
            plt.plot(x,y1,drawstyle='steps-post', label = "Rate")
            plt.plot(x,expRate(x),drawstyle='steps-pre', label='Exponential')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 100, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.title('Rate Fitting using Exponential Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Rate in Plot Units and Exponential Power Law in Choose Fit Function Model:
        elif (self.var.get() == 'Rate') & (self.lbox.curselection()[0] == 5):
            ExpPLRate = fitg1(exp_powerlaw, x, y1, weights=1.0 / y1)
            print(ExpPLRate)
            plt.figure()
            plt.plot(x, y1, drawstyle='steps-post', label="Rate")
            plt.plot(x, ExpPLRate(x), drawstyle='steps-post', color='red', label="ExpPowerLaw")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 100, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Rate(Counts/s)')
            plt.legend(loc=2)
            plt.title('Rate Fitting using Exponential Power Law Model')
            plt.show()

        

######################### Define the functions for Counts ###############################

        # If user select Counts in Plot Units and PowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 0):
            gPLCounts = fitg1(PowerLaw1D, x, y2, weights=1.0 / y2)
            print(gPLCounts)
            plt.figure()
            plt.plot(x, y2, drawstyle='steps-post', label="Counts")
            plt.plot(x, gPLCounts(x), drawstyle='steps-post', color='red', label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1000, ymin = 0.1) #FIXME: find a solution for general case
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.legend(loc=2)
            plt.title('Counts Fitting using 1D Power Law Model')
            plt.show()
            # print('COUNTS & PowerLaw1D')

        # If user select Counts in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 1):
            gBPLCounts = fitg1(BrokenPowerLaw1D, x, y2, weights=1.0 / y2)
            print(gBPLCounts)
            plt.figure()
            plt.plot(x, y2, drawstyle='steps-post', label="Counts")
            plt.plot(x, gBPLCounts(x), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1000, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.legend(loc=2)
            plt.title('Counts Fitting using 1D Broken Power Law Model')
            plt.show()
            # print('COUNTS & BrokenPowerLaw1D')

        # If user select Counts in Plot Units and Gaussian in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 2):
            gaussianCounts = fitg1(Model,x,y2, weights = 1.0/y2)
            print(gaussianCounts)
            plt.figure()
            plt.plot(x,y2,drawstyle='steps-post', label = "Counts")
            plt.plot(x,gaussianCounts(x),drawstyle='steps-pre', label='Gaussian')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1000, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.title('Counts Fitting using Gaussian Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Counts in Plot Units and Polynomial in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 3):
            PolyCounts = fitg1(Poly,x,y2, weights = 1.0/y2)
            print(PolyCounts)
            plt.figure()
            plt.plot(x,y2,drawstyle='steps-post', label = "Counts")
            plt.plot(x,PolyCounts(x),drawstyle='steps-pre', label='Polynomial')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1000, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.title('Counts Fitting using Polynomial Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Counts in Plot Units and Exponential in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 4):
            expCounts = fitg1(exp, x, y2, weights=1.0 / y2)
            print(expCounts)
            plt.figure()
            plt.plot(x,y2,drawstyle='steps-post', label = "Counts")
            plt.plot(x,expCounts(x),drawstyle='steps-pre', label='Exponential')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1000, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.title('Counts Fitting using Exponential Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Counts in Plot Units and Exponential Power Law in Choose Fit Function Model:
        elif (self.var.get() == 'Counts') & (self.lbox.curselection()[0] == 5):
            ExpPLCounts = fitg1(exp_powerlaw, x, y2, weights=1.0 / y2)
            print(ExpPLCounts)
            plt.figure()
            plt.plot(x, y2, drawstyle='steps-post', label="Counts")
            plt.plot(x, ExpPLCounts(x), drawstyle='steps-post', color='red', label="ExpPowerLaw")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1000, ymin = 0.1)
            plt.xlabel('Energy(keV)')
            plt.ylabel('Counts(Counts)')
            plt.legend(loc=2)
            plt.title('Counts Fitting using Exponential Power Law Model')
            plt.show()

######################### Define the functions for Flux ###############################

        # If user select Flux in Plot Units and PowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 0):
            gPLFlux = fitg1(PowerLaw1D, x, y3, weights=1.0 / y3)
            plt.figure()
            plt.plot(x, y3, drawstyle='steps-post', label="Flux")
            plt.plot(x, gPLFlux(x), drawstyle='steps-post', color='red', label="PowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1, ymin = 0.0001) #FIXME: find a solution for general case
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.legend(loc=2)
            plt.title('Flux Fitting using 1D Power Law Model')
            plt.show()
            # print('FLUX & PowerLaw1D')

        # If user select Flux in Plot Units and BrokenPowerLaw1D in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 1):

            # Apply Levenberg - Marquandt algorithm
            gBPLFlux = fitg1(BrokenPowerLaw1D, x, y3, weights=1.0 / y3)
            print(gBPLFlux)
            plt.figure()
            plt.plot(x, y3, drawstyle='steps-post', label="Flux")
            plt.plot(x, gBPLFlux(x), drawstyle='steps-post', color='red', label="BrokenPowerLaw1D")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1, ymin = 0.0001) #FIXME: find a solution for general case
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.legend(loc=2)
            plt.title('Flux Fitting using 1D Broken Power Law Model')
            plt.show()
            # print('FLUX & BrokenPowerLaw1D')

        # If user select Flux in Plot Units and Gaussian in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 2):
            gaussianFlux = fitg1(Model,x,y3, weights = 1.0/y3)
            print(gaussianFlux)
            plt.figure()
            plt.plot(x,y3,drawstyle='steps-post', label = "Flux")
            plt.plot(x,gaussianFlux(x),drawstyle='steps-pre', label='Gaussian')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1, ymin = 0.0001) #FIXME: find a solution for general case
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.title('Flux Fitting using Gaussian Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Flux in Plot Units and Polynomial in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 3):
            PolyFlux = fitg1(Poly,x,y3, weights = 1.0/y3)
            print(PolyFlux)
            plt.figure()
            plt.plot(x,y3,drawstyle='steps-post', label = "Flux")
            plt.plot(x,PolyFlux(x),drawstyle='steps-pre', label='Polynomial')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1, ymin = 0.0001) #FIXME: find a solution for general case
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.title('Flux Fitting using Polynomial Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Flux in Plot Units and Exponential in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 4):
            expFlux = fitg1(exp, x, y3)
            print(expFlux)
            plt.figure()
            plt.plot(x,y3,drawstyle='steps-post', label = "Flux")
            plt.plot(x,expFlux(x),drawstyle='steps-pre', label='Exponential')
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1, ymin = 0.0001) #FIXME: find a solution for general case
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.title('Flux Fitting using Exponential Model')
            plt.legend(loc=2)
            plt.show()

        # If user select Flux in Plot Units and Exponential Power Law in Choose Fit Function Model:
        elif (self.var.get() == 'Flux') & (self.lbox.curselection()[0] == 5):
            ExpPLFlux = fitg1(exp_powerlaw, x, y3, weights=1.0 / y3)
            print(ExpPLFlux)
            plt.figure()
            plt.plot(x, y3, drawstyle='steps-post', label="Flux")
            plt.plot(x, ExpPLFlux(x), drawstyle='steps-post', color='red', label="ExpPowerLaw")
            plt.yscale('log')
            plt.xscale('log')
            plt.ylim(ymax = 1, ymin = 0.0001) #FIXME: find a solution for general case
            plt.xlabel('Energy(keV)')
            plt.ylabel('Flux(Counts/s cm(-2) keV(-1))')
            plt.legend(loc=2)
            plt.title('Flux Fitting using Exponential Power Law Model')
            plt.show()


        # FIXME:
        # Calculate the Reduced Chi - square, test version
        # Initial guess
        #N = len(E_min) #total number of points
        #print(N)
        #sigma = 1.0
        #y_err = sigma / E_min

        #def calc_reduced_chi_square(fit, x, y, yerr, N, n_free):
            #"""
            #fit (array) values for the fit
            #x,y,y_err (arrays) data
            #N total number of points
            #n_free number of parameters we are fitting
            #"""
            #return 1.0 / (N - n_free) * sum(((fit - y) / y_err) ** 2)

        #reduced_chi_squared = calc_reduced_chi_square(gPLFlux(x), x, y3, y3, N, 3) # calculate for Flux
        #print('Reduced Chi Squared with Levenberg - Marquandt algorithm: {}'.format(reduced_chi_squared))
