from tkinter import *
from astropy.io import fits
import re
import pandas as pd
import plotting
import background_plot
import warnings
import second
import editInterval


class EditTimeWindow():
    """Class to create a Select Time Window"""
    bkgTimeInterv = None
    defaultTime = None
  
    def __init__(self, energyBin):
        self.top1 = Toplevel()
        self.top1.title('Select Time Intervals for Background')
        self.top1.geometry("480x500")
        Label(self.top1,
              text="Select Time Intervals for Background",
              fg="black",
              font="Helvetica 8").pack()
        Label(self.top1,
              text="for Energy Band " + str(energyBin),
              fg="black",
              font="Helvetica 8").pack()
        Label(self.top1,
              text="Left/right click to define start/end of intervals",
              fg="black",
              font="Helvetica 8").pack()
        Label(self.top1,
              text="Left double click on a plotted interval for editing options",
              fg="black",
              font="Helvetica 8").pack()




        #########################################################################################
##        """                         First frame                                     """
##
        self.frame1 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
        self.frame1.place(relx=0.05, rely=0.17, relheight=0.25, relwidth=0.9)

        """ Current Intervals"""
        self.lblCurrentIntervals = Label(self.frame1, text="Current Intervals:")
        self.lblCurrentIntervals.place(relx=0.01, rely=0.25)


        timeInterv =  str(EditTimeWindow.bkgTimeInterv) if EditTimeWindow.bkgTimeInterv is not None else str(energyBin)
        print('time intervallllllllllll', timeInterv)
        EditTimeWindow.defaultTime = StringVar()
        EditTimeWindow.defaultTime.set(timeInterv)        
        self.CurrentInterval = Button(self.frame1,  textvariable = EditTimeWindow.defaultTime)
        self.CurrentInterval.place(relx=0.28, rely=0.25)

        self.lblIntervals = Label(self.frame1, text="#Intervals = 1")
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

        self.AdjustData = Button(self.top1, text="Adjust to Data boundaries")
        self.AdjustData.place(relx=0.17, rely=0.8)

        self.DisplayCurrent = Button(self.top1, text="Display current")
        self.DisplayCurrent.place(relx=0.52, rely=0.8)

        self.DeleteAll = Button(self.top1, text="Delete all")
        self.DeleteAll.place(relx=0.75, rely=0.8)

        self.Help = Button(self.top1, text="Help")
        self.Help.place(relx=0.27, rely=0.9)

        self.Cancel = Button(self.top1, text="Cancel")
        self.Cancel.place(relx=0.38, rely=0.9)

        self.AcceptClose = Button(self.top1, text="Accept and Close", command=self.quit)
        self.AcceptClose.place(relx=0.54, rely=0.9)

    def quit(self):
        self.top1.destroy()
        
        
    def editSelectedInterval(self, parent):
        editInterval.EditSelectedInterval(parent)
        




 





  
