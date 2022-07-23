import tkinter as tk
from tkinter import messagebox
import time

SET_TIME = 7
time_limit = SET_TIME
timer = None
reps = 0
starting_time = 0
cpm = 0.0
wpm = 0.0
result = {}

with open("text.txt") as file:
    data = file.readline()

def wpm_counter():
    global time_limit, starting_time, reps, result
    # Countdown timer:
    time_limit -= 1
    countdown_timer.config(text=f"Timer: {time_limit}")

    # Elapsed time:
    current_time = time.time()
    elapsed_time = current_time - starting_time

    # Number of characters:
    input_text = text.get("1.0", "end-1c")
    text_length = len(input_text)
    cpm = text_length / elapsed_time * 60
    char_per_min.config(text=f"CPM: {cpm:.4}")

    # Number of words:
    words = input_text.split()
    word_number = len(words)
    wpm = word_number / elapsed_time * 60
    word_per_min.config(text=f"WPM: {wpm:.4}")

    reps += 1
    result = {
        "wpm": wpm,
        "cpm": cpm,
    }
    return result


def counter():
    global reps, time_limit, starting_time, wpm, cpm, timer, result
    if reps == 0:
        text.configure(state="normal")
        text.focus()
        starting_time = time.time()
        reps += 1
    elif reps == SET_TIME:
        result = wpm_counter()
        text.configure(state="disabled")
        countdown_timer.config(text=f"Timer: {time_limit}")

    elif reps == SET_TIME + 1:
        messagebox.showinfo(title="The test is over!",
                            message=f"Well done!\nCharacters per minute: {result['cpm']:.4}\nWords per minute: {result['wpm']:.4}")
        # Stopping the loop:
        return True
    else:
        result = wpm_counter()
    timer = window.after(1000, counter)


def reset():
    global time_limit, timer, word_per_min, char_per_min, reps
    time_limit = SET_TIME
    countdown_timer.config(text=f"Timer: {time_limit}")
    text.configure(state="normal")
    text.delete("1.0", tk.END)
    text.configure(state="disabled")
    char_per_min.config(text="CPM: 0")
    word_per_min.config(text="WPM: 0")
    reps = 0


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.config(padx=25, pady=25)
window.title("Peter's Typing Speed Test")

sample = tk.Label(text="Sample text:")
text_to_type = tk.Text(height=20, width=52, wrap=tk.WORD)
text_to_type.insert(tk.END, data)
type_here = tk.Label(text="Type here:")
text = tk.Text(height=10, width=52, wrap=tk.WORD)
countdown_timer = tk.Label(text=f"Timer: {time_limit}")
char_per_min = tk.Label(text="CPM: 0")
word_per_min = tk.Label(text="WPM: 0")
start = tk.Button(text="Start", command=counter)
reset = tk.Button(text="Reset", command=reset)

sample.pack()
text_to_type.pack()
type_here.pack()
text.pack()
countdown_timer.pack()
char_per_min.pack()
word_per_min.pack()
start.pack()
reset.pack()

window.mainloop()
