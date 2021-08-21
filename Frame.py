import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import random
from sort import *

from PIL import Image, ImageTk, ImageDraw

sortModes = {"bubble":bubbleSort, "selection":selectionSort, "insertion":insertionSort, "merge":mergeSort, "bogo":bogoSort}

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
    
        self.placeWidget()
    
    def placeWidget(self):
        self.canvas = SortCanvas(self, 700, 400)
        self.canvas.pack()

        self.input = Input(self, 700, 200)
        self.input.addSortCanvas(self.canvas)
        self.input.pack(padx=10)

class SortCanvas(tk.Frame):
    def __init__(self, master, width, height, count=100, sortMode="bubble"):
        super().__init__(master, width=width, height=height)

        self.width = width
        self.height = height

        self.array = np.array(range(1, 101))
        random.shuffle(self.array)

        self.state = "waiting"
        self.sortMode = sortMode
        self.count = count
        self.sort = sortModes[self.sortMode](self.array)

        self.delay = 1

        self.id = None

        self.placeWidget()
        self.draw([(0, self.array, dict())])
    
    def placeWidget(self):
        self.canvas = tk.Canvas(self, bg="black", width=self.width, height=self.height)
        self.canvas.pack()
    
    def draw(self, arrays):
        self.canvas.delete("all")

        n = len(self.array)

        if (self.width/n < 4):
            outline = "white"
        else:
            outline = "black"

        self.image = Image.new("RGB", (self.width, self.height), (0,0,0))
        draw = ImageDraw.Draw(self.image)

        for begin, array, points in arrays:

            for index, i in enumerate(array):
                pos1 = (self.width/n*(begin + index), self.height - self.height/n*i)
                pos2 = (self.width/n*(begin + index + 1), self.height)

                if (index in points.keys()):
                    draw.rectangle([pos1, pos2], fill=points[index], outline=outline, width=1)
                else:
                    draw.rectangle([pos1, pos2], fill="white", outline=outline, width=1)
        
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(1,0, anchor = "nw", image=self.image)
    
    def startSorting(self):
        if (self.state == "waiting"):
            self.sort = sortModes[self.sortMode](self.array)
        elif (self.state == "over" or self.state == "sorting"):
            return

        self.state = "sorting"
        self.next()
    
    def reset(self):
        self.state = "waiting"
        if (self.id != None):
            self.after_cancel(self.id)

        self.array = np.array(range(1, self.count+1))
        random.shuffle(self.array)
        self.draw([(0, self.array, dict())])

    def next(self):
        if (self.state == "waiting"):
            self.sort = sortModes[self.sortMode](self.array)
            self.state = "pause"

        arrays = next(self.sort)
        
        if (arrays == None):
            self.state = "over"
            self.draw([(0, self.array, dict())])
            return

        self.draw(arrays)

        if (self.state == "sorting"):
            self.id = self.after(self.delay, self.next)
        else:
            self.id = None
    
    def step(self):
        if (self.state == "waiting"):
            self.sort = sortModes[self.sortMode](self.array)
            self.state = "pause"
            self.next()
        elif (self.state == "sorting"):
            self.state = "pause"
        elif (self.state == "pause"):
            self.next()

class Input(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height)

        self.width = width
        self.height = height

        self.sortCanvases = []

        self.placeWidget()
    
    def addSortCanvas(self, *lst):
        for i in lst:
            self.sortCanvases.append(i)
    
    def placeWidget(self):
        self.runButton = ttk.Button(self, text="run", width=6, command=self.master.canvas.startSorting, takefocus=False)
        self.runButton.pack(side="left", padx=5, pady=5)

        self.stepButton = ttk.Button(self, text="step", width=6, command=self.master.canvas.step, takefocus=False)
        self.stepButton.pack(side="left", padx=5, pady=5)

        self.shuffleButton = ttk.Button(self, text="reset", width=6, command=self.master.canvas.reset, takefocus=False)
        self.shuffleButton.pack(side="left", padx=5, pady=5)

        self.sortModeComboBox = ttk.Combobox(self, width=10, values=list(sortModes.keys()), state="readonly", takefocus=False)
        self.sortModeComboBox.set("bubble")
        self.sortModeComboBox.bind("<<ComboboxSelected>>", self.setSortMode)
        self.sortModeComboBox.pack(side="left", padx=5, pady=5)

        self.countBox = ttk.Spinbox(self, width=4, from_=5, to=500, state="readonly", wrap=True, increment=5, takefocus=False, command=self.setCount)
        self.countBox.set(100)
        self.countBox.pack(side="left", padx=5, pady=5)
    
    def startSorting(self):
        for i in self.sortCanvases:
            i.startSorting()
    
    def step(self):
        for i in self.sortCanvases:
            i.step()
    
    def reset(self):
        for i in self.sortCanvases:
            i.reset()

    def setSortMode(self, event):
        for i in self.sortCanvases:
            i.sortMode = self.sortModeComboBox.get()
    
    def setCount(self):
        for i in self.sortCanvases:
            i.count = int(self.countBox.get())