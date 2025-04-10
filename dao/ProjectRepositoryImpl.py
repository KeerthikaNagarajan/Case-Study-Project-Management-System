import mysql.connector
from dao.IProjectRepository import IProjectRepository
from entity.employee import Employee
from entity.project import Project
from entity.task import Task
from exception.EmployeeNotFoundException import EmployeeNotFoundException
from exception.ProjectNotFoundException import ProjectNotFoundException
from util.DBConnUtil import DBConnUtil
from util.DBPropertyUtil import DBPropertyUtil


class ProjectRepositoryImpl(IProjectRepository):
    def __init__(self):
        self.connection_string = DBPropertyUtil.get_connection_string("db.properties")
        self.connection = DBConnUtil.get_connection(self.connection_string)

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def create_employee(self, emp: Employee) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Employee (name, designation, gender, salary, project_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            values = (emp.get_name(), emp.get_designation(), emp.get_gender(), emp.get_salary(), emp.get_project_id())
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def create_project(self, pj: Project) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Project (project_name, description, start_date, status)
            VALUES (%s, %s, %s, %s)
            """
            values = (pj.get_project_name(), pj.get_description(), pj.get_start_date(), pj.get_status())
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def create_task(self, task: Task) -> bool:
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Task (task_name, project_id, employee_id, status, allocation_date, deadline_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (task.get_task_name(), task.get_project_id(), task.get_employee_id(), task.get_status(),
                      task.get_allocation_date(), task.get_deadline_date())
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def assign_project_to_employee(self, project_id: int, employee_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM Project WHERE id = %s", (project_id,))
            if not cursor.fetchone():
                raise ProjectNotFoundException(f"Project with ID {project_id} not found")

            cursor.execute("SELECT id FROM Employee WHERE id = %s", (employee_id,))
            if not cursor.fetchone():
                raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found")

            query = "UPDATE Employee SET project_id = %s WHERE id = %s"
            cursor.execute(query, (project_id, employee_id))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def assign_task_in_project_to_employee(self, task_id: int, project_id: int, employee_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM Project WHERE id = %s", (project_id,))
            if not cursor.fetchone():
                raise ProjectNotFoundException(f"Project with ID {project_id} not found")

            cursor.execute("SELECT id FROM Employee WHERE id = %s", (employee_id,))
            if not cursor.fetchone():
                raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found")

            cursor.execute("SELECT task_id FROM Task WHERE task_id = %s", (task_id,))
            if not cursor.fetchone():
                raise Exception("Task not found")

            query = "UPDATE Task SET employee_id = %s WHERE task_id = %s AND project_id = %s"
            cursor.execute(query, (employee_id, task_id, project_id))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def delete_employee(self, employee_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM Employee WHERE id = %s", (employee_id,))
            if not cursor.fetchone():
                raise EmployeeNotFoundException(f"Employee with ID {employee_id} not found")

            cursor.execute("UPDATE Task SET employee_id = NULL WHERE employee_id = %s", (employee_id,))
            cursor.execute("DELETE FROM Employee WHERE id = %s", (employee_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def delete_project(self, project_id: int) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM Project WHERE id = %s", (project_id,))
            if not cursor.fetchone():
                raise ProjectNotFoundException(f"Project with ID {project_id} not found")

            cursor.execute("DELETE FROM Task WHERE project_id = %s", (project_id,))
            cursor.execute("UPDATE Employee SET project_id = NULL WHERE project_id = %s", (project_id,))
            cursor.execute("DELETE FROM Project WHERE id = %s", (project_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def get_all_tasks(self, emp_id: int, project_id: int) -> list:
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT id FROM Employee WHERE id = %s", (emp_id,))
            if not cursor.fetchone():
                raise EmployeeNotFoundException(f"Employee with ID {emp_id} not found")

            cursor.execute("SELECT id FROM Project WHERE id = %s", (project_id,))
            if not cursor.fetchone():
                raise ProjectNotFoundException(f"Project with ID {project_id} not found")

            query = """
            SELECT t.task_id, t.task_name, t.status, t.allocation_date, t.deadline_date
            FROM Task t
            WHERE t.employee_id = %s AND t.project_id = %s
            """
            cursor.execute(query, (emp_id, project_id))
            tasks = cursor.fetchall()
            return tasks
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []