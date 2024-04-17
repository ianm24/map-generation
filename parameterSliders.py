# Program Made By: Ian McDowell
# Started 22 Oct 2020

from tkinter import *
from PIL import Image, ImageTk

# imDir = "./maps/"
imDir = "./archive/15Nov2022_19-42EST/"
tk = Tk()
tk.title("Parameter-Varying Map Viewer")
tk.minsize(650, 250)
LCI = DoubleVar(value=0.0)
LTW = DoubleVar(value=0.5)
NR = StringVar(value="1")

# LCI Slider
Label(tk, text="LCI:").place(x=10, y=100)
Scale(tk,
      from_=-1.0,
      to=1.0,
      length=550,
      resolution=0.1,
      orient=HORIZONTAL,
      variable=LCI).place(x=50, y=80)
# LTW Slider
Label(tk, text="LTW:").place(x=10, y=160)
Scale(tk,
      from_=0.0,
      to=1.0,
      length=550,
      resolution=0.1,
      orient=HORIZONTAL,
      variable=LTW).place(x=50, y=140)
# NR Buttons
Label(tk, text="NR:").place(x=10, y=200)
NRArr = ["1", "H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10",
         "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10"]
counter = 0
for val in NRArr:
    Radiobutton(tk,
                text=val,
                variable=NR,
                value=val).place(x=40+50*int(counter % 11), y=200+20*int(counter/11))
    counter += 1
# #CurrentMap
path = imDir+"map_LCIn"+str(round(LCI.get(), 1)).replace("-", "n").replace(
    ".", "-")+"_LTW"+str(round(LTW.get(), 1)).replace(".", "-")+"_NR-"+NR.get()+".bmp"
img = ImageTk.PhotoImage(Image.open(path))
panel = Label(tk, image=img)
panel.place(x=278, y=20)


while True:
    tk.update()
    if LCI.get() == 0.0:
        path = imDir+"map_LCIn"+str(round(LCI.get(), 1)).replace("-", "n").replace(
            ".", "-")+"_LTW"+str(round(LTW.get(), 1)).replace(".", "-")+"_NR-"+NR.get()+".bmp"
    else:
        path = imDir+"map_LCI"+str(round(LCI.get(), 1)).replace("-", "n").replace(
            ".", "-")+"_LTW"+str(round(LTW.get(), 1)).replace(".", "-")+"_NR-"+NR.get()+".bmp"
    img = ImageTk.PhotoImage(Image.open(path))
    panel.configure(image=img)
    panel.image = img
