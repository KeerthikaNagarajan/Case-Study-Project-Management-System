from abc import ABC, abstractmethod
from entity.employee import Employee
from entity.project import Project
from entity.task import Task

class IProjectRepository(ABC):
    @abstractmethod
    def create_employee(self, emp: Employee) -> bool: pass
    @abstractmethod
    def create_project(self, pj: Project) -> bool: pass
    @abstractmethod
    def create_task(self, task: Task) -> bool: pass
    @abstractmethod
    def assign_project_to_employee(self, project_id: int, employee_id: int) -> bool: pass
    @abstractmethod
    def assign_task_in_project_to_employee(self, task_id: int, project_id: int, employee_id: int) -> bool: pass
    @abstractmethod
    def delete_employee(self, employee_id: int) -> bool: pass
    @abstractmethod
    def delete_project(self, project_id: int) -> bool: pass
    @abstractmethod
    def get_all_tasks(self, emp_id: int, project_id: int) -> list: pass