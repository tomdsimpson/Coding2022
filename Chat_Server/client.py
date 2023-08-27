# Python chat client

import socket
import time
import threading
import tkinter as tk
import tkinter.ttk as ttk

# Setting up socket
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Fonts
TITLE_FONT = ("Ubuntu", 40)
BUTTON_FONT = ("Ubuntu", 25)
TEXT_FONT = ("Ubuntu", 15)

def connect(addr):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    return client

class Login():
    def __init__(self):

        # Making Login window
        self.root = tk.Tk()
        self.root.geometry("500x250+500+500")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.title("Login")
        self.username = tk.StringVar()
        self.serverAdress = tk.StringVar()

        # Widgets
        self.title = tk.Label(self.root, text="Login", font=TITLE_FONT)
        self.title.grid(row=1,column=1,columnspan=2)

        self.usernameLabel = tk.Label(self.root, text="Username:", font=BUTTON_FONT)
        self.usernameLabel.grid(row=2,column=1)
        self.usernameInput = tk.Entry(self.root, textvariable=self.username, font=TEXT_FONT)
        self.usernameInput.grid(row=2,column=2)

        self.serverLabel = tk.Label(self.root, text="Server IP:", font=BUTTON_FONT)
        self.serverLabel.grid(row=3,column=1)
        self.serverInput = tk.Entry(self.root, textvariable=self.serverAdress, font=TEXT_FONT)
        self.serverInput.grid(row=3,column=2)

        self.loginButton = tk.Button(self.root, text="Enter", font=BUTTON_FONT, command=self.start)
        self.loginButton.grid(row=4,column=1,columnspan=2)

        self.error = tk.Label(self.root, text="Please Check Inputs", font=TEXT_FONT)
    
        self.root.mainloop()
    
    def start(self):
        # Validating Input
        if len(self.username.get()) >= 3 and len(self.serverAdress.get()) >= 5:
            self.quit()
            App(self.username.get(), self.serverAdress.get())
        else:
            self.error.grid(row=5,column=1,columnspan=2)

    def quit(self):
        self.root.destroy()



class App:

    def __init__(self, username, server):

        # Making the window
        self.root = tk.Tk()
        self.root.geometry("800x1000+500+500")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.title("Chat Window")
        self.state = False
        self.inputText = tk.StringVar()
        self.username = username
        self.serverAdress = server

        # Title
        self.titleFrame = tk.Frame(self.root)
        self.titleFrame.pack(fill='x')
        self.titleFrame.grid_columnconfigure(1, weight=1)
        self.titleFrame.grid_columnconfigure(2, weight=1)

        self.titleLabel = tk.Label(self.titleFrame, text="What's Upp \u2122", font=TITLE_FONT, pady=20)
        self.titleLabel.grid(row=1,column=1,sticky='we',columnspan=2)

        self.connectButton = tk.Button(self.titleFrame, text="Connect", command=self.start, font=BUTTON_FONT, pady=10)
        self.connectButton.grid(row=2,column=1)

        self.disconnectButton = tk.Button(self.titleFrame, text="Disconnect", command=self.disconnect, font=BUTTON_FONT, pady=10)
        self.disconnectButton.grid(row=2,column=2)

        # Scrolable text display for chat
        self.chatFrame = tk.Frame(self.root)
        self.chatFrame.pack(fill='x')
        self.canvas = tk.Canvas(self.chatFrame, height=750, width=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Configure scrollbar
        scrollbar = tk.Scrollbar(self.chatFrame, command=self.canvas.yview, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand = scrollbar.set)
        self.canvas.bind('<Configure>', self.resetResolution)

        # Frame in canvas
        self.content = tk.Frame(self.canvas, padx=50,pady=50)
        self.frame_id = self.canvas.create_window((0,0), window=self.content, anchor='n')

        # Text Input    
        self.inputFrame = tk.Frame(self.root)
        self.inputFrame.pack(fill='x')
        self.inputFrame.grid_columnconfigure(1, weight=1)
        self.inputFrame.grid_columnconfigure(2, weight=1)
        self.inputFrame.grid_columnconfigure(3, weight=1)
        
        self.usernameLabel = tk.Label(self.inputFrame, text=f"{self.username}:", font=BUTTON_FONT)
        self.usernameLabel.grid(row=1,column=1)


        self.messageBox = tk.Entry(self.inputFrame, textvariable=self.inputText, font=TEXT_FONT)
        self.messageBox.grid(row=1,column=2)

        self.messageButton = tk.Button(self.inputFrame, text="Send", command=self.sendMessage, font=BUTTON_FONT)
        self.messageButton.grid(row=1,column=3)

        self.canvas.itemconfigure(self.frame_id, width=500)
        checkMessages = threading.Thread(target=self.checkRecieve)
        checkMessages.daemon = True
        checkMessages.start()
        self.root.mainloop()

    def start(self):
        if self.state == False:
            self.client = connect((self.serverAdress, PORT))
            label = tk.Label(self.content, text="[Succesfuly Connected]", pady=10, font=TEXT_FONT)
            label.pack()
            self.state = True
        else:
            label = tk.Label(self.content, text="[Already Connected]", pady=10, font=TEXT_FONT)
            label.pack()

    def disconnect(self):
        if self.state == True:
            msg = DISCONNECT_MESSAGE
            message = msg.encode(FORMAT)
            self.client.send(message)

            label = tk.Label(self.content, text="[Succesfuly Disconnected]", pady=10, font=TEXT_FONT)
            label.pack()
            self.state = False
        else:
            label = tk.Label(self.content, text="[Already Disconnected]", pady=10, font=TEXT_FONT)
            label.pack()

    def sendMessage(self):
        if self.state == True:
            msg = f"{self.username}:   {self.inputText.get()}"
            message = msg.encode(FORMAT)
            self.client.send(message)

    def checkRecieve(self):
        while True:
            if self.state == True:
                inc_msg = self.client.recv(1024).decode(FORMAT)
                if inc_msg != "":
                    label = tk.Label(self.content, text=inc_msg, font=TEXT_FONT, pady=5, wraplength=400)
                    label.pack(side=tk.TOP)
                    self.resetResolution(None)
            
    def resetResolution(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def quit(self):
        self.disconnect()
        self.root.destroy()


# Displaying window
Login()
