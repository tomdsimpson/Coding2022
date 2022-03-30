# Wordle Solver Attempt Two
# Tom Simpson

# Importing modules
import json


# Reading in guesses
with open("guesses.txt") as file:
    guesses = []
    for line in file:
        guesses.append(line.strip())

# Read in fequency map
with open("freq_map.json", "r") as file:
    freq_map = json.load(file)



# Calculating Letter Frequencies
def find_frequencies(word_list):

    frequencies = {"a":[0, 0, 0, 0, 0], "b":[0, 0, 0, 0, 0], "c":[0, 0, 0, 0, 0], "d":[0, 0, 0, 0, 0], "e":[0, 0, 0, 0, 0], "f":[0, 0, 0, 0, 0], "g":[0, 0, 0, 0, 0], "h":[0, 0, 0, 0, 0], "i":[0, 0, 0, 0, 0], "j":[0, 0, 0, 0, 0], "k":[0, 0, 0, 0, 0], "l":[0, 0, 0, 0, 0], "m":[0, 0, 0, 0, 0], "n":[0, 0, 0, 0, 0], "o":[0, 0, 0, 0, 0], "p":[0, 0, 0, 0, 0], "q":[0, 0, 0, 0, 0], "r":[0, 0, 0, 0, 0], "s":[0, 0, 0, 0, 0], "t":[0, 0, 0, 0, 0], "u":[0, 0, 0, 0, 0], "v":[0, 0, 0, 0, 0], "w":[0, 0, 0, 0, 0], "x":[0, 0, 0, 0, 0], "y":[0, 0, 0, 0, 0], "z":[0, 0, 0, 0, 0], }
    for word in word_list:
        for character in range(len(word)):
            frequencies[word[character]][character] += 1

    return frequencies



# Calculating Word Score
def wordScore(word_list, freq, freq_map):

    words = {}
    max_freq = [0, 0, 0, 0, 0]

    for c in freq:
        for x in range(0, 5):
            if max_freq[x] < freq[c][x]:
                max_freq[x] = freq[c][x]

    print(max_freq)

    for w in word_list:
        score = 1
        for x in range(0,5):
            c = w[x]
            score *= 1 + (freq[c][x] - max_freq[x]) ** 2

        if float(freq_map[w]) != 0:
            score /= float(freq_map[w])
        words.update({w:score})
    
    return words


# Removing impossible answers
def trim_list(word_list, guess, pattern):

    new_list = []

    # Checking everyword in list of acceptable guesses        
    for w in word_list:

        word_data = [w, ["0", "0", "0", "0", "0"]]
        valid = True

        # Green pass
        for c in range(0, 5):
            if pattern[c] == "g":
                if guess[c] != word_data[0][c]:
                    valid = False
                else:
                    word_data[1][c] = "1"


        # Yellow pass if valid
        if valid:
            for c in range(0, 5):
                
                # Yellow Grey Pass
                if pattern[c] == "y":

                    if guess[c] == word_data[0][c]:
                        valid = False
                    
                    else:
                        valid = False
                        for x in range(len(word_data[0])):

                            if word_data[0][x] == guess[c] and x != c and word_data[1][x] != "1":

                                valid = True
                                word_data[1][x] = "1"
                                break
                if not valid:
                    break

        # Grey pass if valid
        if valid:
  
            for c in range(0, 5):
                if pattern[c] == "w":
                    for x in range(len(word_data[0])):

                        if word_data[0][x] == guess[c] and word_data[1][x] == "0":
                            valid = False

        if valid:
            new_list.append(w)
        
    return new_list








for x in range(6):
    freq = find_frequencies(guesses)
    #print(freq)
    word_scores = wordScore(guesses, freq, freq_map)
    print(min(word_scores, key=word_scores.get))
    guess = input("What was your guess?   ")
    pattern = input("What was your pattern?   ")
    new_guesses = trim_list(guesses, guess, pattern)
    guesses = new_guesses

    if len(guesses) == 1:
        print(f"Win: {guesses[0]}")
        break
    #print(new_guesses)


# Each iteration of this up to six you need to trim word list


#new_list = trim_list(guesses, "cooky", "wwyww")
#print(new_list)
