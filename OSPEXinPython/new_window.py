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
import do_fit


class Set_Energy():
    """Class to set Energy range(s) in Y axis"""
    yVal = None
    """Value(s) for Y axis"""

    def __init__(self, parent):
            """Creating a new window called 'SPEX Fit Options'"""
            self.p = parent
            #self.rootP = rootParent
            self.newwin2 = Toplevel(parent)
            self.newwin2.title('XTEXTEDIT') #title of the window
            self.newwin2.geometry("600x400") #size of the new window
            self.display2 = Label(self.newwin2, text = "\n Enter Energy range(s)(keV) in the following format: "
                                             "Start_-_End"
                                             "\n \n Use '-' as separators"
                                             "\n \n Example: '10_-_20'",
                                      fg='black', 
                                      font=("Times", 11))
            self.display2.place(relx=0.15, rely=0.02)
            self.e = StringVar()
            self.e.set('10 - 20')
            self.ee1 = Entry(self.newwin2, textvariable = self.e )
            self.ee1.place(relx=0.35, rely=0.35, relheight=0.07,relwidth=0.25)
    
            Set_Energy.yVal = self.ee1.get()

            show_Button = Button(self.newwin2, text = "Finished editing", command = self.show_entry_fields)
            show_Button.place(relx=0.15, rely=0.75, relheight=0.05, relwidth=0.20)

    def show_entry_fields(self):
            """Getting the values from user choice"""
            do_fit.Fitting.setEVal = self.ee1.get()
            do_fit.Fitting.evalue.set(self.ee1.get())
            print('fitting e', self.ee1.get(), do_fit.Fitting.evalue)
            self.newwin2.destroy()
    
        

   
        
