# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
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
from screen import Screen
import json
from PIL import Image
from pyscreenshot import grab
# import logging
# logging.basicConfig(level=logging.DEBUG)
# # logging.basicConfig(level=logging.CRITICAL)
# logger = logging.getLogger(__name__)

class Controls :
    def __init__(self, models, view):
        self.models, self.view = models, view
        self.create_controls()
        self.x, self.y, self.radius = 0,0,10
        self.spot = self.view.canvas.create_oval(
            self.x-self.radius, self.y-self.radius,
            self.x+self.radius, self.y+self.radius,
            fill='yellow', outline='black',tags='spot')
        self.canvas_xy = 0

    def configure(self, event=None):
        fillColor = ''
        if self.view.parent.fillVar.get(): fillColor = self.view.parent.colorVar.get()

        outlineColor = ''
        if self.view.parent.outlineVar.get(): outlineColor = 'black'
		
        self.view.canvas.itemconfigure(self.arc, style=self.view.parent.styleVar.get())
        self.view.canvas.itemconfigure(self.arc, fill=fillColor)
        self.view.canvas.itemconfigure(self.arc, outline=outlineColor)
        
    def __repr__(self):
        return "<Controls(mag:{}, freq:{}, phase:{}, harmonics :{})>".format(self.mag,self.freq,self.phase,self.harmonics)

    def cb_update_magnitude(self,event):
        print("cb_update_magnitude(self,event)",self.mag_var.get())
        self.models[0].set_magnitude(self.mag_var.get())
        self.models[0].generate()
        self.plot_signal(self.models[0].name, self.models[0].signal)
 
    def cb_update_harmonics(self,event):
        print("cb_update_harmonics(self,event)",self.harmonics_var.get())
        self.models[0].set_harmonics(self.harmonics_var.get())
        self.models[0].generate()
        self.plot_signal(self.models[0].name, self.models[0].signal)
            
    def cb_update_frequency(self,event):
        print("cb_update_frequency(self,event)",self.frequency_var.get())
        self.models[0].set_frequency(self.frequency_var.get())
        self.models[0].generate()
        self.plot_signal(self.models[0].name, self.models[0].signal)
            
    def cb_update_phase(self,event):
        print("cb_update_phase(self,event)",self.phase_var.get())
        self.models[0].set_phase(self.phase_var.get())
        self.models[0].generate()
        self.plot_signal(self.models[0].name, self.models[0].signal)
            
    def cb_update_samples(self,event):
        print("cb_update_samples(self,event)",self.samples_var.get())
        self.models[0].set_samples(self.samples_var.get())
        self.models[0].generate()
        self.plot_signal(self.models[0].name, self.models[0].signal)

    def cb_update_magnitude2(self,event):
        print("cb_update_magnitude(self,event)",self.mag_var2.get())
        self.models[1].set_magnitude(self.mag_var2.get())
        self.models[1].generate()
        self.plot_signal(self.models[1].name, self.models[1].signal)
 
    def cb_update_harmonics2(self,event):
        print("cb_update_harmonics(self,event)",self.harmonics_var2.get())
        self.models[1].set_harmonics(self.harmonics_var2.get())
        self.models[1].generate()
        self.plot_signal(self.models[1].name, self.models[1].signal)
            
    def cb_update_frequency2(self,event):
        print("cb_update_frequency(self,event)",self.frequency_var2.get())
        self.models[1].set_frequency(self.frequency_var2.get())
        self.models[1].generate()
        self.plot_signal(self.models[1].name, self.models[1].signal)
            
    def cb_update_phase2(self,event):
        print("cb_update_phase(self,event)",self.phase_var2.get())
        self.models[1].set_phase(self.phase_var2.get())
        self.models[1].generate()
        self.plot_signal(self.models[1].name, self.models[1].signal)
            
    def cb_update_samples2(self,event):
        print("cb_update_samples(self,event)",self.samples_var2.get())
        self.models[1].set_samples(self.samples_var2.get())
        self.models[1].generate()
        self.plot_signal(self.models[1].name, self.models[1].signal)
            
    def about_us(self):
        tk.messagebox.showinfo(title="About Us", message="Mael JOUSSET m9jousse@enib.fr")

    def about_tk(self):
        tk.messagebox.showinfo(title="About Tk", message="des infos sur TkInter")
    
    def about_python(self):
        tk.messagebox.showinfo(title="About Python", message="Python version : 3.10.3")

    def exit(self):
        tmp = tk.messagebox.askquestion(title="Exit", message="do you want to quit ?")
        print(tmp)
        if tmp == "yes":
            self.view.parent.quit()

    def open(self):
        #io = open("out.json","r")
        #dictionary = json.load(io)
        #print(dictionary)
        name = tk.filedialog.askopenfilename()
        io = open(name, "r")
        dictionarys = json.load(io)
        for i in range(len(dictionarys)):
            self.models[i].set_name(dictionarys[i]['name'])
            self.models[i].set_magnitude(dictionarys[i]['mag'])
            self.models[i].set_frequency(dictionarys[i]['freq'])
            self.models[i].set_phase(dictionarys[i]['phase'])
            self.models[i].set_harmonics(dictionarys[i]['harmo'])
            self.models[i].set_samples(dictionarys[i]['samples'])
            self.models[i].generate()
            self.plot_signal(self.models[i].name, self.models[i].signal)

    def save(self):
        dictionnarys = []
        for model in self.models:
            dictionnary = {
                'name' : model.get_name(),
                'mag' : model.get_magnitude(),
                'freq' : model.get_frequency(),
                'phase' : model.get_phase(),
                'harmo' : model.get_harmonics(),
                'samples' : model.get_samples()
            }
            dictionnarys.append(dictionnary)
        
        file = tk.filedialog.asksaveasfilename(filetypes=[("json file", ".json")], defaultextension=".json")
        for dictionnary in dictionnarys:
            json.dump(dictionnarys, open(file, "w"))
        
    def save_image(self):
        if self.pos :
            list = self.view.canvas.coords(self.pos)
            img = grab(bbox=(400, 500, 1000, 1200))
            
            file = tk.filedialog.asksaveasfilename(filetypes=[("png file", ".png")], defaultextension=".png")
            img.save(file)

    def open_window(self):
        newWindow = tk.Toplevel(self.view.parent)
        newWindow.title("X-Y")
        newWindow.geometry("200x200")
        self.canvas_xy = tk.Canvas(newWindow)

    def create_controls(self):
        menubar = tk.Menu(self.view.parent)
        menu1 = tk.Menu(menubar, tearoff=0)
        menu1.add_command(label="Open", command=self.open)
        menu1.add_command(label="Save", command=self.save)
        menu1.add_command(label="Save Image", command=self.save_image)
        menu1.add_separator()
        menu1.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=menu1)
        menu2 = tk.Menu(menubar, tearoff=0)
        menu2.add_command(label="About Us", command=self.about_us)
        menu2.add_command(label="About Tk", command=self.about_tk)
        menu2.add_command(label="About Python", command=self.about_python)
        menubar.add_cascade(label="Help", menu=menu2)
        self.view.parent.config(menu=menubar)

        btn = tk.Button(self.view.parent,
             text ="X-Y",
             command = self.open_window)
        btn.pack()

        self.mag_var=tk.DoubleVar()
        self.mag_var.set(self.models[0].get_magnitude())
        self.scale_mag=tk.Scale(self.view.variableFrame,variable=self.mag_var,
                            label="Amplitude",
                            orient="horizontal",length=250,
                            from_=0,to=1,relief="raised",
                            sliderlength=20,resolution = 0.1,
                            tickinterval=0.5,
                            command=self.cb_update_magnitude)
        self.harmonics_var=tk.IntVar()
        self.harmonics_var.set(self.models[0].get_harmonics())
        self.scale_harmonics=tk.Scale(self.view.variableFrame,variable=self.harmonics_var,
                                label="Harmonics",
                                orient="horizontal",length=250,
                                from_=1,to=50,relief="raised",
                                sliderlength=20,tickinterval=5,
                                command=self.cb_update_harmonics)
        self.frequency_var=tk.IntVar()
        self.frequency_var.set(self.models[0].get_frequency())
        self.scale_frequency=tk.Scale(self.view.variableFrame,variable=self.frequency_var,
                                label="Frequency",
                                orient="horizontal",length=250,
                                from_=1,to=10,relief="raised",
                                sliderlength=20,tickinterval=1,
                                command=self.cb_update_frequency)
        self.phase_var=tk.IntVar()
        self.phase_var.set(self.models[0].get_phase())
        self.scale_phase=tk.Scale(self.view.variableFrame,variable=self.phase_var,
                                label="Phase",
                                name="phase",
                                orient="horizontal",length=250,
                                from_=-45,to=45,relief="raised",
                                sliderlength=20,tickinterval=10,
                                command=self.cb_update_phase)
        self.samples_var=tk.IntVar()
        self.samples_var.set(self.models[0].get_samples())
        self.scale_samples=tk.Scale(self.view.variableFrame,variable=self.samples_var,
                                label="Samples",
                                orient="horizontal",length=250,
                                from_=50,to=200,relief="raised",
                                sliderlength=20,tickinterval=30,
                                command=self.cb_update_samples)
        frame=tk.LabelFrame(self.view.parent,text="Frequency")
        self.radio_var=tk.IntVar()
        btn=tk.Radiobutton(frame,text="All", variable=self.radio_var,value=1,command=self.cb_activate_button)
        btn.select()
        btn.pack(anchor ="w")
        btn=tk.Radiobutton(frame,text="Odd", variable=self.radio_var,value=2,command=self.cb_activate_button)
        btn.pack(anchor ="w")

        self.mag_var2=tk.DoubleVar()
        self.mag_var2.set(self.models[1].get_magnitude())
        self.scale_mag2=tk.Scale(self.view.variableFrame2,variable=self.mag_var2,
                            label="Amplitude",
                            orient="horizontal",length=250,
                            from_=0,to=1,relief="raised",
                            sliderlength=20,resolution = 0.1,
                            tickinterval=0.5,
                            command=self.cb_update_magnitude2)
        self.harmonics_var2=tk.IntVar()
        self.harmonics_var2.set(self.models[1].get_harmonics())
        self.scale_harmonics2=tk.Scale(self.view.variableFrame2,variable=self.harmonics_var2,
                                label="Harmonics",
                                orient="horizontal",length=250,
                                from_=1,to=50,relief="raised",
                                sliderlength=20,tickinterval=5,
                                command=self.cb_update_harmonics2)
        self.frequency_var2=tk.IntVar()
        self.frequency_var2.set(self.models[1].get_frequency())
        self.scale_frequency2=tk.Scale(self.view.variableFrame2,variable=self.frequency_var2,
                                label="Frequency",
                                orient="horizontal",length=250,
                                from_=1,to=10,relief="raised",
                                sliderlength=20,tickinterval=1,
                                command=self.cb_update_frequency2)
        self.phase_var2=tk.IntVar()
        self.phase_var2.set(self.models[1].get_phase())
        self.scale_phase2=tk.Scale(self.view.variableFrame2,variable=self.phase_var2,
                                label="Phase",
                                name="phase",
                                orient="horizontal",length=250,
                                from_=-45,to=45,relief="raised",
                                sliderlength=20,tickinterval=10,
                                command=self.cb_update_phase2)
        self.samples_var2=tk.IntVar()
        self.samples_var2.set(self.models[1].get_samples())
        self.scale_samples2=tk.Scale(self.view.variableFrame2,variable=self.samples_var2,
                                label="Samples",
                                orient="horizontal",length=250,
                                from_=50,to=200,relief="raised",
                                sliderlength=20,tickinterval=30,
                                command=self.cb_update_samples2)
        frame2=tk.LabelFrame(self.view.parent,text="Frequency")
        self.radio_var2=tk.IntVar()
        btn=tk.Radiobutton(frame2,text="All", variable=self.radio_var2,value=1,command=self.cb_activate_button2)
        btn.select()
        btn.pack(anchor ="w")
        btn=tk.Radiobutton(frame2,text="Odd", variable=self.radio_var2,value=2,command=self.cb_activate_button2)
        btn.pack(anchor ="w")
        frame.pack()
        frame2.pack()
        
    def cb_activate_button(self):
        print("You selected the option " + str(self.radio_var.get()))
        self.models[0].harmo_odd_even=self.radio_var.get()
        self.models[0].generate()

    def cb_activate_button2(self):
        print("You selected the option " + str(self.radio_var2.get()))
        self.models[1].harmo_odd_even=self.radio_var2.get()
        self.models[1].generate()

    def plot_signal(self, name, signal):
        width,height=self.view.get_width(),self.view.get_height()
        if signal and len(signal)>1:
            self.view.get_canvas().delete(name)
            plot=[(x*width, height/2*(y+1)) for (x,y) in signal]
            self.pos = self.view.get_canvas().create_line(plot,fill='red',smooth=1,width=3,tags=name)

    def update(self, subject):
        name=subject.get_name()
        signal=subject.get_signal()
        if name not in self.signals.keys() :
            self.signals[name]=signal
        self.canvas.delete(name)
        self.plot_signal(name, signal)

    def animate(self, i=0):
        width,height=self.view.canvas.winfo_width(),self.view.canvas.winfo_height()
        msec=50
        if i==len(self.models[0].signal) :
            i=0
        x,y=self.models[0].signal[i][0]*width, height/2*(self.models[0].signal[i][1]+1)
        self.view.canvas.coords(self.spot,x,y,x+self.radius,y+self.radius)
        after_id=self.view.parent.after(msec, self.animate,i+1)
        return after_id     

if   __name__ == "__main__" :
    root=tk.Tk()
    root.title("Dupond/Dupont : Oscilloscope Simulator")
    simulator=Generator()
    screen=Screen(root)
    controls = Controls(simulator, screen)
    simulator.generate()
    screen.set_tiles(tiles=10)
    screen.create_grid()
    controls.plot_signal('red')
    screen.packing(controls.scale_mag, controls.scale_harmonics, controls.scale_frequency, controls.scale_phase)
    root.mainloop()

