from fastapi import HTTPException

from repositories.department import DepartmentRepository
from repositories.employee import EmployeeRepository
from schemes import DepatmentCreate, DepatmentRead, DepartmentUpdate, EmployeeRead

class DepartmentService:
    def __init__(self, repo: DepartmentRepository, employee_repo = EmployeeRepository):
        self.repo = repo
        self.employee_repo = employee_repo

    async def create_department(self, data: DepatmentCreate):
        department_dict = data.model_dump()
        
        if 'parent_id' in department_dict and department_dict['parent_id'] is not None:
            parent_exist = await self.repo.get_by_id(department_dict['parent_id'])
            if not parent_exist:
                raise HTTPException(status_code=404, detail='Parent department not found')
        
        department = await self.repo.create(department_dict)
        return department
        
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
        # Однако в связи с ограничением по глубине - пусть будет

        return DepatmentRead(
            id=department_repo.id,
            name=department_repo.name,
            created_at=department_repo.created_at,
            parent_id=department_repo.parent_id,
            employees=employees,
            children=children)


    async def update_department(self, 
                                department_id: int,
                                update_data: DepartmentUpdate):
        department = await self.repo.get_by_id(department_id)
        if not department:
            raise HTTPException(status_code=404, detail='Department not found')
        update_dict = update_data.model_dump()
        if 'parent_id' in update_dict:
            new_parent_id = update_dict['parent_id']

            if new_parent_id == department_id:
                raise HTTPException(status_code=404, 
                                    detail="Department cannot be its own parent")
            if new_parent_id is not None:
                parent_exist = await self.repo.get_by_id(new_parent_id)
                if not parent_exist:
                    raise HTTPException(status_code=404, 
                                        detail='Department not found')
        
        updated_department = await self.repo.update(department, update_dict)
        return updated_department


    async def delete_department(self, 
                                department_id: int,
                                mode: str,
                                reassign_to_department_id: int | None = None):
        department = await self.repo.get_by_id(department_id)
        if not department:
            raise HTTPException(status_code=404, detail='Department not found')
        
        if mode == 'reassign':
            if reassign_to_department_id is None:
                raise HTTPException(status_code=400, detail='reassign_to_department_id is required when mode=reassign')
            
            target_department = await self.repo.get_by_id(reassign_to_department_id)
            if not target_department:
                raise HTTPException(status_code=404, detail='Target department not found')
            
            if reassign_to_department_id == department_id:
                raise HTTPException(status_code=400, detail='Cannot reassign to the same department')
            
            # Reassign employees to the target department
            await self.employee_repo.update_department_from_employee(department_id, reassign_to_department_id)
            
            # Reassign child departments to the parent of the deleted department
            child_departments = await self.repo.get_children(department_id)
            for child in child_departments:
                child.parent_id = department.parent_id
            await self.repo.db_session.flush()
        
        # Delete the department (cascade will handle employees and children in cascade mode)
        await self.repo.delete(department)

