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
##
##        #################################################################################
##        """                          Second frame                             """
##        self.frame2 = Frame(self.top1, relief=RAISED, borderwidth=2)
##        self.frame2.place(relx=0.05, rely=0.14, relheight=0.27, relwidth=0.9)
##        #self.frame2.pack(fill='x')
##
##        self.SeparateBk = Checkbutton(self.frame2, text="Separate BK for each energy band",
##        variable=self.sepBkVar, command=self.onClikSeparateBk, state=NORMAL) #command=self.onClikSeparateBk, onvalue = True, offvalue = False,
##        self.SeparateBk.place(relx=0.01, rely=0.04)
##        #self.SeparateBk.pack(side=TOP)
##        #self.SeparateBk.bind("<Button-1>", self.onClikSeparateBk)
##
##        self.AllBands_choices = ('Set all bands to', '0Poly', '1Poly', '2Poly', '3Poly', 'Exp', 'High E Profile', 'This E Profile')
##        self.AllBandsVar = StringVar(self.frame2)
##        self.AllBandsVar.set(self.AllBands_choices[0])
##        self.AllBandsSelection = OptionMenu(self.frame2, self.AllBandsVar, *self.AllBands_choices)
##        self.AllBandsSelection.place(relx=0.26, rely=0.04)
##        self.AllBandsSelection.config(state="disabled")
##
##        """ half smoothing """
##        self.HalfSmooth = Label(self.frame2, text="Profile Half Smoothing width(#pts):")
##        self.HalfSmooth.place(relx=0.41, rely=0.05)
##
##        self.HalfSmoothList = ("0","1","4","8","16","32","64","128","256")
##
##        self.SpinboxHalfSmooth = Spinbox(self.frame2, values=self.HalfSmoothList )
##        self.SpinboxHalfSmooth.place(relx=0.63, rely=0.05, width=50)
##
##        """ show profile """
##        self.ShowProfile = Checkbutton(self.frame2, text="Show Profile", variable='ShowProf')
##        self.ShowProfile.place(relx=0.7, rely=0.04)
##
##        """ Current Energy Bands """
##        self.lblCurrentEnergy = Label(self.frame2, text="Current Energy Bands:")
##        self.lblCurrentEnergy.place(relx=0.01, rely=0.4)
##
##        self.CurrentEnergy_choices = ('3.0 to 6.0', '6.0 to 12.0', '12.0 to 25.0', '25.0 to 50.0', '50.0 to 100.0', '100.0 to 300.0')
##        self.CurrentEnergyVar = StringVar(self.frame2)
##        self.CurrentEnergyVar.set(self.CurrentEnergy_choices[0])
##        self.CurrentEnergySelection = OptionMenu(self.frame2, self.CurrentEnergyVar, *self.CurrentEnergy_choices)
##        self.CurrentEnergySelection.place(relx=0.15, rely=0.4)
##        self.CurrentEnergySelection.config(state="disabled")
##
##        """ Bands 0 """
##        self.Bands0 = Label(self.frame2, text="#Bands:0")
##        self.Bands0.place(relx=0.3, rely=0.4)
##
##        """ Change Energy Band Button """
##        self.ChangeEnergBand = Button(self.frame2, text="Change", state=DISABLED)
##        self.ChangeEnergBand.place(relx=0.38, rely=0.4)
##
##        """ set_to_spex_eband Button """
##        self.SetSpex = Button(self.frame2, text="Set to spex_eband", state=DISABLED)
##        self.SetSpex.place(relx=0.45, rely=0.4)
##
##        """ show Button """
##        self.ShowFluxEnerg = Button(self.frame2, text="Show", state=DISABLED)
##        self.ShowFluxEnerg.place(relx=0.58, rely=0.4)
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



 





  
