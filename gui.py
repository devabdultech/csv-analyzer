from tkinter import filedialog
import ttkbootstrap as ttk
from script import calculate_average_largest, time_to_rows, find_largest_value


class IntervalEntry:
    def __init__(self, master, row, label_text):
        self.label = ttk.Label(master, text=label_text + ":",
                               anchor='e')
        self.label.grid(row=row, column=0, sticky='e', pady=(10, 5))

        self.start_label = ttk.Label(
            master, text="Start:", anchor='e')
        self.start_label.grid(row=row, column=1, sticky='e')

        self.start_entry = ttk.Entry(master)
        self.start_entry.grid(row=row, column=2, sticky='we')

        self.end_label = ttk.Label(
            master, text="End:", anchor='e')
        self.end_label.grid(row=row, column=3, sticky='e')

        self.end_entry = ttk.Entry(master)
        self.end_entry.grid(row=row, column=4, sticky='we')


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_file_path.delete(0, ttk.END)
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
        result_label.configure(
            text="Error: Please select a CSV file.")
        style = ttk.Style()
        style.configure("Error.TLabel", font=("Inter", 14), foreground="red")
        result_label.config(style="Error.TLabel")
        return

    largest_values = []
    for i, (start_time, end_time) in enumerate(intervals, start=1):
        if not start_time or not end_time:
            result_label.configure(
                text=f"Error: Interval {i} is incomplete.")
            style = ttk.Style()
            style.configure("Error.TLabel", font=(
                "Inter", 14), foreground="red")
            result_label.config(style="Error.TLabel")
            return
        try:
            time_to_rows(start_time)
            time_to_rows(end_time)
            largest_value = find_largest_value(
                file_path, start_time, end_time, 0)
            largest_values.append(largest_value)
        except ValueError:
            result_label.configure(
                text=f"Error: Invalid format in Interval {i}.")
            style = ttk.Style()
            style.configure("Error.TLabel", font=(
                "Inter", 14), foreground="red")
            result_label.config(style="Error.TLabel")
            return

    # Display individual largest values
    if all(value is not None for value in largest_values):
        label_interval1.configure(
            text=f"Interval 1: {largest_values[0]:.2f}")
        label_interval2.configure(
            text=f"Interval 2: {largest_values[1]:.2f}")
        label_interval3.configure(
            text=f"Interval 3: {largest_values[2]:.2f}")

    # Calculate average largest value
    average_largest = calculate_average_largest(file_path, intervals)
    if average_largest is not None:
        result_label.configure(
            text=f"Average of 3 Largest Values: {average_largest:.2f}")
        style = ttk.Style()
        style.configure("Success.TLabel", font=(
            "Inter", 14), foreground="green")
        result_label.config(style="Success.TLabel")
    else:
        result_label.configure(
            text="Error: No valid values found in the specified intervals.")
        style = ttk.Style()
        style.configure("Error.TLabel", font=("Inter", 14), foreground="red")
        result_label.config(style="Error.TLabel")


if __name__ == "__main__":
    root = ttk.Window(themename="solar", resizable=[False, False])
    root.geometry("800x500")
    root.title("CSV Data Analyzer")

    # Title
    title_label = ttk.Label(root, text="CSV Data Analyzer", font=(
        "Inter", 20), padding=(0, 20), justify='center')
    title_label.grid(row=0, column=0, columnspan=20)

    # Filepath
    label_file_path = ttk.Label(
        root, text="Select CSV File:", anchor='e')
    label_file_path.grid(row=1, column=0, pady=(10, 5), sticky='e')

    entry_file_path = ttk.Entry(root)
    entry_file_path.grid(row=1, column=1, columnspan=12, sticky='we')

    button_browse = ttk.Button(
        root, text="Select File", command=browse_file, cursor="hand2")
    button_browse.grid(row=1, column=13, sticky='w')

    # Intervals
    label_intervals = ttk.Label(
        root, text="Enter 3 Intervals (XX:XX - XX:XX):")
    label_intervals.grid(row=2, column=0, columnspan=5, pady=(10, 5))

    # Creating IntervalEntry instances
    interval1 = IntervalEntry(root, 3, "Interval 1")
    interval2 = IntervalEntry(root, 4, "Interval 2")
    interval3 = IntervalEntry(root, 5, "Interval 3")

    # Result
    result_label = ttk.Label(root, text="", font=("Inter", 14))
    result_label.grid(row=6, column=0, columnspan=5, pady=(20, 10))

    # Individual largest values labels
    label_interval1 = ttk.Label(root, text="", font=("Inter", 12))
    label_interval1.grid(row=7, column=2, pady=(20, 10))

    label_interval2 = ttk.Label(root, text="", font=("Inter", 12))
    label_interval2.grid(row=7, column=3, pady=(20, 10))

    label_interval3 = ttk.Label(root, text="", font=("Inter", 12))
    label_interval3.grid(row=7, column=4, pady=(20, 10))

    # Calculate button
    button_calculate = ttk.Button(
        root, text="Calculate", command=calculate_and_display, cursor="hand2")
    button_calculate.grid(row=8, column=0, columnspan=5, pady=(0, 14))

    # Center all widgets
    for child in root.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Center the window
    root.eval('tk::PlaceWindow . center')

    root.mainloop()
