
"""
        Application: Background in OSPEX with Python
        
        Started date: 11/10/2019
        
        Creators: Aichatou Aboubacar, LIAISIAN Abdrakhmanova, Abdallah Hamini
        
        Organization: LESIA, Observatory of Paris, France
"""



from tkinter import *
from astropy.io import fits
import re
import pandas as pd
import plotting
import background_plot
import warnings
import second


class BackgroundWindow():
    """Class to create a Select Input Window"""
    fname=None
    def __init__(self, root):
        self.top1 = Toplevel()
        self.top1.title('SPEX Background Options')
        self.top1.geometry("1000x600")
        Label(self.top1,
              text="Select Background",
              fg="black",
              font="Helvetica 12 bold italic").pack()

        """Initiate the parameters and widgets"""

        self.hdul = None

        self.root = root
        #self.sepBkVar = BooleanVar()
        self.sepBkVar = IntVar()
        #self.sepBkVar.set(1)
        # self.root.wm_atributes("-disabled", True)

        #########################################################################################
        """                         First frame                                     """

        self.frame1 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
        self.frame1.place(relx=0.05, rely=0.04, relheight=0.1, relwidth=0.9)
        #self.frame1.pack(fill='x', side=TOP)

        #self.frame1.pack(side=TOP)
        self.lblFilename = Label(self.frame1, text="Interval Selection: ")
        self.lblFilename.place(relx=0.01, rely=0.2)
        #self.lblFilename.pack(side=LEFT)

        self.chkBtGraphical = Checkbutton(self.frame1, text="Graphical", variable='Graphical')
        self.chkBtGraphical.place(relx=0.15, rely=0.2)
        #self.chkBtGraphical.pack(side=LEFT)

        self.chkBtFullOptions = Checkbutton(self.frame1, text="Full Options", variable='FullOpt')
        self.chkBtFullOptions.place(relx=0.25, rely=0.2)
        #self.chkBtFullOptions.pack(side=LEFT)
    
        self.Component_choices = ('Rate', 'Counts', 'Flux')
        self.var = StringVar(self.frame1)
        self.var.set(self.Component_choices[2])
        self.selection = OptionMenu(self.frame1, self.var, *self.Component_choices)
        self.selection.place(relx=0.46, rely=0.18)
        #self.selection.pack(side=LEFT)

        self.lblPlotUnits = Label(self.frame1, text="Plot Units: ")
        #self.lblPlotUnits.pack(side=LEFT)
        self.lblPlotUnits.place(relx=0.37, rely=0.18)

        #################################################################################
        """                          Second frame                             """
        self.frame2 = Frame(self.top1, relief=RAISED, borderwidth=2)
        self.frame2.place(relx=0.05, rely=0.14, relheight=0.27, relwidth=0.9)
        #self.frame2.pack(fill='x')

        self.SeparateBk = Checkbutton(self.frame2, text="Separate BK for each energy band",
        variable=self.sepBkVar, command=self.onClikSeparateBk, state=NORMAL) #command=self.onClikSeparateBk, onvalue = True, offvalue = False,
        self.SeparateBk.place(relx=0.01, rely=0.04)
        #self.SeparateBk.pack(side=TOP)
        #self.SeparateBk.bind("<Button-1>", self.onClikSeparateBk)

        self.AllBands_choices = ('Set all bands to', '0Poly', '1Poly', '2Poly', '3Poly', 'Exp', 'High E Profile', 'This E Profile')
        self.AllBandsVar = StringVar(self.frame2)
        self.AllBandsVar.set(self.AllBands_choices[0])
        self.AllBandsSelection = OptionMenu(self.frame2, self.AllBandsVar, *self.AllBands_choices)
        self.AllBandsSelection.place(relx=0.26, rely=0.04)
        self.AllBandsSelection.config(state="disabled")

        """ half smoothing """
        self.HalfSmooth = Label(self.frame2, text="Profile Half Smoothing width(#pts):")
        self.HalfSmooth.place(relx=0.41, rely=0.05)

        self.HalfSmoothList = ("0","1","4","8","16","32","64","128","256")

        self.SpinboxHalfSmooth = Spinbox(self.frame2, values=self.HalfSmoothList )
        self.SpinboxHalfSmooth.place(relx=0.63, rely=0.05, width=50)

        """ show profile """
        self.ShowProfile = Checkbutton(self.frame2, text="Show Profile", variable='ShowProf')
        self.ShowProfile.place(relx=0.7, rely=0.04)

        """ Current Energy Bands """
        self.lblCurrentEnergy = Label(self.frame2, text="Current Energy Bands:")
        self.lblCurrentEnergy.place(relx=0.01, rely=0.4)

        self.CurrentEnergy_choices = ('3.0 to 6.0', '6.0 to 12.0', '12.0 to 25.0', '25.0 to 50.0', '50.0 to 100.0', '100.0 to 300.0')
        self.CurrentEnergyVar = StringVar(self.frame2)
        self.CurrentEnergyVar.set(self.CurrentEnergy_choices[0])
        self.CurrentEnergySelection = OptionMenu(self.frame2, self.CurrentEnergyVar, *self.CurrentEnergy_choices)
        self.CurrentEnergySelection.place(relx=0.15, rely=0.4)
        self.CurrentEnergySelection.config(state="disabled")

        """ Bands 0 """
        self.Bands0 = Label(self.frame2, text="#Bands:0")
        self.Bands0.place(relx=0.3, rely=0.4)

        """ Change Energy Band Button """
        self.ChangeEnergBand = Button(self.frame2, text="Change", state=DISABLED)
        self.ChangeEnergBand.place(relx=0.38, rely=0.4)

        """ set_to_spex_eband Button """
        self.SetSpex = Button(self.frame2, text="Set to spex_eband", state=DISABLED)
        self.SetSpex.place(relx=0.45, rely=0.4)

        """ show Button """
        self.ShowFluxEnerg = Button(self.frame2, text="Show", state=DISABLED)
        self.ShowFluxEnerg.place(relx=0.58, rely=0.4)

        """ Loop_set_times button """
        self.LoopSetTimes = Button(self.frame2, text="Loop to Set Times", state=DISABLED)
        self.LoopSetTimes.place(relx=0.01, rely=0.7)

        """ Delete_all_times Button """
        self.DelAllTimes = Button(self.frame2, text="Delete all Times", state=DISABLED)
        self.DelAllTimes.place(relx=0.15, rely=0.7)
        ########################################################################################
        
        """                           Third frame                         """
        self.frame3 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
        self.frame3.place(relx=0.05, rely=0.41, relheight=0.27, relwidth=0.9)

        #self.frame3b = LabelFrame(self.top1, relief=RAISED, borderwidth=2)

        ########################################################################################
        """                           Fourth frame                        """
        self.frame4 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
        self.frame4.place(relx=0.05, rely=0.68, relheight=0.08, relwidth=0.9)

        self.SpexBands = Label(self.frame4, text="Time Profile in spex_ebands:")
        self.SpexBands.place(relx=0.01, rely=0.04)

        self.Data = Checkbutton(self.frame4, text="Data", variable='Data')
        self.Data.place(relx=0.22, rely=0.04)

        self.Background = Checkbutton(self.frame4, text="Background", variable='Background')
        self.Background.place(relx=0.29, rely=0.04)

        self.DataBackground = Checkbutton(self.frame4, text="Data-Background", variable='DataBack')
        self.DataBackground.place(relx=0.4, rely=0.04)

        self.Error = Checkbutton(self.frame4, text="Error", variable='Error')
        self.Error.place(relx=0.54, rely=0.04)

        self.Plot = Button(self.frame4, text="Plot")
        self.Plot.place(relx=0.63, rely=0.04)

        self.Refresh = Button(self.top1, text="Refresh")
        self.Refresh.place(relx=0.45, rely=0.8)

        self.Close = Button(self.top1, text="Close")
        self.Close.place(relx=0.54, rely=0.8)

        """ Scrollbar """
        self.vscrollbar = Scrollbar(self.frame3, orient="vertical")
        #self.vscrollbar.pack(side='right', fill="y")

        self.hscrollbar = Scrollbar(self.frame3, orient="horizontal")
        #self.hscrollbar.pack(side='bottom', fill="x")
        #self.hscrollbar.place(relx=0.1, rely=0.3)
        #################################################################################################

        """                                  Canvas                                    """
        self.backCanv = Canvas(self.frame3, bd=2, width=850, bg="#FFFFFF", height=120) #, background='#FFFFFF'
        #self.backCanv.pack(fill='x')
        self.vscrollbar.config(command=self.backCanv.yview)
        self.hscrollbar.config(command=self.backCanv.xview)
        self.backCanv.config(yscrollcommand=self.vscrollbar.set)
        self.backCanv.config(xscrollcommand=self.hscrollbar.set)
        self.backCanv.config(scrollregion = (0,0,700,700))
        self.backCanv.place(relx=0.01, rely=0.1)
        
        #self.SeparateBk.config(command=self.backCanv.config(state="normal"))
  
        #self.backCanv.delete(ALL)
        self.notSeparateCanva()

