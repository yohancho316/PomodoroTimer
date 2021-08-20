import tkinter as tk
from tkinter import ttk
from typing import Text
from collections import deque

class PomodoroTimer(tk.Tk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.title("John's Pomodoro Study Timer")
    self.columnconfigure(0,weight=1)
    self.rowconfigure(1,weight=1)
    #self.geometry('380x210')
    self.resizable(True,True)

    # Pomodoro Class Variables
    self.pomodoro = tk.StringVar(value = 25)
    self.long_break = tk.StringVar(value = 15)
    self.short_break = tk.StringVar(value = 5)
    self.timer_order = ['Pomodoro', 'Short Break', 'Pomodoro', 'Short Break', 'Pomodoro', 'Long Break']
    self.timer_schedule = deque(self.timer_order)

    container = ttk.Frame(self)
    container.grid()
    container.columnconfigure(0,weight=1)

    self.frames = dict()

    # Timer Frame
    timer_frame = Timer(container,self,lambda:self.show_frame(Settings))
    timer_frame.grid(row=0,column=0,sticky='NSEW')

    # Settings Frame
    settings_frame = Settings(container,self,lambda:self.show_frame(Timer))
    settings_frame.grid(row=0,column=0,sticky='NSEW')

    # Insert KVP into frames Dict
    # Key: timer_frame / settings_frame class
    # Value: timer_frame / settings_frame objects
    self.frames[Timer] = timer_frame
    self.frames[Settings] = settings_frame

    self.show_frame(Timer)

  def show_frame(self,container):
    frame = self.frames[container]
    frame.tkraise()

# Settings Frame Class
class Settings(ttk.Frame):
  def __init__(self,parent,controller,show_timer):
    super().__init__(parent)

    # Frame Widgets
    settings_container = ttk.Frame(self,padding='30 15 30 15',)
    settings_container.grid(row=0,column=0,padx=10,pady=10,sticky='EW')
    settings_container.columnconfigure(0,weight=1)
    settings_container.rowconfigure(2,weight=1)

    # Label Widgets
    pomodoro_label = ttk.Label(settings_container,text='Pomodoro: ')
    long_break_label = ttk.Label(settings_container,text='Long Break Time: ')
    short_break_label = ttk.Label(settings_container,text='Short Break Time: ')

    pomodoro_label.grid(row=0,column=0,sticky='W')
    long_break_label.grid(row=1,column=0,sticky='W')
    short_break_label.grid(row=2,column=0,sticky='W')

    # Spinbox Input Widgets
    pomodoro_input = tk.Spinbox(settings_container,from_=0,to=120,increment=1,justify='center',textvariable=controller.pomodoro,width=10,)
    long_break_input = tk.Spinbox(settings_container,from_=0,to=60,increment=1,justify='center',textvariable=controller.long_break,width=10,)
    short_break_input = tk.Spinbox(settings_container,from_=0,to=30,increment=1,justify='center',textvariable=controller.short_break,width=10,)

    pomodoro_input.grid(row=0,column=1,sticky='EW')
    long_break_input.grid(row=1,column=1,sticky='EW')
    short_break_input.grid(row=2,column=1,sticky='EW')
    pomodoro_input.focus()

    # Padding Configuration
    for child in settings_container.winfo_children():
      child.grid_configure(padx=5,pady=5)

    button_container = ttk.Frame(self)
    button_container.grid(sticky='WE',padx=10)
    button_container.columnconfigure(0,weight=1)

    timer_button = ttk.Button(button_container,text='Back',command=show_timer,cursor='hand2')
    timer_button.grid(row=0,column=0,sticky='EW',padx=2)

# Timer Frame Class
class Timer(ttk.Frame):
  def __init__(self,parent,controller,show_settings):
    super().__init__(parent)

    # Timer Class Variables
    self.controller = controller
    pomodoro_time = int(controller.pomodoro.get())
    self.current_time = tk.StringVar(value=f'{pomodoro_time:02d}:00')
    self.timer_running = False
    self._timer_decrement_job = None
    self.current_timer_label = tk.StringVar(value=controller.timer_schedule[0])

    timer_description_label = ttk.Label(self,textvariable=self.current_timer_label)
    timer_description_label.grid(row=0,column=0,padx=(10,0),pady=(10,0),sticky='W')

    settings_button = ttk.Button(self,text='Settings',command=show_settings,cursor='hand2')
    settings_button.grid(row=0,column=1,sticky='E',padx=10,pady=(10,0))

    timer_frame = ttk.Frame(self,height='100')
    timer_frame.grid(row=1,column=0,columnspan=2,pady=(10,0),sticky='NSEW')

    timer_counter = ttk.Label(timer_frame,textvariable=self.current_time)
    timer_counter.place(relx=0.5,rely=0.5,anchor='center')

    button_container = ttk.Frame(self,padding=10)
    button_container.grid(row=2,column=0,columnspan=2,sticky='EW')
    button_container.columnconfigure((0,1,2),weight=1)

    self.start_button = ttk.Button(button_container,text='Start',state='enable',command=self.start_timer,cursor='hand2')
    self.start_button.grid(row=0,column=0,sticky='EW')

    self.stop_button = ttk.Button(button_container,text='Stop',state='disabled',command=self.stop_timer,cursor='hand2')
    self.stop_button.grid(row=0,column=1,sticky='EW')

    reset_button = ttk.Button(button_container,text='Reset',command=self.reset_timer,cursor='hand2')
    reset_button.grid(row=0,column=2,sticky='EW')

    self.decrement_time()

  # Start Timer Method
  def start_timer(self):
    self.timer_running = True
    self.start_button['state'] = 'disabled'
    self.stop_button['state'] = 'enabled'
    self.decrement_time()

  # Stop Timer Method
  def stop_timer(self):
    self.timer_running = False
    self.start_button['state'] = 'enabled'
    self.stop_button['state'] = 'disabled'
    if self._timer_decrement_job:
      self.after_cancel(self._timer_decrement_job)
      self._timer_decrement_job = None

  # Reset Timer Method
  def reset_timer(self):
    self.stop_timer()
    pomodoro_time = int(self.controller.pomodoro.get())
    self.current_time.set(f'{pomodoro_time:02d}:00')
    self.controller._timer_decrement_job = deque(self.controller.timer_order)
    self.current_timer_label.set(self.controller.timer_schedule[0])

  # Decrement Timer Method
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
      self._timer_decrement_job = self.after(1000, self.decrement_time)
    elif self.timer_running and current_time == '00:00':
      self.controller.timer_schedule.rotate(-1)
      next_up = self.controller.timer_schedule[0]
      self.current_timer_label.set(next_up)
      if next_up == 'Pomodoro':
        pomodoro_time = int(self.controller.pomodoro.get())
        self.current_time.set(f"{pomodoro_time:02d}:00")
      elif next_up == 'Short Break':
        short_break_time = int(self.controller.short_break.get())
        self.current_time.set(f"{short_break_time:02d}:00")
      elif next_up == 'Long Break':
        long_break_time = int(self.controller.long_break.get())
        self.current_time.set(f"{long_break_time:02d}:00")
      self._timer_decrement_job = self.after(1000,self.decrement_time)

timer = PomodoroTimer()
timer.mainloop()
