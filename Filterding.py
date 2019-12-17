from tkinter import *
from tkinter import filedialog


class MainGUI:

    def __init__(self):
        window = Tk()
        window.title("Filterding")
        window.geometry("700x400")

        file = filedialog.askopenfilename(title="Select a file.")

        exit_button = Button(window, text="Exit",
                             command=lambda: window.quit())
        exit_button.grid(column=0, row=0)

        window.mainloop()


def main():

    gui = MainGUI()


main()