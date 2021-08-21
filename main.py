import tkinter as tk
from Frame import *

def main():
    root = tk.Tk()

    app = MainFrame(root)
    app.pack(fill="both")

    root.update()
    
    width = app.winfo_width()
    height = app.winfo_height()

    root.geometry(f"{width}x{height}")
    root.mainloop()

if (__name__ == "__main__"):
    main()