from tkinter import *
from astropy.io import fits
import re
import pandas as pd
import plotting
import background_plot
import warnings
import second


class SelectEnergyWindow():
    """Class to create a Select Energy Window"""
    fname=None
    def __init__(self):
        self.top1 = Toplevel()
        self.top1.title('SPEX Energy Bands for Background')
        self.top1.geometry("450x500")
        Label(self.top1,
              text="Select Energy Bands for Background",
              fg="black",
              font="Helvetica 12 bold").pack()
        Label(self.top1,
              text="Left/right click to define start/end of intervals",
              fg="black",
              font="Helvetica 8").pack()
        Label(self.top1,
              text="Left double click on a plotted interval for editing options",
              fg="black",
              font="Helvetica 8").pack()

        self.hdul = None

        #self.root = root
        #self.sepBkVar = BooleanVar()
        self.sepBkVar = IntVar()
        #self.sepBkVar.set(1)
        # self.root.wm_atributes("-disabled", True)

        #########################################################################################
##        """                         First frame                                     """
##
        self.frame1 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
        self.frame1.place(relx=0.05, rely=0.17, relheight=0.25, relwidth=0.9)

        """ Current Intervals"""
        self.lblCurrentIntervals = Label(self.frame1, text="Current Intervals:")
        self.lblCurrentIntervals.place(relx=0.01, rely=0.25)

        self.CurrentIntervals_choices = ('Interval 0, 3.000 to 6.000', 'Interval 1, 6.000 to 12.000', 'Interval 2, 12.000 to 25.000',
                                         'Interval 3, 25.000 to 50.000', 'Interval 4, 50.000 to 100.000', 'Interval 5, 100.000 to 300.000')
        self.CurrentIntervalsVar = StringVar(self.frame1)
        self.CurrentIntervalsVar.set(self.CurrentIntervals_choices[0])
        self.CurrentIntervalsSelection = OptionMenu(self.frame1, self.CurrentIntervalsVar, *self.CurrentIntervals_choices)
        self.CurrentIntervalsSelection.place(relx=0.28, rely=0.25)
        #self.CurrentEnergySelection.config(state="disabled")

        self.lblIntervals = Label(self.frame1, text="#Intervals = 6")
        self.lblIntervals.place(relx=0.7, rely=0.25)

        self.DeleteSelectedInterv = Button(self.frame1, text="Delete selected interval", state=DISABLED)
        self.DeleteSelectedInterv.place(relx=0.01, rely=0.7)

        self.EditSelectedInterv = Button(self.frame1, text="Edit selected interval ...", command=lambda: self.editSelectedInterval(self.top1)) #, command=self.editSelectedInterval)
        self.EditSelectedInterv.place(relx=0.35, rely=0.7)


        self.EditInterv = Button(self.frame1, text="Edit interval ...", state=DISABLED)
        self.EditInterv.place(relx=0.7, rely=0.7)
##
##        #################################################################################
##        """                          Second frame                             """
##        self.frame2 = Frame(self.top1, relief=RAISED, borderwidth=2)
##        self.frame2.place(relx=0.05, rely=0.14, relheight=0.27, relwidth=0.9)
        self.frame2 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
        self.frame2.place(relx=0.05, rely=0.42, relheight=0.34, relwidth=0.9)

        self.OptionsCursor = Label(self.frame2, text="Options for cursor selection:")
        self.OptionsCursor.place(relx=0.03, rely=0.07)

        self.ContiguousInterv = Checkbutton(self.frame2, text="Contiguous intervals", state=NORMAL) 
        self.ContiguousInterv.place(relx=0.01, rely=0.22)

        self.ff = Checkbutton(self.frame2, text="Contiguous intervals", state=NORMAL) 
        self.ff.place(relx=0.01, rely=0.37)

        self.EditOptionParam = Label(self.frame2, text="Editing Option Parameters:")
        self.EditOptionParam.place(relx=0.45, rely=0.07)

        self.SubIntervalName = Label(self.frame2, text="# Sub-intervals(N):")
        self.SubIntervalName.place(relx=0.45, rely=0.22)
        self.SubInterval = Entry(self.frame2, width=7)
        self.SubInterval.place(relx=0.72, rely=0.22)

        self.LenghtSubIntervalName = Label(self.frame2, text="Length of Sub-intervals:")
        self.LenghtSubIntervalName.place(relx=0.45, rely=0.44)
        self.LenghtSubInterval = Entry(self.frame2, width=7)
        self.LenghtSubInterval.place(relx=0.77, rely=0.44)

        self.DataBinsName = Label(self.frame2, text="# Data Bins per Sub-interval(M):")
        self.DataBinsName.place(relx=0.45, rely=0.66)
        self.DataBins = Entry(self.frame2, width=7)
        self.DataBins.place(relx=0.86, rely=0.66)

##################################################################################

        self.AdjustData = Button(self.top1, text="Adjust to Data boundaries", state=DISABLED)
        self.AdjustData.place(relx=0.17, rely=0.8)

        self.DisplayCurrent = Button(self.top1, text="Display current", state=DISABLED)
        self.DisplayCurrent.place(relx=0.52, rely=0.8)

        self.DeleteAll = Button(self.top1, text="Delete all", state=DISABLED)
        self.DeleteAll.place(relx=0.75, rely=0.8)

        self.Help = Button(self.top1, text="Help", state=DISABLED)
        self.Help.place(relx=0.27, rely=0.9)

        self.Cancel = Button(self.top1, text="Cancel", state=DISABLED)
        self.Cancel.place(relx=0.38, rely=0.9)

        self.AcceptClose = Button(self.top1, text="Accept and Close", state=DISABLED)
        self.AcceptClose.place(relx=0.54, rely=0.9)
        
        
    def editSelectedInterval(self, parent):
        editInterval.EditSelectedInterval(parent)
        
##
##        """ Loop_set_times button """
##        self.LoopSetTimes = Button(self.frame2, text="Loop to Set Times", state=DISABLED)
##        self.LoopSetTimes.place(relx=0.01, rely=0.7)
##
##        """ Delete_all_times Button """
##        self.DelAllTimes = Button(self.frame2, text="Delete all Times", state=DISABLED)
##        self.DelAllTimes.place(relx=0.15, rely=0.7)
##        ########################################################################################
##        
##        """                           Third frame                         """
##        self.frame3 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
##        self.frame3.place(relx=0.05, rely=0.41, relheight=0.27, relwidth=0.9)



 





  
