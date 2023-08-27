# Wordle Game (TKinter)
# Tom Simpson

# Importing Modules
import tkinter as tk
import random as r



# Generating possible answer list
def read_answers():

    answers = []
    with open("../Solver/guesses.txt", "r") as f:
        for line in f:
             answers.append(line.strip())
    return answers


# --- Defining Window --- #
class wordleUI:

    def __init__(self):

        self.root = tk.Tk()
        master = self.root

        # Initialising Gameplay stuff
        self.answers = read_answers()
        self.answer = self.answers[r.randint(0, len(self.answers)-1)]
        self.height = 1
        self.gameState = True
        self.colors = {"w":"#777777", "g":"#3d9929", "y":"#e4dc2e"}

        # Initialising Tk stuff
        self.titleFont = ('Helvetica bold',40)
        self.labelFont = ('Helvetica bold',20)
        self.displayFont = ('Helvetica bold',35)

        master.geometry("600x800+1200+200")
        master.config(background="#eeeeee")
        master.title("Wordle")
        master.iconphoto(False, tk.PhotoImage(file='./icon.png'))

        frame = tk.Frame(master)
        frame.grid(row=1,column=1)
        frame.config(background="#eeeeee")

        self.feedback = tk.Frame(master)
        self.feedback.grid(row=2,column=1)
        self.feedback.config(background="#eeeeee")

        controls = tk.Frame(master)
        controls.grid(row=3,column=1)
        controls.config(background="#eeeeee")

        # Making widgets
        self.titleLabel = tk.Label(frame, width = 15, height = 1, text="Wordle", font=self.titleFont, background="#eeeeee")
        self.titleLabel.grid(row=1,column=1,columnspan=5)

        self.inputSection = tk.Text(frame, width = 10, height = 1, font=("Helvetica bold",30))
        self.inputSection.grid(row=2, column=1, columnspan=3, pady=10, padx=5)

        self.submitButton = tk.Button(frame, width = 8, height = 1, font=self.labelFont, text="Submit", command=self.game_phase)
        self.submitButton.grid(row=2, column=4, columnspan=2, pady=10)

        self.retartButton = tk.Button(controls, text="Replay", command=self.restartGame, width = 8, height = 1, font=self.labelFont)
        self.retartButton.grid(row=1,column=1,padx=5,pady=5)

        self.quitButton = tk.Button(controls, text="Quit", command=self.quitGame, width = 8, height = 1, font=self.labelFont)
        self.quitButton.grid(row=1,column=2,padx=5,pady=5)

        # Filler
        for x in range(6):
            spacer = tk.Label(self.feedback, text="", background="#eeeeee", font=self.displayFont)
            spacer.grid(row=x+1,column=1,pady=8)

        # Running window
        self.root.mainloop()


    # Game Functionality
    def game_phase(self):

        # Checking if won or invalid input
        if self.gameState != "win":self.gameState = "play"
        self.validateInput()
        if self.gameState != "play":return "VOID"

        # Getting guess and check frame
        guess = (self.inputSection.get(1.0, "end-1c")).lower()
        output = [["", "", "", "", ""], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]] # Pattern LetterUsed AnswerLetterUsed

        #Green pass
        for c in range(len(guess)):
            if guess[c] == self.answer[c]:
                output[0][c] = "g"
                output[1][c] = 1
                output[2][c] = 1

        # Yellow pass
        for c1 in range(len(guess)):        
            for c2 in range(len(self.answer)):
                if output[1][c1] == 0 and output[2][c2] == 0:               
                    if c1 != c2 and guess[c1] == self.answer[c2]:
                        output[0][c1] = "y"
                        output[1][c1] = 1
                        output[2][c2] = 1

        # Grey pass
        for c in range(len(guess)):
            if output[1][c] == 0:
                output[0][c] = "w"
                output[1][c] = 1

        # Extracting needed data
        display_output = [output[0], guess.upper()]

        # --- Displaying --- #
        for x in range(len(display_output[0])):
            label = tk.Label(self.feedback, text=display_output[1][x], width = 2, height = 1, background = self.colors[display_output[0][x]], fg="#ffffff", font=self.displayFont)
            label.grid(row=self.height,column=x+1,pady=8,padx=5)
        self.height += 1

        if output[0] == ["g", "g", "g", "g", "g"]:
            self.gameState = "win"


    # Control button functions
    def quitGame(self):
        self.root.destroy()
    
    def restartGame(self):
        self.root.destroy()
        wordle = wordleUI()

    def validateInput(self):

        guess = (self.inputSection.get(1.0, "end-1c")).lower()
        if self.height == 7:
            self.gameState="invalid"
        if len(guess) != 5:
            self.gameState="invalid"
        if guess not in self.answers:
            self.gameState="invalid"

        


# -- Main code --- #
wordle = wordleUI()



    
