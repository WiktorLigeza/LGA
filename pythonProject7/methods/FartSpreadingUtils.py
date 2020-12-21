from tkinter.simpledialog import askstring
import tkinter as tk

def increaseBallSpeed(self):
    if self.sleepTime <= 10:
        self.sleepTime = 10
    else:
        self.sleepTime -= 10


def add(self):  # Add a new ball
    pass


def setWalls(self):
    pass


def remove(self):
    num = askstring('number', 'how many?')
    num = int(num)
    for i in range(num):
        self.ballList.remove(self.ballList[i])
