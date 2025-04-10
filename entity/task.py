class Task:
    def __init__(self, task_id=None, task_name=None, project_id=None, employee_id=None, status=None, allocation_date=None, deadline_date=None):
        self.__task_id = task_id
        self.__task_name = task_name
        self.__project_id = project_id
        self.__employee_id = employee_id
        self.__status = status
        self.__allocation_date = allocation_date
        self.__deadline_date = deadline_date

    # Getters
    def get_task_id(self): return self.__task_id
    def get_task_name(self): return self.__task_name
    def get_project_id(self): return self.__project_id
    def get_employee_id(self): return self.__employee_id
    def get_status(self): return self.__status
    def get_allocation_date(self): return self.__allocation_date
    def get_deadline_date(self): return self.__deadline_date

    # Setters
    def set_task_id(self, task_id): self.__task_id = task_id
    def set_task_name(self, task_name): self.__task_name = task_name
    def set_project_id(self, project_id): self.__project_id = project_id
    def set_employee_id(self, employee_id): self.__employee_id = employee_id
    def set_status(self, status): self.__status = status
    def set_allocation_date(self, allocation_date): self.__allocation_date = allocation_date
    def set_deadline_date(self, deadline_date): self.__deadline_date = deadline_date