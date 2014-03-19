from Tkinter import *
import os
import sys
sys.path.append("..")
from mod.GUI import *

root = Tk(className="smart dictionary")

app = SmartD_GUI(root)

root.mainloop()
