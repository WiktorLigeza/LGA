
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np
from methods import engine, FartSpreadingUtils
from tkinter.simpledialog import askstring

class FartSpreading:
    def __init__(self, master):

        self.img_matrix = np.zeros([450, 450, 3], dtype=np.uint8)
        self.state_matrix = np.zeros([450, 450, 5], dtype=np.uint8)

        num = askstring('threshold', 'set threshold')
        try: self.threshold = int(num)
        except: self.threshold = 60
        self.img_matrix, self.state_matrix, b = engine.set_grid(self.img_matrix, self.state_matrix, self.threshold)

        master.title("LGA (number of elements: {})".format(b))
        self.master = master

        self.frame = tk.Frame(self.master, background="black")


        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.img_matrix))

        self.canvas = tk.Canvas(self.frame, width=450, height=450)
        self.canvas.pack(fill="y")
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        self.frame.pack()


        # buttons
        # buttonStop = tk.Button(self.frame, text="Stop", command=self.stop)
        # buttonStop.pack(side=tk.LEFT)
        #
        # buttonResume = tk.Button(self.frame, text="Resume", command=self.resume)
        # buttonResume.pack(side=tk.LEFT)
        #
        # buttonFaster = tk.Button(self.frame, text="Faster", command=self.increaseBallSpeed)
        # buttonFaster.pack(side=tk.LEFT)
        #
        # buttonSlower = tk.Button(self.frame, text="Slower", command=self.decreaseBallSpeed)
        # buttonSlower.pack(side=tk.LEFT)
        #
        # buttonAdd = tk.Button(self.frame, text="Add", command=self.add)
        # buttonAdd.pack(side=tk.LEFT)
        #
        # buttonRemove = tk.Button(self.frame, text="Remove", command=self.remove)
        # buttonRemove.pack(side=tk.LEFT)

        self.sleepTime = 50
        self.isStopped = False
        self.animate()
        master.mainloop()

    # calls
    def stop(self):  # Stop animation
        self.isStopped = True

    def resume(self):  # Resume animation
        self.isStopped = False

    def animate(self):  # Animate ball movements
        if self.isStopped == False:
             self.master.after(self.sleepTime, lambda: engine.set_sim(self.canvas, self.img_matrix, self.state_matrix, self.master,
                                                      self.frame))


    def add(self):  # Add a new ball
        FartSpreadingUtils.add(self)

    def remove(self):
        FartSpreadingUtils.remove(self)

    def increaseBallSpeed(self):
        FartSpreadingUtils.increaseBallSpeed(self)

    def decreaseBallSpeed(self):
        self.sleepTime += 10





if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    FartSpreading(tk.Toplevel(root))