##############################################      Functions          ####################################################################


    def notSeparateCanva(self):
        
        self.frame0 = Frame(self.backCanv, relief=RAISED, borderwidth=2, width=800, height=90)

        self.backCanv.create_window(400, 70,  window=self.frame0, width=800, height=90)
        
        self.AllEnerg = Label(self.frame0, text="For all Energies: ")
        self.AllEnerg.place(relx=0.01, rely=0.12)

        self.BkTimes = Label(self.frame0, text="Bk Times:")
        self.BkTimes.place(relx=0.15, rely=0.12)

##        self.BkT_choices = ('None', ' ')
##        self.BkTVar = StringVar(self.frame0)
##        self.BkTVar.set(self.BkT_choices[0])
##        self.BkTSelection = OptionMenu(self.frame3, self.BkTVar, *self.BkT_choices)
        self.BkTSelection = Button(self.frame0, text="None")
        self.BkTSelection.place(relx=0.24, rely=0.15)


        self.Times = Label(self.frame0, text="#Times: 0 ")
        self.Times.place(relx=0.62, rely=0.12)

        self.Method = Label(self.frame0, text="Method:")
        self.Method.place(relx=0.7, rely=0.12)

        self.Method_choices = ('0Poly', '1Poly', '2Poly', '3Poly', 'Exp', 'High E Profile', 'This E Profile')
        self.MethodVar = StringVar(self.frame0)
        self.MethodVar.set(self.Method_choices[0])
        self.MethodSelection = OptionMenu(self.frame0, self.MethodVar, *self.Method_choices)
        self.MethodSelection.place(relx=0.76, rely=0.09)

        self.BkTimeInterv = Label(self.frame0, text="Bk Time Intervals: ")
        self.BkTimeInterv.place(relx=0.01, rely=0.55)

        self.Delete = Button(self.frame0, text="Delete")
        self.Delete.place(relx=0.15, rely=0.55)

        self.Change = Button(self.frame0, text="Change")
        self.Change.place(relx=0.22, rely=0.55)

        self.Show = Button(self.frame0, text="Show", command=lambda: self.show_backgroundplot("show", 6))
        self.Show.place(relx=0.29, rely=0.55)

        self.PlotSpectr = Button(self.frame0, text="Plot Spectrum")
        self.PlotSpectr.place(relx=0.36, rely=0.55)

        self.PlotVsTim = Button(self.frame0, text="Plot vs Time", command=lambda: self.show_backgroundplot("time", 6))
        self.PlotVsTim.place(relx=0.48, rely=0.55)

        self.Error2 = Checkbutton(self.frame0, text="Error", variable='Error2')
        self.Error2.place(relx=0.58, rely=0.55)

