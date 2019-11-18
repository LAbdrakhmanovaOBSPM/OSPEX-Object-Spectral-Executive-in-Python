
"""

   Application: OSPEX in Python

   Started date: 11/03/2019

   Creators: Liaisian Abdrakhmanova, Abdallah Hamini

   Organization: LESIA, Observatory of Paris, France
  
   Graphical User Interface: GUI was created using tkinter library

   Usage: information to test the program provided in Requirements file

   Status = 'Development'

"""
   
   
   
from tkinter import *
from tkinter.filedialog import askopenfilename
from astropy.io import fits
import re
import copy
import pandas as pd
import plotting
import warnings
import background

class SecondWindow():
   
    """
    Class to create "Select Input Window" menu option in OSPEX

    """
   
    def __init__(self, root):
        self.top1 = Toplevel()
        self.top1.title('SPEX Input Options')
        self.top1.geometry("1000x600")
        Label(self.top1,
              text="Select Input",
              fg="red",
              font="Helvetica 12 bold italic").pack()

        """Initiate the parameters and widgets"""

        self.hdul = None

        self.root = root
        # self.root.wm_atributes("-disabled", True)

        """First frame"""

        self.frame1 = LabelFrame(self.top1, relief=RAISED, borderwidth=1)
        self.frame1.place(relx=0.05, rely=0.04, relheight=0.35, relwidth=0.9)

        self.lblFilename = Label(self.frame1, text="Spectrum or Image File: ")
        self.lblFilename.place(relx=0.01, rely=0.2)

        self.textFilename = Entry(self.frame1, width=20)

        self.textFilename.place(relx=0.2, rely=0.18, relheight=0.16, relwidth=0.57)

        self.browseButton = Button(self.frame1, text='Browse ->', command=self.OpenFile)
        self.browseButton.place(relx=0.8, rely=0.186)

        self.chkBtEntireFile = Checkbutton(self.frame1, text="Entire file", command=self.checked)
        self.chkBtEntireFile.place(relx=0.03, rely=0.37)
        self.chkBtEntireFile.select()

        self.SetFromButton = Button(self.frame1, text="Set from -> ", state=DISABLED)
        self.SetFromButton.place(relx=0.1, rely=0.55)

        self.StartButton = Button(self.frame1, text="Start", state=DISABLED)
        self.StartButton.place(relx=0.24, rely=0.55)

        self.textStart = Entry(self.frame1, width=20)
        self.textStart.place(relx=0.31, rely=0.55, height=33, width=190)
        self.textStart['state'] = 'disabled'

        self.EndButton = Button(self.frame1, text="End", state=DISABLED)
        self.EndButton.place(relx=0.53, rely=0.55)

        self.textEnd = Entry(self.frame1, width=20)
        self.textEnd.place(relx=0.59, rely=0.55, height=33, width=190)
        self.textEnd['state'] = 'disabled'

        self.lblDuration = Label(self.frame1, text="Dur(s): ", state=DISABLED)
        self.lblDuration.place(relx=0.82, rely=0.58)

        self.textDuration = Entry(self.frame1, width=20)
        self.textDuration.place(relx=0.88, rely=0.55, height=33, width=80)
        self.textDuration['state'] = 'disabled'

        self.lblTimeOffset = Label(self.frame1, text="Time Offset(s): ")
        self.lblTimeOffset.place(relx=0.24, rely=0.85)

        self.TimeOffsetList = ("-100.00", "-90.00", "-80.00", "-70.00", "-60.00", "-50.00",
                               "-40.00", "-30.00", "-20.00", "-10.00", "0.00", "10.00", "20.00",
                               "30.00", "40.00", "50.00", "60.00", "70.00", "80.00", "90.00")

        self.SpinboxTimeOffset = Spinbox(self.frame1, values=self.TimeOffsetList, text="Time Offset(s)", )
        self.SpinboxTimeOffset.place(relx=0.37, rely=0.85, width=80)

        # "Summarize" button. If we click on it, it gives the information from self.hdul[1].header
        # It should be a new window with the name "SPEX::PREVIEW"

        self.SummarizeButton = Button(self.frame1, text="Summarize ->", command=self.Summarize)
        self.SummarizeButton.place(relx=0.48, rely=0.81)

        # "Show Header" button. If we click on it, it gives the information from primary_header = hdulist[0].header

        self.ShowHeaderButton = Button(self.frame1, text="Show Header", command=self.ShowHeader)
        self.ShowHeaderButton.place(relx=0.67, rely=0.81)


        """Second frame/Plotting section"""

        self.frame2 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
        self.frame2.place(relx=0.005, rely=0.39, relheight=0.52, relwidth=0.99)

        # Interval Selection Interface
        self.lblIntervalSelection = Label(self.frame2, text="Interval Selection Interface: ")
        self.lblIntervalSelection.place(relx=0.013, rely=0.16)

        # Question: what's the difference between Graphical, Full Options, Show Filter?

        self.chkBtGraphical = Checkbutton(self.frame2, text="Graphical")
        self.chkBtGraphical.place(relx=0.21, rely=0.16)

        self.chkBtFullOptions = Checkbutton(self.frame2, text="Full Options")
        self.chkBtFullOptions.place(relx=0.31, rely=0.16)

        self.chkBtShowFilter = Checkbutton(self.frame2, text="Show Filter")
        self.chkBtShowFilter.place(relx=0.45, rely=0.15)

        # Energy Bands for Time Plots
        self.lblEnergyBands = Label(self.frame2, text="Energy Bands for Time Plots: ")
        self.lblEnergyBands.place(relx=0.013, rely=0.36)

        self.EnergyBands_choices = ('3.à to 6.0', '6.0 to 12.0', '12.0 to 25.0',
                                    '25.0 to 50.0', '50.0 to 100.0', '100.0 to 300.0')
        self.varE = StringVar(self.frame1)
        self.varE.set(self.EnergyBands_choices[0])
        self.selectionE = OptionMenu(self.frame2, self.varE, *self.EnergyBands_choices)
        self.selectionE.place(relx=0.228, rely=0.34)

        self.EChangeButton = Button(self.frame2, text="Change")
        self.EChangeButton.place(relx=0.36, rely=0.34)

        self.ShowEbandsButton = Button(self.frame2, text="Show Ebands")
        self.ShowEbandsButton.place(relx=0.46, rely=0.34)

        self.SetToDefaultButton = Button(self.frame2, text="Set to default")
        self.SetToDefaultButton.place(relx=0.6, rely=0.34)

        # Time Bands for Energy Plots
        self.lblTimeBands = Label(self.frame2, text="Time Bands for Energy Plots: ")
        self.lblTimeBands.place(relx=0.013, rely=0.55)

        self.TimeBands_choices = ('1s time interval', '2nd time interval', '3rd time interval', '4th time interval')
        self.varT = StringVar(self.frame2)
        self.varT.set(self.TimeBands_choices[0])
        self.selectionT = OptionMenu(self.frame2, self.varT, *self.TimeBands_choices)
        self.selectionT.place(relx=0.228, rely=0.53, width = 320)

        self.TChangeButton = Button(self.frame2, text="Change")
        self.TChangeButton.place(relx=0.58, rely=0.53)

        self.ShowTbandsButton = Button(self.frame2, text="Show Tbands")
        self.ShowTbandsButton.place(relx=0.69, rely=0.53)

        # Plot Units. Plotting for Rate, Counts and Flux
        self.lblPlotUnits = Label(self.frame2, text="Plot Units: ")
        self.lblPlotUnits.place(relx=0.013, rely=0.75)

        # Option menu for Rate, Counts, Flux
        self.Component_choices = ('Rate', 'Counts', 'Flux')
        self.var = StringVar(self.frame1)
        self.var.set(self.Component_choices[0])
        self.selection = OptionMenu(self.frame2, self.var, *self.Component_choices)
        self.selection.place(relx=0.11, rely=0.73)

        self.PlotSpectrumButton = Button(self.frame2, text="Plot Spectrum", command=lambda: self.show_plot("spec"))
        self.PlotSpectrumButton.place(relx=0.21, rely=0.73)

        self.PlotTimeProfileButton = Button(self.frame2, text="Plot Time Profile",
                                            command=lambda: self.show_plot("time"))
        self.PlotTimeProfileButton.place(relx=0.357, rely=0.73)

        self.PlotSpectrogramButton = Button(self.frame2, text="Plot Spectrogram",
                                            command=lambda: self.show_plot("specgr"))
        self.PlotSpectrogramButton.place(relx=0.52, rely=0.73)

        # The buttons at the bottom of the "Select Input" window

        self.refreshButton = Button(self.top1, text="Refresh")
        self.refreshButton.place(relx=0.4, rely=0.925)
        
        self.closeButton = Button(self.top1, text="Close", command=self.destroy)
        self.closeButton.place(relx=0.5, rely=0.925)



    """Main methods"""

    def OpenFile(self):
        self.name = askopenfilename(initialdir=("."),
                                    filetypes=(("FITS files", "*.fits"), ("All Files", "*.*")),
                                    title="Please Select Spectrum or Image File")
        self.textFilename.delete(0, 'end')
        background.BackgroundWindow.fname=self.name
        try:
            with fits.open(self.name) as hdul:
                self.hdul = hdul
                self.timeData = [self.hdul[3].header[17], self.hdul[3].header[18], self.hdul[1].data.TIMEDEL]
                self.summarizeData = [self.hdul[1].header[24], str(self.hdul[1].header[25])[10:],
                                      self.hdul[1].header[15],
                                      self.hdul[1].data.TIME, self.hdul[2].data.E_MIN,
                                      self.hdul[2].data.E_MIN[0], self.hdul[2].data.E_MAX[-1]]
                self.plotData = [self.hdul[1].data.RATE, self.hdul[1].data.TIME, self.hdul[1].data.LIVETIME,
                                 self.hdul[1].data.CHANNEL]
                self.time_len = len(self.summarizeData[3])
                self.TimeNew = pd.to_datetime(self.plotData[1], unit='s')
                self.TimeNew2 = self.plotData[1] - 2

                self.textFilename.insert(0, self.name)
        except:
            self.textFilename.insert(0, "No file exists")

    # def Summarize

    def Summarize(self):
        top = Toplevel()
        top.title('SPEX::PREVIEW')
        top.geometry("400x300")
        frameSummarize = LabelFrame(top, relief=RAISED, borderwidth=2)
        frameSummarize.pack(side=TOP, expand=True)

        # textSummarize = ['Spectrum or Image File Summary: ', 'Data Type: ', 'Time Bins:', 'Time range:', '#Energy Bins: ',
        # 'Area: ', 'Detectors Used: ', 'Response Info: ']

        txt = ["\n\n\nSpectrum or Image File Summary",
               "\nData Type: ", self.summarizeData[2],
               "\nFile name: ", self.name,
               "\n#Time Bins: ", self.time_len, "Time range: ", self.timeData[0], 'to', self.timeData[1],
               "\n#Energy Bins: ", len(self.summarizeData[4]),
               "Energy range: ", self.summarizeData[5], 'to', self.summarizeData[6],
               "\nArea: ", self.summarizeData[0],
               "\nDetectors Used: ", self.summarizeData[1],
               "\nResponse Info: ", self.name]
        list = Text(frameSummarize)
        list.insert(END, txt)
        list.pack()

    # def ShowHeader
    # Can read the information and display it
    # Text should be well-organized in the window 'SPEX::FITSHEADER'
    def ShowHeader(self):
        text = re.sub(" +", " ", self.hdul[0].header.tostring())
        top = Toplevel()
        top.title('SPEX::FITSHEADER')
        top.geometry("500x600")
        scrollbar1 = Scrollbar(top)
        scrollbar1.pack(side=RIGHT, fill=Y)
        header = Text(top, width=450, height=450)
        header.insert(END, (text).splitlines())
        header.config(state=DISABLED)
        header.pack()
        scrollbar1.config(command=header.yview)

    def destroy(self):
        # self.root.wm_attributes("-disabled", False)
        self.top1.destroy()

    def checked(self):
        if self.SetFromButton['state'] == 'disabled':
            self.SetFromButton['state'] = 'normal'
            self.StartButton['state'] = 'normal'
            self.EndButton['state'] = 'normal'

            self.textStart['state'] = 'normal'
            self.textEnd['state'] = 'normal'
            self.textDuration['state'] = 'normal'
            self.lblDuration['state'] = 'normal'

            self.textStart.delete(0, 'end')
            self.textEnd.delete(0, 'end')
            self.textDuration.delete(0, 'end')

            self.textStart.insert(0, self.timeData[0])
            self.textEnd.insert(0, self.timeData[1])
            self.textDuration.insert(0, sum(self.timeData[2]))

        else:
            self.SetFromButton['state'] = 'disabled'
            self.StartButton['state'] = 'disabled'
            self.EndButton['state'] = 'disabled'

            self.textStart['state'] = 'disabled'
            self.textEnd['state'] = 'disabled'
            self.textDuration['state'] = 'disabled'
            self.lblDuration['state'] = 'disabled'

    # ------------PLOTTING------------------------------

    def show_plot(self, e):
        plots = plotting.Input(self.name)
        if self.var.get() == 'Rate':
            if e == 'spec':
                plots.plot_spectrum_rate()
            elif e == 'time':
                plots.rate_vs_time_plotting()
            elif e == 'specgr':
                plots.plot_spectrogram_rate()
        if self.var.get() == 'Counts':
            if e == 'spec':
                plots.plot_spectrum_counts()
            elif e == 'time':
                plots.counts_vs_time_plotting()
            elif e == 'specgr':
                plots.plot_spectrogram_counts()
        if self.var.get() == 'Flux':
            if e == 'spec':
                plots.plot_spectrum_flux()
            elif e == 'time':
                plots.flux_vs_time_plotting()
            elif e == 'specgr':
                plots.plot_spectrogram_flux()
