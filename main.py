import tkinter as tk
from tkinter import ttk
from typing import Text
from collections import deque

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
    timer_frame.grid(row=0,column=0,sticky='NSEW')

class Timer(ttk.Frame):
  def __init__(self,parent):
    super().__init__(parent)

    self.current_time = tk.StringVar(value='00:10')
    self.timer_order = ['Pomodoro', 'Short Break', 'Pomodoro', 'Short Break', 'Pomodoro', 'Long Break']
    self.timer_schedule = deque(self.timer_order)
    self.timer_running = True

    timer_frame = ttk.Frame(self,height='100')
    timer_frame.grid(pady=(10,0),sticky='NSEW')

    timer_counter = ttk.Label(timer_frame,textvariable=self.current_time)
    timer_counter.grid()

    self.decrement_time()

  def decrement_time(self):
    current_time = self.current_time.get()

    if self.timer_running and current_time != "00:00":
      minutes, seconds = current_time.split(':')
      if int(seconds) > 0:
        seconds = int(seconds) - 1
        minutes = int(minutes)
      else:
        seconds = 59
        minutes = int(minutes) - 1

      self.current_time.set(f"{minutes:02d}:{seconds:02d}")
      self.after(1000, self.decrement_time)
    elif self.timer_running and current_time == '00:00':
      self.timer_schedule.rotate(-1)
      next_up = self.timer_schedule[0]
      if next_up == 'Pomodoro':
        self.current_time.set('25:00')
      elif next_up == 'Short Break':
        self.current_time.set('05:00')
      elif next_up == 'Long Break':
        self.current_time.set('15:00')
      self.after(1000,self.decrement_time)

timer = PomodoroTimer()
timer.mainloop()
