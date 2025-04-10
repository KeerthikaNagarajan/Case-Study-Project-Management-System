import unittest
from unittest.mock import MagicMock, patch
from entity.employee import Employee
from entity.project import Project
from entity.task import Task
from dao.ProjectRepositoryImpl import ProjectRepositoryImpl
from exception.EmployeeNotFoundException import EmployeeNotFoundException
from exception.ProjectNotFoundException import ProjectNotFoundException


class TestProjectManagementSystem(unittest.TestCase):

    def setUp(self):
        # Create a mock database connection for testing
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Patch the DBConnUtil to return our mock connection
        self.patcher = patch('dao.ProjectRepositoryImpl.DBConnUtil.get_connection')
        self.mock_get_connection = self.patcher.start()
        self.mock_get_connection.return_value = self.mock_connection

        # Create repository instance
        self.repository = ProjectRepositoryImpl()
        self.repository.connection = self.mock_connection

    def tearDown(self):
        self.patcher.stop()

    # Test Case 1: Test if employee is created successfully
    def test_create_employee_successfully(self):
        # Setup
        emp = Employee(
            name="Test Employee",
            designation="Developer",
            gender="M",
            salary=50000,
            project_id=1
        )

        # Mock database response
        self.mock_cursor.execute.return_value = None
        self.mock_connection.commit.return_value = None

        # Execute
        result = self.repository.create_employee(emp)

        # Assert
        self.assertTrue(result)
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()

    # Test Case 2: Test if task is created successfully
    def test_create_task_successfully(self):
        # Setup
        task = Task(
            task_name="Test Task",
            project_id=1,
            employee_id=1,
            status="Assigned",
            allocation_date="2025-01-01",
            deadline_date="2025-02-01"
        )

        # Mock database response
        self.mock_cursor.execute.return_value = None
        self.mock_connection.commit.return_value = None

        # Execute
        result = self.repository.create_task(task)

        # Assert
        self.assertTrue(result)
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()

    # Test Case 3: Test search for projects and tasks assigned to employee
    def test_get_all_tasks_for_employee_in_project(self):
        # Setup
        employee_id = 1
        project_id = 1

        # Mock database response
        mock_tasks = [
            {'task_id': 1, 'task_name': 'Task 1', 'status': 'Started',
             'allocation_date': '2025-01-01', 'deadline_date': '2025-02-01'},
            {'task_id': 2, 'task_name': 'Task 2', 'status': 'Assigned',
             'allocation_date': '2025-01-15', 'deadline_date': '2025-02-15'}
        ]
        self.mock_cursor.fetchall.return_value = mock_tasks

        # Execute
        result = self.repository.get_all_tasks(employee_id, project_id)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['task_name'], 'Task 1')
        self.assertEqual(result[1]['task_name'], 'Task 2')
        self.mock_cursor.execute.assert_called()

    # Test Case 4: Test if exceptions are thrown correctly
    def test_assign_project_to_nonexistent_employee_throws_exception(self):
        # Setup
        project_id = 1
        employee_id = 999  # Non-existent employee

        # Mock database response for employee check
        self.mock_cursor.fetchone.return_value = None

        # Execute and Assert
        with self.assertRaises(EmployeeNotFoundException):
            self.repository.assign_project_to_employee(project_id, employee_id)

    def test_assign_task_to_nonexistent_project_throws_exception(self):
        # Setup
        task_id = 1
        project_id = 999  # Non-existent project
        employee_id = 1

        # Mock database response for project check
        self.mock_cursor.fetchone.return_value = None

        # Execute and Assert
        with self.assertRaises(ProjectNotFoundException):
            self.repository.assign_task_in_project_to_employee(task_id, project_id, employee_id)

    # Additional test cases for better coverage
    def test_delete_nonexistent_employee_throws_exception(self):
        # Setup
        employee_id = 999  # Non-existent employee

        # Mock database response for employee check
        self.mock_cursor.fetchone.return_value = None

        # Execute and Assert
        with self.assertRaises(EmployeeNotFoundException):
            self.repository.delete_employee(employee_id)

    def test_delete_project_successfully(self):
        # Setup
        project_id = 1

        # Mock database responses
        self.mock_cursor.fetchone.return_value = [project_id]  # Project exists
        self.mock_cursor.execute.return_value = None
        self.mock_connection.commit.return_value = None

        # Execute
        result = self.repository.delete_project(project_id)

        # Assert
        self.assertTrue(result)
        self.mock_cursor.execute.assert_called()
        self.mock_connection.commit.assert_called()


if __name__ == '__main__':
    unittest.main()