##        self.frame1 = Frame(self.backCanv, relief=RAISED, borderwidth=2, width=800, height=110)     
##        self.backCanv.create_window(400, 170,  window=self.frame1, width=800, height=90)
##
##        self.frame2 = Frame(self.backCanv, relief=RAISED, borderwidth=2, width=800, height=110)     
##        self.backCanv.create_window(400, 270,  window=self.frame2, width=800, height=90)
##        self.BkTime = Label(self.frame2, text="Bk Times:")
##        self.BkTime.place(relx=0.15, rely=0.12)
##
##        self.frame3 = Frame(self.backCanv, relief=RAISED, borderwidth=2, width=800, height=110)     
##        self.backCanv.create_window(400, 370,  window=self.frame3, width=800, height=90)
##
##        self.frame4 = Frame(self.backCanv, relief=RAISED, borderwidth=2, width=800, height=110)     
##        self.backCanv.create_window(400, 470,  window=self.frame4, width=800, height=90)

    def energBandCanvList(self, i, x, y, energyLabel):

          fr = 'frame'+str(i)
          v0 = 'AllEnerg' + str(i)
          v1 = 'BkTimes' + str(i)
          v2 = 'BkTSelection' + str(i)
        
          #frameName = self.fr
          self.fr= Frame(self.backCanv, relief=RAISED, borderwidth=2, width=800, height=110)
          self.backCanv.create_window(x, y,  window=self.fr, width=800, height=90)
  

