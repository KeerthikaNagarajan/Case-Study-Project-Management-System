class Employee:
    def __init__(self, id=None, name=None, designation=None, gender=None, salary=None, project_id=None):
        self.__id = id
        self.__name = name
        self.__designation = designation
        self.__gender = gender
        self.__salary = salary
        self.__project_id = project_id

    # Getters
    def get_id(self): return self.__id
    def get_name(self): return self.__name
    def get_designation(self): return self.__designation
    def get_gender(self): return self.__gender
    def get_salary(self): return self.__salary
    def get_project_id(self): return self.__project_id

    # Setters
    def set_id(self, id): self.__id = id
    def set_name(self, name): self.__name = name
    def set_designation(self, designation): self.__designation = designation
    def set_gender(self, gender): self.__gender = gender
    def set_salary(self, salary): self.__salary = salary
    def set_project_id(self, project_id): self.__project_id = project_id