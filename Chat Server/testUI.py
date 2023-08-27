import tkinter as tk
import tkinter.ttk as ttk

class App():

    def __init__(self):

        # Setting up window
        self.root = tk.Tk()
        self.root.title('Testing scrolling section')
        self.root.geometry('500x400')
        self.root.configure(bg="red")
        self.counter = 0

        self.button = tk.Button(self.root, text='Print: Hello World!', command=self.makeLabel)
        self.button.pack()

        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.mainFrame, bg="blue")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.mainFrame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.resetResolution)

        self.internalFrame = tk.Frame(self.canvas, bg="#000000")
        self.canvas.create_window((0,0), window=self.internalFrame, anchor=tk.NW)

        self.root.mainloop()
    


    def makeLabel(self):
        self.counter += 1
        label = tk.Label(self.internalFrame, text=f"Hello World{self.counter}!")
        label.pack()
        self.resetResolution(None)

    def resetResolution(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

App()