##        v3 = 'Times' + i
##        v4 = 'Method' + i
##        v5 = 'MethodSelection' + i
##        v6 = 'BkTimeInterv' + i
##        v7 = 'Delete' + i
##        v8 = 'Change' + i
##        v9 = 'Show' + i
##        v10 = 'PlotSpectr' + i
##        v11 = 'PlotVsTim' + i
##        v12 = 'Error2' + i
        
##          self.v0 = Label(self.fr, text=energyLabel)
##          self.v0.place(relx=0.01, rely=0.12)
##
##          self.v1 = Label(self.fr, text="Bk Times:")
##          self.v1.place(relx=0.15, rely=0.12)
## 
##          self.v2 = Button(self.fr, text="None")
##          self.v2.place(relx=0.24, rely=0.15)
##          print('selffff', self.v0, self.fr)

          self.AllEnerg = Label(self.fr, text=energyLabel)
          self.AllEnerg.place(relx=0.01, rely=0.12)

          self.BkTimes = Label(self.fr, text="Bk Times:")
          self.BkTimes.place(relx=0.15, rely=0.12)

          self.BkTSelection = Button(self.fr, text="None")
          self.BkTSelection.place(relx=0.24, rely=0.15)
        
          self.Times = Label(self.fr, text="#Times: 0 ")
          self.Times.place(relx=0.62, rely=0.12)

          self.Method = Label(self.fr, text="Method:")
          self.Method.place(relx=0.7, rely=0.12)

          self.Method_choices = ('0Poly', '1Poly', '2Poly', '3Poly', 'Exp', 'High E Profile', 'This E Profile')
          self.MethodVar = StringVar(self.fr)
          self.MethodVar.set(self.Method_choices[0])
          self.MethodSelection = OptionMenu(self.fr, self.MethodVar, *self.Method_choices)
          self.MethodSelection.place(relx=0.76, rely=0.09)

          self.BkTimeInterv = Label(self.fr, text="Bk Time Intervals: ")
          self.BkTimeInterv.place(relx=0.01, rely=0.55)

          self.Delete = Button(self.fr, text="Delete")
          self.Delete.place(relx=0.15, rely=0.55)

          self.Change = Button(self.fr, text="Change")
          self.Change.place(relx=0.22, rely=0.55)

          self.Show = Button(self.fr, text="Show", command=lambda: self.show_backgroundplot("show", i))
          self.Show.place(relx=0.29, rely=0.55)

          self.PlotSpectr = Button(self.fr, text="Plot Spectrum")
          self.PlotSpectr.place(relx=0.36, rely=0.55)

          self.PlotVsTim = Button(self.fr, text="Plot vs Time", command=lambda: self.show_backgroundplot("time", i))
          self.PlotVsTim.place(relx=0.48, rely=0.55)

          self.Error2 = Checkbutton(self.fr, text="Error", variable='Error2')
          self.Error2.place(relx=0.58, rely=0.55)

    def onClikSeparateBk(self):
         print('separa', self.sepBkVar.get())
         energyLab = ['3.0 to 6.0 keV', '6.0 to 12.0 keV', '12.0 to 25.0 keV', '25.0 to 50.0 keV',
                      '50.0 to 100.0 keV', '100.0 to 300.0 keV' ]
         if self.sepBkVar.get() == 1:
            if BackgroundWindow.fname is not None:
               #self.backCanv.place_forget()
               self.backCanv.delete(ALL)
               for j in range(6):
                 #print('jjjjj', j)
                 self.energBandCanvList(j, 400, 70 + 100*j, energyLab[j])
                     
            else:
               self.backCanv.delete(ALL)
   
            
            self.ChangeEnergBand.config(state="normal")
            self.SetSpex.config(state="normal")
            self.ShowFluxEnerg.config(state="normal")
            self.LoopSetTimes.config(state="normal")
            self.DelAllTimes.config(state="normal")
            self.CurrentEnergySelection.config(state="normal")
            self.AllBandsSelection.config(state="normal")
         else:
            #self.backCanv.place()
            self.backCanv.delete(ALL)
            self.notSeparateCanva()
            #self.backCanv.place(relx=0.01, rely=0.1)
            
            self.ChangeEnergBand.config(state="disabled")
            self.SetSpex.config(state="disabled")
            self.ShowFluxEnerg.config(state="disabled")
            self.LoopSetTimes.config(state="disabled")
            self.DelAllTimes.config(state="disabled")
            self.CurrentEnergySelection.config(state="disabled")
            self.AllBandsSelection.config(state="disabled")

         print('plt', BackgroundWindow.fname)

