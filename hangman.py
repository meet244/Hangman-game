import tkinter as tk
from tkinter import messagebox
import random
from playsound import playsound


# Define the list of words
words = ["apple", "banana", "cherry", "orange", "lemon", "grape", "pineapple", "watermelon"]

# Choose a random word from the list
word = random.choice(words)

# Initialize the number of guesses and the list of guessed letters
guesses = 6
guessed_letters = []

# Create the main window
root = tk.Tk()
root.title("Hangman")

# Create the canvas for drawing the hangman
canvas = tk.Canvas(root, width=300, height=300)
canvas.grid(column=0, row=0)

# Draw the scaffold
canvas.create_line(20, 280, 120, 280)
canvas.create_line(70, 280, 70, 20)
canvas.create_line(70, 20, 170, 20)
canvas.create_line(170, 20, 170, 50)

# Create a label for displaying the word
word_label = tk.Label(root, text=" ".join(["_" for letter in word]))
word_label.grid(column=0, row=1)

# Create a label for displaying the number of guesses remaining
guesses_label = tk.Label(root, text="Guesses remaining: {}".format(guesses))
guesses_label.grid(column=0, row=2)

# Create a label for displaying the letters guessed so far
guessed_label = tk.Label(root, text="Guessed letters: ")
guessed_label.grid(column=0, row=3)

# Create an entry for the user to guess a letter
guess_entry = tk.Entry(root)
guess_entry.grid(column=0, row=4)

# Define a function to check the user's guess
def check_guess():
    global guesses
    global guessed_letters
    global word_label
    
    guess = guess_entry.get().lower()
    guess_entry.delete(0, tk.END)
    
    # Check if the guess is a single letter
    if len(guess) != 1 or not guess.isalpha():
        return
    
    # Check if the guess has already been guessed
    if guess in guessed_letters:
        return
    
    guessed_letters.append(guess)
    guessed_label.config(text="Guessed letters: {}".format(" ".join(guessed_letters)))
    
    # Check if the guess is in the word
    if guess in word:
        word_list = list(word_label["text"])
        for i in range(len(word)):
            if word[i] == guess:
                word_list[2*i] = guess
        word_label.config(text="".join(word_list))
        
        # Check if the user has won
        if "_" not in word_list:
            playsound("win.wav")
            messagebox.showinfo("Hangman", "You win!")
            retry_button.grid(column=0, row=5)
            exit_button.grid(column=0, row=6)
            guess_entry.config(state=tk.DISABLED)
            return
    
    # If the guess is not in the word, decrement the number of guesses remaining
    else:
        guesses -= 1
        guesses_label.config(text="Guesses remaining: {}".format(guesses))
        
        # Draw the hangman
        if guesses == 5:
            canvas.create_oval(140, 50, 200, 110)
        elif guesses == 4:
            canvas.create_line(170, 110, 170, 170)
        elif guesses == 3:
            canvas.create_line(170, 130, 140, 140)
        elif guesses == 2:
            canvas.create_line(170, 130, 200, 140)
        elif guesses == 1:
            canvas.create_line(170, 170, 140, 190)
        elif guesses == 0:
            canvas.create_line(170, 170, 200, 190)
            playsound("lose.mp3")
            messagebox.showinfo("Hangman", "You lose! The word was '{}'".format(word))
            retry_button.grid(column=0, row=5)
            exit_button.grid(column=0, row=6)
            guess_entry.config(state=tk.DISABLED)

def retry_game():
    global word
    global guesses
    global guessed_letters
    word = random.choice(words)
    guesses = 6
    guessed_letters = []

    word_label.config(text=" ".join(["_" for letter in word]))
    guesses_label.config(text="Guesses remaining: {}".format(guesses))
    guessed_label.config(text="Guessed letters: ")
    guess_entry.config(state=tk.NORMAL)
    canvas.delete("all")
    canvas.create_line(20, 280, 120, 280)
    canvas.create_line(70, 280, 70, 20)
    canvas.create_line(70, 20, 170, 20)
    canvas.create_line(170, 20, 170, 50)
    retry_button.grid_forget()
    exit_button.grid_forget()

def exit_game():
    root.destroy()

retry_button = tk.Button(root, text="Retry", command=retry_game)

exit_button = tk.Button(root, text="Exit", command=exit_game)

root.bind("<Return>", lambda event: check_guess())

root.mainloop()