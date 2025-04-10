class Project:
    def __init__(self, id=None, project_name=None, description=None, start_date=None, status=None):
        self.__id = id
        self.__project_name = project_name
        self.__description = description
        self.__start_date = start_date
        self.__status = status

    # Getters
    def get_id(self): return self.__id
    def get_project_name(self): return self.__project_name
    def get_description(self): return self.__description
    def get_start_date(self): return self.__start_date
    def get_status(self): return self.__status

    # Setters
    def set_id(self, id): self.__id = id
    def set_project_name(self, project_name): self.__project_name = project_name
    def set_description(self, description): self.__description = description
    def set_start_date(self, start_date): self.__start_date = start_date
    def set_status(self, status): self.__status = status