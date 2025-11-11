#Title- GradeBook Analyzer
#Name- Vaishali Doonga
#Date- 11-11-2025

import csv
import os

def display_menu():
    """Displays the main menu for user choice."""
    print("\nWelcome to the Gradebook Analyzer!")
    print("Choose an option:")
    print("1.Manual entry of student names and marks")
    print("2.Load data from a CSV file")
    print("3.Exit")

def get_manual_data():
    """Allows manual entry of student data."""
    marks = {}
    num_students = int(input("Enter the number of students: "))
    for i in range(num_students):
        name = input("Enter student name: ")
        mark = float(input(f"Enter mark for {name}: "))
        marks[name] = mark
    return marks

def load_csv_data(filename):
    """Loads student data from a CSV file."""
    marks = {}
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader, None)  
        for row in reader:
            if len(row) >= 2:
                name, mark = row[0], float(row[1])
                marks[name] = mark
    return marks

def calculate_average(marks_dict):
    """Calculates the average of the marks."""
    if not marks_dict:
        return 0
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    """Calculates the median of the marks."""
    if not marks_dict:
        return 0
    sorted_marks = sorted(marks_dict.values())
    n = len(sorted_marks)
    if n % 2 == 0:
        return (sorted_marks[n//2 - 1] + sorted_marks[n//2]) / 2
    else:
        return sorted_marks[n//2]

def find_max_score(marks_dict):
    """Finds the maximum score."""
    if not marks_dict:
        return 0
    return max(marks_dict.values())

def find_min_score(marks_dict):
    """Finds the minimum score."""
    if not marks_dict:
        return 0
    return min(marks_dict.values())

def assign_grades(marks_dict):
    """Assigns letter grades based on marks."""
    grades = {}
    for name, mark in marks_dict.items():
        if mark >= 90:
            grades[name] = 'A'
        elif mark >= 80:
            grades[name] = 'B'
        elif mark >= 70:
            grades[name] = 'C'
        elif mark >= 60:
            grades[name] = 'D'
        else:
            grades[name] = 'F'
    return grades

def grade_distribution(grades_dict):
    """Counts the number of students per grade."""
    distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for grade in grades_dict.values():
        distribution[grade] += 1
    return distribution

def pass_fail_filter(marks_dict):
    """Filters students into passed and failed lists using list comprehension."""
    passed_students = [name for name, mark in marks_dict.items() if mark >= 40]
    failed_students = [name for name, mark in marks_dict.items() if mark < 40]
    return passed_students, failed_students

def print_analysis_summary(marks_dict, grades_dict, distribution, passed, failed):
    """Prints the statistical analysis summary."""
    print("\n--- Statistical Analysis ---")
    print(f"Average Score: {calculate_average(marks_dict):.2f}")
    print(f"Median Score: {calculate_median(marks_dict):.2f}")
    print(f"Max Score: {find_max_score(marks_dict):.2f}")
    print(f"Min Score: {find_min_score(marks_dict):.2f}")
    print("\n--- Grade Distribution ---")
    for grade, count in distribution.items():
        print(f"{grade}: {count} students")
    print(f"\nPassed Students ({len(passed)}): {', '.join(passed)}")
    print(f"Failed Students ({len(failed)}): {', '.join(failed)}")

def print_results_table(marks_dict, grades_dict):
    """Prints a formatted table of names, marks, and grades."""
    print("\n--- Results Table ---")
    print(f"{'Name':<15} {'Marks':<10} {'Grade':<5}")
    print("-" * 30)
    for name in marks_dict:
        print(f"{name:<15} {marks_dict[name]:<10.2f} {grades_dict[name]:<5}")

def export_to_csv(marks_dict, grades_dict, filename="gradebook_output.csv"):
    """Exports the results to a CSV file (bonus feature)."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Marks", "Grade"])
        for name in marks_dict:
            writer.writerow([name, marks_dict[name], grades_dict[name]])
    print(f"Results exported to {filename}")

def main():
    """Main function to run the gradebook analyzer."""
    while True:
        display_menu()
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            marks = get_manual_data()
        elif choice == '2':
            filename = input("Enter CSV filename (e.g., students.csv): ").strip()
            marks = load_csv_data(filename)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
            continue
        
        if not marks:
            print("No data loaded. Please try again.")
            continue
        
        
        grades = assign_grades(marks)
        distribution = grade_distribution(grades)
        passed, failed = pass_fail_filter(marks)
        
        
        print_analysis_summary(marks, grades, distribution, passed, failed)
        print_results_table(marks, grades)
        
        
        export_choice = input("Do you want to export results to CSV? (y/n): ").strip().lower()
        if export_choice == 'y':
            export_to_csv(marks, grades)
        
        
        repeat = input("Do you want to perform another analysis? (y/n): ").strip().lower()
        if repeat != 'y':
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()
