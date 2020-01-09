from tkinter import *
import background

class EditSelectedInterval():
    """Class to create an editSelectedInterval Window"""
 
    def __init__(self, p):
        #self.p = p
        self.top1 = Toplevel(p)
        self.top1.title('Edit time interval')
        self.top1.geometry("480x200")
        Label(self.top1,
              text="Enter new Time Interval in the following format: start - end \n Example: 08:05 - 08:07",
              fg="black",
              font="Helvetica 12 bold italic").pack()
        


        """                         First frame                                     """

        self.frame1 = LabelFrame(self.top1, relief=RAISED, borderwidth=2)
        self.frame1.place(relx=0.05, rely=0.2, relheight=0.4, relwidth=0.9)

        self.c = StringVar()
        self.c.set('08:30 - 08:40')
        
        self.setIntervalText = Entry(self.frame1, width=50, textvariable = self.c)
        self.setIntervalText.place(relx=0.1, rely=0.25)
     

        self.Validate = Button(self.top1, text="Accept And Close", command=self.quit)
        self.Validate.place(relx=0.4, rely=0.8)



    def quit(self):

##        self.p.update()
##        self.p.deiconify()
        print('cccccccccccc',  self.setIntervalText.get())
        background.BackgroundWindow.bkgTimeInterv = self.setIntervalText.get()

        self.top1.destroy()



 





  
