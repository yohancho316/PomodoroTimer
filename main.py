import tkinter as tk
from tkinter import ttk

class PomodoroTimer(tk.Tk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.title("John's Pomodoro Study Timer")
    self.columnconfigure(0,weight=1)
    self.rowconfigure(0,weight=1)

    container = ttk.Frame(self)
    container.grid()
    container.columnconfigure(0,weight=1)

    timer_frame = Timer(container)
    timer_frame.grid(row=0,column=0,stikcy='NSEW')

class Timer(ttk.Frame):
  def __init__(self,parent):
    super().__init__(parent)

  def decrement_time(self):
    pass
