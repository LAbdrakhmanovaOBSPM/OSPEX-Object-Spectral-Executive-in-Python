
"""

  Application: OSPEX in Python

  Started date: 11/03/2019

  Creators: Liaisian Abdrakhmanova, Abdallah Hamini

  Organization: LESIA, Observatory of Paris, France
  
  Graphical User Interface: GUI was created using tkinter library

  Usage: information to test the program provided in Requirements file

  Status = 'Development'

"""
  
  
  
import webbrowser
from tkinter import *
from tkinter import messagebox
import importlib
import second
import background


def clickedContact():
    messagebox.showinfo('OSPEX Contact Information', 'The OSPEX package was developed by Abdallah Hamini and Liaisian Abdrakhmanova'
                                                     '\nat LESIA, Observatory of Paris, France'
                                                     '\n\n@:Abdallah.Hamini@obspm.fr'
                                                     '\n@:Liaisian.Abdrakhmanova@obspm.fr'
                                                     '\n\n№:(+33)145077470')


def clickedHelp_on_Help():
    messagebox.showinfo('OSPEX Help Information', 'The documentation for OSPEX is in HTML format.'
                                                  '\n\nWhen you click the help buttons, your preferred browser will be activated.'
                                                  '\n\nThe browser may start in iconized mode.'
                                                  '\nIf it does not appear, you may need to find it on the taskbar.')


def clickedOSPEX_ORR():
    messagebox.showinfo('OSPEX Object Reference Retrieval',
                        'Will be filled in the future')


new = 1


def WhatsNew():
    url1 = "https://hesperia.gsfc.nasa.gov/ssw/packages/spex/doc/ospex_whatsnew.htm"
    webbrowser.open(url1, new=new)


def OSPEX_Guide():
    url2 = "https://hesperia.gsfc.nasa.gov/ssw/packages/spex/doc/ospex_explanation.htm"
    webbrowser.open(url2, new=new)


def OSPEX_Parameter_Tables():
    url3 = "https://hesperia.gsfc.nasa.gov/ssw/packages/spex/doc/ospex_params_all.htm"
    webbrowser.open(url3, new=new)


def SelectInput():
    second.SecondWindow(root)

def SelectBackground():
    background.BackgroundWindow(root)


root = Tk()
root.title('SPEX Main Window')
# root.iconbitmap(r"/home/stage/PycharmProjects/testing/Rhessi.ico")
root.geometry("500x600")
# root.config(bg = "black")
# root["bg"] = "gray22"

mainmenu = Menu(root)
root.config(menu=mainmenu)

Label(root,
      text="\n \n \nOSPEX",
      fg="red",
      font="Helvetica 12 bold italic").pack()

Label(root,
      text="\n \n \n \n Spectral Data Analysis Package",
      fg="red",
      font="Times").pack()

Label(root,
      text="\n \n \n Use the buttons under File to: "
           "\n \n 1. Select Input Data Files"
           "\n 2. Define Background and Analysis Intervals, \n and Select Fit Function Components"
           "\n 3. Fit data "
           "\n 4. View Fit Results "
           "\n 5. Save Session and Results"
           "\n \n \n Use Plot_Control buttons to change display of current plot."
           "\n Use Window_Control buttons to redisplay previous plots.",
      fg="blue",
      font="Times",
      justify='left').pack()

filemenu = Menu(mainmenu, tearoff=0)
helpmenu = Menu(mainmenu, tearoff=0)

Select_Input = filemenu.add_command(label="Select Input ...", command=SelectInput)
Select_Background = filemenu.add_command(label="Select Background ...", command=SelectBackground)
filemenu.add_command(label="Select Fit Options and Do Fit ...")
filemenu.add_command(label="Plot Fit Results ...")
filemenu.add_command(label="Set parameters manually ...")
filemenu.add_command(label="Set parameters from script")

filemenu.add_separator()

filemenu.add_command(label="Setup Summary")
filemenu.add_command(label="Fit Results Summary")
filemenu.add_command(label="Write script")
filemenu.add_command(label="Save Fit Results (No Script)")
filemenu.add_command(label="Import Fit Results")
filemenu.add_command(label="Write FITS Spectrum File")

filemenu.add_separator()

filemenu.add_command(label="Clear Stored Fit Results")
filemenu.add_command(label="Reset Entire OSPEX Session to Defaults")

filemenu.add_separator()

filemenu.add_command(label="Set Plot Preferences")

filemenu.add_separator()

filemenu.add_command(label="Configure Plot File")
filemenu.add_command(label="Create Plot File")

filemenu.add_separator()

filemenu.add_command(label="Select Printer ...")

filemenu.add_separator()

filemenu.add_command(label="Configure Print Plot Output...")
filemenu.add_command(label="Print Plot")

filemenu.add_separator()

filemenu.add_command(label="Export Data")
filemenu.add_command(label="Reset Widgets (Recover from Problems)")
filemenu.add_command(label="Exit", command=root.quit)

# Creating Menu command Window_Control
windowmenu = Menu(mainmenu, tearoff=0)
windowmenu.add_command(label="Current Panel")
windowmenu.add_command(label="Show All Panels")
windowmenu.add_command(label="2x2 Panels")
windowmenu.add_command(label="Delete All Panels")
windowmenu.add_command(label="Multi-Panel Options")

# Creating Menu command Help
helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="What's New", command=WhatsNew)
helpmenu.add_command(label="ОSPEX Guide", command=OSPEX_Guide)
helpmenu.add_command(label="OSPEX Parameter Tables", command=OSPEX_Parameter_Tables)
helpmenu.add_command(label="Contacts", command=clickedContact)
helpmenu.add_command(label="Help on Help", command=clickedHelp_on_Help)
helpmenu.add_command(label="ОSPEX Object Reference Retrieval", command=clickedOSPEX_ORR)

mainmenu.add_cascade(label="File", menu=filemenu)
mainmenu.add_cascade(label="Window_Control", menu=windowmenu)
mainmenu.add_cascade(label="Help", menu=helpmenu)

root.mainloop()
