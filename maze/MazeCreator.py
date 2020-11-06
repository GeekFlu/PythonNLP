from tkinter import *


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Maze Creator Ver 1.0")
        self.pack(fill=BOTH, expand=1)
        quitBtn = Button(self, text="Quit", fg="red", command=quit)
        quitBtn.place(x=0, y=0)


# For installing tkinter on Ubuntu run sudo apt install python3-tk
if __name__ == "__main__":
    root = Tk()
    root.geometry("400x300")
    app = Window(root)
    root.mainloop()
