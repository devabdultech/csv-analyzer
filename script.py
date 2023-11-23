import csv
import tkinter as tk


def time_to_rows(timestamp):
    return (int(timestamp[0:2]) * 60 + int(timestamp[3:5])) * 250


def find_largest_value(file_path, start_time, end_time, column_index):
    largest_value = float('-inf')
    start_row = time_to_rows(start_time)
    end_row = time_to_rows(end_time)
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            if start_row <= index <= end_row:
                try:
                    value = float(row[column_index])
                    if value > largest_value:
                        largest_value = value
                except ValueError:
                    print(
                        f"Skipping invalid value at row {index + 1}, column {column_index + 1}")

    if largest_value == float('-inf'):
        return None
    return largest_value


def calculate_average_largest(file_path, intervals):
    largest_values = []
    for interval in intervals:
        start_time, end_time = interval
        largest_value = find_largest_value(file_path, start_time, end_time, 0)
        if largest_value is not None:
            largest_values.append(largest_value)
    if not largest_values:
        return None
    return sum(largest_values) / len(largest_values)
