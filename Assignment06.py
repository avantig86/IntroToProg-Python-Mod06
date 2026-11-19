# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Avanti Gulhane,11/19/2026,Added functions and classes
# ------------------------------------------------------------------------------------------ #
import json

# Define the data constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course
    2. Show current data
    3. Save data to a file
    4. Exit the program
-----------------------------------------
'''
FILE_NAME: str = "Enrollments.json"

# Define the data variables
students: list = []
menu_choice: str = ''


class IO:
    """Handles user input, output, and error messages."""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Display a friendly message and optional technical error details."""
        print(message)
        if error is not None:
            print("-- Technical Error Message --")
            print(error.__doc__)
            print(str(error))

    @staticmethod
    def output_menu(menu: str):
        """Display the course registration menu."""
        print(menu)

    @staticmethod
    def input_menu_choice():
        """Prompt the user for a menu choice and return it."""
        return input("What would you like to do: ")

    @staticmethod
    def output_student_courses(student_data: list):
        """Display each student registration as comma-separated values."""
        print("-" * 50)
        for student in student_data:
            print(f'{student["FirstName"]}, {student["LastName"]}, {student["CourseName"]}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """Collect and validate a registration, then return the updated list."""
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should contain only letters.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should contain only letters.")
            course_name = input("Please enter the name of the course: ")
            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(str(e), e)
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with your entered data.", e)
        return student_data


class FileProcessor:
    """Handles reading and writing student registrations in a JSON file."""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """Read registrations from a JSON file and return the list."""
        file = None
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
        except Exception as e:
            IO.output_error_messages("Error: Please check that the file exists and is in JSON format.", e)
        finally:
            if file is not None and not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Write registrations to a JSON file and return whether saving succeeded."""
        file = None
        try:
            file = open(file_name, "w")
            json.dump(student_data, file, indent=2)
            return True
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with writing to the file.", e)
            return False
        finally:
            if file is not None and not file.closed:
                file.close()


# Main program: load data and process menu choices
if __name__ == "__main__":
    students = FileProcessor.read_data_from_file(FILE_NAME, students)

    while True:
        IO.output_menu(MENU)
        menu_choice = IO.input_menu_choice()

        if menu_choice == "1":
            students = IO.input_student_data(students)
        elif menu_choice == "2":
            IO.output_student_courses(students)
        elif menu_choice == "3":
            if FileProcessor.write_data_to_file(FILE_NAME, students):
                print("The following data was saved to file!")
                IO.output_student_courses(students)
        elif menu_choice == "4":
            break
        else:
            IO.output_error_messages("Please only choose option 1, 2, 3, or 4.")

    print("Program Ended")
