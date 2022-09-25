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
from controls import Controls
from screen import Screen
# import logging
# logging.basicConfig(level=logging.DEBUG)
# # logging.basicConfig(level=logging.CRITICAL)
# logger = logging.getLogger(__name__)



if   __name__ == "__main__" :
    root=tk.Tk()
    root.title("Mael JOUSSET : Oscilloscope Simulator")
    root.option_readfile("hello.opt")
    simulator=Generator('x')
    simulator2=Generator('y', mag=0.75)
    screen=Screen(root)
    
    controls = Controls([simulator, simulator2], screen)
    simulator.generate()
    simulator2.generate()
    screen.set_tiles(tiles=10)
    screen.create_grid()
    for model in controls.models:
        controls.plot_signal(model.name, model.signal)
    screen.packing(controls.scale_mag, controls.scale_harmonics, controls.scale_frequency, controls.scale_phase, controls.scale_samples)
    screen.packing(controls.scale_mag2, controls.scale_harmonics2, controls.scale_frequency2, controls.scale_phase2, controls.scale_samples2)
    controls.animate()
    root.mainloop()

