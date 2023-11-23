import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from script import calculate_average_largest, time_to_rows


class IntervalEntry:
    def __init__(self, master, row, label_text):
        self.label = tk.Label(master, text=label_text, font=("Inter", 12))
        self.label.grid(row=row, column=0, pady=5)

        self.start_entry = tk.Entry(master, font=("Inter", 12))
        self.start_entry.grid(row=row, column=1, pady=5)

        self.end_label = tk.Label(
            master, text=f"{label_text} End Time:", font=("Inter", 12))
        self.end_label.grid(row=row, column=2, pady=5)

        self.end_entry = tk.Entry(master, font=("Inter", 12))
        self.end_entry.grid(row=row, column=3, pady=5)


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)


def calculate_and_display():
    file_path = entry_file_path.get()

    # Intervals
    intervals = [
        (interval1.start_entry.get(), interval1.end_entry.get()),
        (interval2.start_entry.get(), interval2.end_entry.get()),
        (interval3.start_entry.get(), interval3.end_entry.get())
    ]

    # Check for missing file
    if not file_path:
        result_label.config(text="Error: Please select a CSV file.", fg="red")
        return

    # Check for missing or invalid intervals
    for i, (start_time, end_time) in enumerate(intervals, start=1):
        if not start_time or not end_time:
            result_label.config(
                text=f"Error: Interval {i} is incomplete.", fg="red")
            return
        try:
            time_to_rows(start_time)
            time_to_rows(end_time)
        except ValueError:
            result_label.config(
                text=f"Error: Invalid format in Interval {i}.", fg="red")
            return

    # Calculate average largest value
    average_largest = calculate_average_largest(file_path, intervals)
    if average_largest is not None:
        result_label.config(
            text=f"Average of 3 Largest Values: {average_largest:.2f}", fg="green")
    else:
        result_label.config(
            text="Error: No valid values found in the specified intervals.", fg="red")


root = ttk.Window()
root.geometry("800x500")
root.title("CSV Data Analyzer")

# Title
title_label = tk.Label(root, text="CSV Data Analyzer", font=("Inter", 18))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Filepath
label_file_path = tk.Label(root, text="Select CSV File:", font=("Inter", 12))
label_file_path.grid(row=1, column=0, padx=10, pady=5)

entry_file_path = tk.Entry(root, font=("Inter", 12))
entry_file_path.grid(row=1, column=1, pady=5, columnspan=2, sticky='we')

button_browse = tk.Button(
    root, text="Browse", command=browse_file, font=("Inter", 12))
button_browse.grid(row=1, column=3, pady=5, padx=(10, 0))  # \


# Intervals
label_intervals = tk.Label(
    root, text="Enter 3 Intervals (XX:XX - XX:XX):", font=("Inter", 18, "bold", "underline"))
label_intervals.grid(row=2, column=0, pady=(10, 5), columnspan=6, sticky="n")


# Creating IntervalEntry instances
interval1 = IntervalEntry(root, 3, "Interval 1")
interval2 = IntervalEntry(root, 4, "Interval 2")
interval3 = IntervalEntry(root, 5, "Interval 3")

# Result
result_label = tk.Label(root, text="", font=("Inter", 12))
result_label.grid(row=6, column=0, columnspan=4, pady=10)

# Calculate button
button_calculate = tk.Button(
    root, text="Calculate", command=calculate_and_display, font=("Inter", 15))
button_calculate.grid(row=7, column=0, columnspan=4, pady=14)

# Center the window
root.eval('tk::PlaceWindow . center')

root.mainloop()
