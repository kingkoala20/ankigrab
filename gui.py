from main import *
import customtkinter
from datetime import datetime as dt
import os
import csv

customtkinter.set_appearance_mode("dark")
#TODO Create design for the UI


#-- Timestamp Variables --
DT_TODAY = dt.today()
DATE_TODAY = DT_TODAY.strftime("%m-%d")

class AnkiGrabApp(customtkinter.CTk):
    
    width = "800"
    height = "600"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #--Main Config--
        self.title("Ankigrab")
        #self.geometry(f"{self.width}x{self.height}")
        
        #--Fonts--
        self.fstyle_heading = customtkinter.CTkFont(family="Lucida Bright", size=40)
        
        #--Widgets
        self.header = customtkinter.CTkLabel(self, text="Ankigrab Desktop", font=self.fstyle_heading)
        self.header.grid(row=0, column=0, columnspan=2, pady=(20,10), sticky="NEWS")
        
        #--Frames
        self.entryframe = EntryFrame(self, height=500, width=500, border_width=1)
        self.entryframe.grid(row=1, column=0, sticky="NEWS")
        
        self.toolsframe = ToolsFrame(self, height=500, width=200, border_width=1)
        self.toolsframe.grid(row=1, column=1, sticky="NEWS")
        
class ToolsFrame(customtkinter.CTkFrame):
    pass

class EntryFrame(customtkinter.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        #--Fonts--
        self.fontlabel = customtkinter.CTkFont(family="Lucida Bright", size=18, weight="bold")
        
        #--Widgets--
        self.wordlabel = customtkinter.CTkLabel(self, text="Enter Word: ", font=self.fontlabel)
        self.wordlabel.grid(row=0, column=0, pady=(10, 30), padx=(30,10))
        
        self.wordentry = customtkinter.CTkEntry(self, width = 140)
        self.wordentry.grid(row=0, column=1, pady=(10,30), padx=(10,30))
        
class TodayList(customtkinter.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        #--Varibles Setup--
        current = DATE_TODAY
        filepath = f'.\csvs\{current} words.csv'
        
        self.entries = []
        
        if not os.path.isfile(filepath):
            header = "CSV not yet generated. Please add word to start generation."

        
        #--Displaying List--
        
        
        
if __name__ == "__main__":
    app = AnkiGrabApp()
    app.mainloop()
        
        