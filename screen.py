# -*- coding: utf-8 -*-
import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin
from utils import radians
from generator import Generator
from observer import Observer
# import logging
# logging.basicConfig(level=logging.DEBUG)
# # logging.basicConfig(level=logging.CRITICAL)
# logger = logging.getLogger(__name__)

class Screen(Observer) :
    def __init__(self,parent,bg="white"):
        Observer.__init__(self)
        self.parent=parent
        self.canvas=tk.Canvas(parent,bg=bg)
        self.canvas.bind("<Configure>", self.resize)
        self.width=int(self.canvas.cget("width"))
        self.height=int(self.canvas.cget("height"))
        self.resize=True
        self.tiles=4
        self.listVariable = tk.Frame(self.parent)
        self.variableFrame = tk.Frame(self.listVariable)
        self.variableFrame2 = tk.Frame(self.listVariable)
        self.pos = 'top'
        self.x,self.y,self.radius=0,0,10
        self.spot=self.canvas.create_oval(
            self.x-self.radius,self.y-self.radius,
            self.x+self.radius,self.y+self.radius,
            fill='yellow',outline='black',tags="spot")
        self.width=int(self.canvas.cget("width"))
        self.height=int(self.canvas.cget("height"))
             
    def __repr__(self):
        return "<Screen(mag:{}, freq:{}, phase:{}, harmonics :{})>".format(self.mag,self.freq,self.phase,self.harmonics)
    def get_canvas(self) :
        return self.canvas
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_tiles(self):
        return self.tiles
    def set_tiles(self,tiles):
        self.tiles=tiles

    def create_grid(self):
        width,height=self.width,self.height
        tiles=self.tiles
        tile_x=width/tiles
        for t in range(1,tiles+1): # lignes verticales
            x=t*tile_x
            self.canvas.create_line(x,0,x,height,tags="grid")
            self.canvas.create_line(x,height/2-5,x,height/2+5 ,width=4,tags="grid")
        tile_y=height/tiles
        for t in range(1,tiles+1): # lignes horizontales
            y=t*tile_y
            self.canvas.create_line(0,y,width,y,tags="grid")
            self.canvas.create_line(width/2-5,y,width/2+5,y,width=4,tags="grid")

    def resize(self, event):
        self.width = event.width
        self.height = event.height
        self.canvas.delete("grid")
        self.create_grid()
        #self.plot_signal()

    def packing(self, scale_mag, scale_harmonics, scale_frequency, scale_phase, scale_samples) :
        self.canvas.pack(expand=1,fill="both",padx=6)
        self.listVariable.pack(side='left')
        self.variableFrame.pack(side='left')
        self.variableFrame2.pack(side='right')
        scale_mag.pack(side = self.pos)
        scale_harmonics.pack(side = self.pos)
        scale_frequency.pack(side = self.pos)
        scale_phase.pack(side = self.pos)
        scale_samples.pack(side = 'top')
        print(self.pos)
        

if __name__ == "__main__" :
    root=tk.Tk()
    root.title("Dupond/Dupont : Oscilloscope Simulator")
    simulator=Generator(root)
    screen = Screen(root)
    simulator.attach(screen)
    screen.set_tiles(tiles=10)
    screen.create_grid()
    screen.packing()
    simulator.generate()
    root.mainloop()
