from repositories.employee import EmployeeRepository

class EmployeeServise:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo
    
    async def create_employee(self, employee_data):
        pass

    