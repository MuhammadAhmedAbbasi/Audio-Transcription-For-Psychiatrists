from collections import defaultdict

class StudentInfo:
    """
    A class to manage student information and database records.

    Attributes:
        student_id_info (str): A string to store the student ID information.
        database_data_saved (defaultdict): A dictionary to store student data, with 
        keys as student identifiers and values as dictionaries of student information.
    """
    def __init__(self):
        self.id = ""
        self.data = defaultdict(dict)
