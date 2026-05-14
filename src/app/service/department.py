from repositories.department import DepartmentRepository
from repositories.employee import EmployeeRepository
from schemes import DepatmentCreate, DepatmentRead, EmployeeRead

class DepartmentService:
    def __init__(self, repo: DepartmentRepository, employee_repo = EmployeeRepository):
        self.repo = repo
        self.employee_repo = employee_repo

    async def create_department(self, data: DepatmentCreate):
        pass
        
    async def get_department_tree(self, 
                                  department_id: int, 
                                  dept: int,
                                  include_employees: bool, 
                                  sort_employees_by='created_at'):
        department_repo = await self.repo.get_by_id(department_id)
        
        if not department_repo:
            return None

        employees = []
        if include_employees:
            employees_orm = await self.employee_repo.get_employees(department_id=department_id, 
                                                                   sort_by=sort_employees_by)
            employees = [EmployeeRead.model_validate(e) for e in employees_orm] if employees_orm else []
        
        children = []
        if dept > 0:
            child_departments = await self.repo.get_children(department_id)
            for child in child_departments:
                child_tree = await self.get_department_tree(
                child.id,
                dept - 1,
                include_employees,
                sort_employees_by
            )
            if child_tree:
                children.append(child_tree)

        # Тут по высланому ТЗ требуется рекурсивный вывод. 
        # В реальных задачах подобного рода вызовы если и допустимы, то использовать их надо с аккуратностью
        # Имеет недостатки - возможность переполнения стэка, увеличивает потребление памяти, снижате производительность и прочее
        # В связи с этим к большим данным применять может быть опасно


        return DepatmentRead(
            id=department_repo.id,
            name=department_repo.name,
            created_at=department_repo.created_at,
            parent_id=department_repo.parent_id,
            employees=employees,
            children=children).model_dump()  
