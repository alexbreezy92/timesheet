import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class TimesheetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Timesheet Tracker")
        self.root.wm_attributes("-topmost", 1)
        self.root.resizable(False, False)  # Make window not resizable
        
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        self.setup_ui()
        
    def setup_ui(self):
        self.create_toolbar()
        self.create_header()
        self.create_main_frame()
        self.create_entries()
        self.create_totals()
        
    def create_toolbar(self):
        menubar = tk.Menu(self.root)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)
        
    def show_about(self):
        messagebox.showinfo("About", "This timesheet utility is used to calculate hours worked for the week as well as the daily totals. It updates whenever any box is updated.")
    
    def create_header(self):
        header_frame = tk.Frame(self.root, borderwidth=2, relief="ridge")
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        tk.Label(header_frame, text="Day", anchor="center").grid(row=0, column=0, padx=20, sticky="ew")
        tk.Label(header_frame, text="Start Time", anchor="center").grid(row=0, column=2, padx=20, sticky="ew")
        tk.Label(header_frame, text="End Time", anchor="center").grid(row=0, column=7, padx=80, sticky="ew")
        tk.Label(header_frame, text="Daily Total", anchor="center").grid(row=0, column=10, sticky="ew")
        
    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, borderwidth=2, relief="ridge")
        self.main_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
    def create_entries(self):
        self.start_hours = []
        self.start_minutes = []
        self.start_periods = []
        self.end_hours = []
        self.end_minutes = []
        self.end_periods = []
        self.daily_totals = []
        
        for i, day in enumerate(self.days):
            tk.Label(self.main_frame, text=day).grid(row=i, column=0, padx=5, sticky="w")
            
            start_hour = tk.Entry(self.main_frame, width=2)
            start_hour.grid(row=i, column=1, padx=5, sticky="ew")
            start_hour.bind("<FocusOut>", self.update_totals)
            self.start_hours.append(start_hour)
            
            tk.Label(self.main_frame, text=":").grid(row=i, column=2, padx=5, sticky="ew")
            
            start_minute = tk.Entry(self.main_frame, width=2)
            start_minute.grid(row=i, column=3, padx=5, sticky="ew")
            start_minute.bind("<FocusOut>", self.update_totals)
            self.start_minutes.append(start_minute)
            
            start_period = tk.StringVar(value="AM")
            start_period_menu = tk.OptionMenu(self.main_frame, start_period, "AM", "PM", command=lambda _: self.update_totals(None))
            start_period_menu.grid(row=i, column=4, padx=5, sticky="ew")
            self.start_periods.append(start_period)
            
            tk.Label(self.main_frame, text="").grid(row=i, column=5, padx=5)  # Additional spacing
            
            end_hour = tk.Entry(self.main_frame, width=2)
            end_hour.grid(row=i, column=6, padx=5, sticky="ew")
            end_hour.bind("<FocusOut>", self.update_totals)
            self.end_hours.append(end_hour)
            
            tk.Label(self.main_frame, text=":").grid(row=i, column=7, padx=5, sticky="ew")
            
            end_minute = tk.Entry(self.main_frame, width=2)
            end_minute.grid(row=i, column=8, padx=5, sticky="ew")
            end_minute.bind("<FocusOut>", self.update_totals)
            self.end_minutes.append(end_minute)
            
            end_period = tk.StringVar(value="PM")
            end_period_menu = tk.OptionMenu(self.main_frame, end_period, "AM", "PM", command=lambda _: self.update_totals(None))
            end_period_menu.grid(row=i, column=9, padx=5, sticky="ew")
            self.end_periods.append(end_period)
            
            daily_total = tk.Label(self.main_frame, text="0:00")
            daily_total.grid(row=i, column=10, padx=5, sticky="ew")
            self.daily_totals.append(daily_total)
    
    def create_totals(self):
        tk.Label(self.main_frame, text="Total hours:").grid(row=len(self.days), column=9, padx=5, sticky="w")
        self.total_hours_label = tk.Label(self.main_frame, text="0:00")
        self.total_hours_label.grid(row=len(self.days), column=10, padx=5, sticky="w")
    
    def update_totals(self, event):
        total_hours = timedelta()
        
        for i in range(len(self.days)):
            start_hour_str = self.start_hours[i].get()
            start_minute_str = self.start_minutes[i].get()
            start_period = self.start_periods[i].get()
            end_hour_str = self.end_hours[i].get()
            end_minute_str = self.end_minutes[i].get()
            end_period = self.end_periods[i].get()
            
            if start_hour_str and start_minute_str and end_hour_str and end_minute_str:
                try:
                    start_time_str = f"{start_hour_str}:{start_minute_str} {start_period}"
                    end_time_str = f"{end_hour_str}:{end_minute_str} {end_period}"
                    start_time = datetime.strptime(start_time_str, "%I:%M %p")
                    end_time = datetime.strptime(end_time_str, "%I:%M %p")
                    
                    if end_time < start_time:
                        end_time += timedelta(days=1)
                    
                    daily_total = end_time - start_time
                    total_hours += daily_total
                    
                    hours, remainder = divmod(daily_total.seconds, 3600)
                    minutes = remainder // 60
                    self.daily_totals[i].config(text=f"{hours}:{minutes:02d}")
                except ValueError:
                    self.daily_totals[i].config(text="Error")
            else:
                self.daily_totals[i].config(text="0:00")
        
        total_hours_hours = total_hours.days * 24 + total_hours.seconds // 3600
        total_hours_minutes = (total_hours.seconds % 3600) // 60
        self.total_hours_label.config(text=f"{total_hours_hours}:{total_hours_minutes:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimesheetTracker(root)
    root.mainloop()
