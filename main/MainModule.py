from dao.ProjectRepositoryImpl import ProjectRepositoryImpl
from entity.employee import Employee
from entity.project import Project
from entity.task import Task
from exception.EmployeeNotFoundException import EmployeeNotFoundException
from exception.ProjectNotFoundException import ProjectNotFoundException


class MainModule:
    def __init__(self):
        self.repository = ProjectRepositoryImpl()

    def display_menu(self):
        while True:
            print("\nProject Management System (2025)")
            print("1. Add Employee")
            print("2. Add Project")
            print("3. Add Task")
            print("4. Assign project to employee")
            print("5. Assign task within a project to employee")
            print("6. Delete Employee")
            print("7. Delete Project")
            print("8. List all tasks assigned to an employee in a project")
            print("9. Show all employees")
            print("10. Show all projects")
            print("11. Show all tasks")
            print("12. Exit")

            choice = input("Enter your choice: ")

            try:
                if choice == '1':
                    self.add_employee()
                elif choice == '2':
                    self.add_project()
                elif choice == '3':
                    self.add_task()
                elif choice == '4':
                    self.assign_project_to_employee()
                elif choice == '5':
                    self.assign_task_in_project_to_employee()
                elif choice == '6':
                    self.delete_employee()
                elif choice == '7':
                    self.delete_project()
                elif choice == '8':
                    self.list_tasks_for_employee_in_project()
                elif choice == '9':
                    self.show_all_employees()
                elif choice == '10':
                    self.show_all_projects()
                elif choice == '11':
                    self.show_all_tasks()
                elif choice == '12':
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"Error: {str(e)}")

    def add_employee(self):
        print("\nAdd New Employee")
        name = input("Enter employee name: ")
        designation = input("Enter designation: ")
        gender = input("Enter gender (M/F/O): ")
        salary = float(input("Enter salary: "))
        project_id = input("Enter project ID (leave empty if none): ")

        emp = Employee(
            name=name,
            designation=designation,
            gender=gender,
            salary=salary,
            project_id=int(project_id) if project_id else None
        )

        if self.repository.create_employee(emp):
            print("Employee created successfully!")
        else:
            print("Failed to create employee.")

    def add_project(self):
        print("\nAdd New Project")
        project_name = input("Enter project name: ")
        description = input("Enter description: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        status = input("Enter status (started/dev/build/test/deployed): ")

        pj = Project(
            project_name=project_name,
            description=description,
            start_date=start_date,
            status=status
        )

        if self.repository.create_project(pj):
            print("Project created successfully!")
        else:
            print("Failed to create project.")

    def add_task(self):
        print("\nAdd New Task")
        task_name = input("Enter task name: ")
        project_id = int(input("Enter project ID: "))
        employee_id = input("Enter employee ID (leave empty if none): ")
        status = input("Enter status (Assigned/Started/Completed): ")
        allocation_date = input("Enter allocation date (YYYY-MM-DD): ")
        deadline_date = input("Enter deadline date (YYYY-MM-DD): ")

        task = Task(
            task_name=task_name,
            project_id=project_id,
            employee_id=int(employee_id) if employee_id else None,
            status=status,
            allocation_date=allocation_date,
            deadline_date=deadline_date
        )

        if self.repository.create_task(task):
            print("Task created successfully!")
        else:
            print("Failed to create task.")

    def assign_project_to_employee(self):
        print("\nAssign Project to Employee")
        project_id = int(input("Enter project ID: "))
        employee_id = int(input("Enter employee ID: "))

        try:
            if self.repository.assign_project_to_employee(project_id, employee_id):
                print("Project assigned successfully!")
        except EmployeeNotFoundException as e:
            print(f"Error: {str(e)}")
        except ProjectNotFoundException as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def assign_task_in_project_to_employee(self):
        print("\nAssign Task to Employee in Project")
        task_id = int(input("Enter task ID: "))
        project_id = int(input("Enter project ID: "))
        employee_id = int(input("Enter employee ID: "))

        try:
            if self.repository.assign_task_in_project_to_employee(task_id, project_id, employee_id):
                print("Task assigned successfully!")
        except EmployeeNotFoundException as e:
            print(f"Error: {str(e)}")
        except ProjectNotFoundException as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def delete_employee(self):
        print("\nDelete Employee")
        employee_id = int(input("Enter employee ID to delete: "))

        try:
            if self.repository.delete_employee(employee_id):
                print("Employee deleted successfully!")
        except EmployeeNotFoundException as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def delete_project(self):
        print("\nDelete Project")
        project_id = int(input("Enter project ID to delete: "))

        try:
            if self.repository.delete_project(project_id):
                print("Project deleted successfully!")
        except ProjectNotFoundException as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def list_tasks_for_employee_in_project(self):
        print("\nList Tasks for Employee in Project")
        employee_id = int(input("Enter employee ID: "))
        project_id = int(input("Enter project ID: "))

        try:
            tasks = self.repository.get_all_tasks(employee_id, project_id)
            if tasks:
                print("\nTasks assigned to employee in project:")
                for task in tasks:
                    print(f"Task ID: {task['task_id']}, Name: {task['task_name']}, Status: {task['status']}")
                    print(f"Allocation Date: {task['allocation_date']}, Deadline: {task['deadline_date']}")
                    print("-" * 40)
            else:
                print("No tasks found for this employee in the specified project.")
        except EmployeeNotFoundException as e:
            print(f"Error: {str(e)}")
        except ProjectNotFoundException as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def show_all_employees(self):
        try:
            cursor = self.repository.connection.cursor(dictionary=True)
            query = "SELECT * FROM Employee ORDER BY name"
            cursor.execute(query)
            employees = cursor.fetchall()

            if employees:
                print("\nAll Employees:")
                print("-" * 80)
                print(f"{'ID':<5}{'Name':<20}{'Designation':<20}{'Gender':<8}{'Salary':<10}{'Project ID':<10}")
                print("-" * 80)
                for emp in employees:
                    print(
                        f"{emp['id']:<5}{emp['name']:<20}{emp['designation']:<20}{emp['gender']:<8}{emp['salary']:<10}{emp['project_id'] or 'None':<10}")
            else:
                print("No employees found.")
        except Exception as e:
            print(f"Error retrieving employees: {str(e)}")
        finally:
            if cursor:
                cursor.close()

    def show_all_projects(self):
        try:
            cursor = self.repository.connection.cursor(dictionary=True)
            query = "SELECT * FROM Project ORDER BY start_date"
            cursor.execute(query)
            projects = cursor.fetchall()

            if projects:
                print("\nAll Projects (2025):")
                print("-" * 100)
                print(f"{'ID':<5}{'Name':<20}{'Description':<30}{'Start Date':<12}{'Status':<10}")
                print("-" * 100)
                for proj in projects:
                    print(
                        f"{proj['id']:<5}{proj['project_name']:<20}{proj['description'][:27] + '...':<30}{str(proj['start_date']):<12}{proj['status']:<10}")
            else:
                print("No projects found.")
        except Exception as e:
            print(f"Error retrieving projects: {str(e)}")
        finally:
            if cursor:
                cursor.close()

    def show_all_tasks(self):
        try:
            cursor = self.repository.connection.cursor(dictionary=True)
            query = """
            SELECT t.task_id, t.task_name, p.project_name, e.name as employee_name, 
                   t.status, t.allocation_date, t.deadline_date
            FROM Task t
            LEFT JOIN Project p ON t.project_id = p.id
            LEFT JOIN Employee e ON t.employee_id = e.id
            ORDER BY t.deadline_date
            """
            cursor.execute(query)
            tasks = cursor.fetchall()

            if tasks:
                print("\nAll Tasks:")
                print("-" * 120)
                print(
                    f"{'ID':<5}{'Task Name':<25}{'Project':<20}{'Assigned To':<20}{'Status':<12}{'Allocated':<12}{'Deadline':<12}")
                print("-" * 120)
                for task in tasks:
                    print(f"{task['task_id']:<5}{task['task_name']:<25}{task['project_name']:<20}"
                          f"{task['employee_name'] or 'Unassigned':<20}{task['status']:<12}"
                          f"{str(task['allocation_date']):<12}{str(task['deadline_date']):<12}")
            else:
                print("No tasks found.")
        except Exception as e:
            print(f"Error retrieving tasks: {str(e)}")
        finally:
            if cursor:
                cursor.close()


if __name__ == "__main__":
    app = MainModule()
    app.display_menu()