##    def plotAll(self):
##      sec = second.SecondWindow(self.root)
##      plt = sec.OpenFile()
##      print('plt', plt)


    def show_backgroundplot(self, e, i):

            
         if self.sepBkVar.get() == 1:
          if BackgroundWindow.fname is not None:          
           plots = background_plot.Input(BackgroundWindow.fname)
           if self.var.get() == 'Rate':
            if e == 'time':
                #plots.rate_vs_time_plotting()
                plots.backg_plot_vs_time('rate', i)
##            elif e == 'show':
##                plots.rate_vs_time_plotting()
##            elif e == 'specgr':
##                plots.plot_spectrogram_rate()
           if self.var.get() == 'Counts':
            if e == 'time':
               plots.backg_plot_vs_time('counts', i)
##          elif e == 'show':
##             plots.rate_vs_time_plotting()
##          elif e == 'specgr':
##               plots.plot_spectrogram_rate()
           if self.var.get() == 'Flux':
            if e == 'time':
                plots.backg_plot_vs_time('flux', i)
##            elif e == 'show':
##                plots.flux_vs_time_plotting()
##            elif e == 'specgr':
##                plots.plot_spectrogram_flux()

##                
         else:
           plots = plotting.Input(BackgroundWindow.fname)
          
           if self.var.get() == 'Rate':
            if e == 'time':
                plots.rate_vs_time_plotting()
##            elif e == 'show':
##                plots.rate_vs_time_plotting()
##            elif e == 'specgr':
##                plots.plot_spectrogram_rate()
           if self.var.get() == 'Counts':
            if e == 'time':
               plots.counts_vs_time_plotting()
##          elif e == 'show':
##             plots.rate_vs_time_plotting()
##          elif e == 'specgr':
##               plots.plot_spectrogram_rate()
           if self.var.get() == 'Flux':
            if e == 'time':
                plots.flux_vs_time_plotting()
##            elif e == 'show':
##                plots.flux_vs_time_plotting()
##            elif e == 'specgr':
##                plots.plot_spectrogram_flux()
        
            
##


 

###################################################################################################################
##        """Fourth frame """
##        self.frame4 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
##        self.frame4.place(relx=0.05, rely=0.26, relheight=0.1, relwidth=0.9)
##
##        
##        self.textFilename = Entry(self.frame1, width=20)
##
##        self.textFilename.place(relx=0.2, rely=0.18, relheight=0.16, relwidth=0.57)
##
##        self.browseButton = Button(self.20.186)
##
##        self.chkBtEntireFile = Checkbutton(self.frame1, text="Entire file", command=self.checked)
##        self.chkBtEntireFile.place(relx=0.03, rely=0.37)
##        self.chkBtEntireFile.select()
##
##        self.SetFromButton = Button(self.frame1, text="Set from -> ", state=DISABLED)
##        self.SetFromButton.place(relx=0.1, rely=0.55)
##
##        self.StartButton = Button(self.frame1, text="Start", state=DISABLED)
##        self.StartButton.place(relx=0.24, rely=0.55)
##
##        self.textStart = Entry(self.frame1, width=20)
##        self.textStart.place(relx=0.31, rely=0.55, height=33, width=190)
##        self.textStart['state'] = 'disabled'
##
##        self.EndButton = Button(self.frame1, text="End", state=DISABLED)
##        self.EndButton.place(relx=0.53, rely=0.55)
##
##        self.textEnd = Entry(self.frame1, width=20)
##        self.textEnd.place(relx=0.59, rely=0.55, height=33, width=190)
##        self.textEnd['state'] = 'disabled'
##
##        self.lblDuration = Label(self.frame1, text="Dur(s): ", state=DISABLED)
##        self.lblDuration.place(relx=0.82, rely=0.58)
##
##        self.textDuration = Entry(self.frame1, width=20)
##        self.textDuration.place(relx=0.88, rely=0.55, height=33, width=80)
##        self.textDuration['state'] = 'disabled'
##
##        self.lblTimeOffset = Label(self.frame1, text="Time Offset(s): ")
##        self.lblTimeOffset.place(relx=0.24, rely=0.85)
##
##        self.TimeOffsetList = ("-100.00", "-90.00", "-80.00", "-70.00", "-60.00", "-50.00",
##                               "-40.00", "-30.00", "-20.00", "-10.00", "0.00", "10.00", "20.00",
##                               "30.00", "40.00", "50.00", "60.00", "70.00", "80.00", "90.00")
##
##        self.SpinboxTimeOffset = Spinbox(self.frame1, values=self.TimeOffsetList, text="Time Offset(s)", )
##        self.SpinboxTimeOffset.place(relx=0.37, rely=0.85, width=80)
##
##        # "Summarize" button. If we click on it, it gives the information from self.hdul[1].header
##        # It should be a new window with the name "SPEX::PREVIEW"
##
##        self.SummarizeButton = Button(self.frame1, text="Summarize ->", command=self.Summarize)
##        self.SummarizeButton.place(relx=0.48, rely=0.81)
##
##        # "Show Header" button. If we click on it, it gives the information from primary_header = hdulist[0].header
##
##        self.ShowHeaderButton = Button(self.frame1, text="Show Header", command=self.ShowHeader)
##        self.ShowHeaderButton.place(relx=0.67, rely=0.81)






  
