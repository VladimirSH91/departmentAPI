import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, date
from app.repositories.department import DepartmentRepository
from app.service.department import DepartmentService
from app.schemes.department import DepatmentCreate, DepartmentUpdate, DepatmentRead
from app.schemes.employee import EmployeeRead

@pytest.fixture
def mock_repo():
    """Фикстура для репозитория с замоканными асинхронными методами."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_by_name_and_parent = AsyncMock()
    repo.create = AsyncMock()
    repo.get_children = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    repo.db_session = MagicMock()
    repo.db_session.flush = AsyncMock()
    return repo

@pytest.fixture
def mock_employee_repo():
    """Фикстура для employee репозитория."""
    repo = MagicMock()
    repo.get_employees = AsyncMock()
    repo.update_department_from_employee = AsyncMock()
    return repo

@pytest.fixture
def service(mock_repo, mock_employee_repo):
    """Фикстура для сервиса, принимающего замоканные репозитории."""
    return DepartmentService(repo=mock_repo, employee_repo=mock_employee_repo)

@pytest.mark.asyncio
async def test_create_department_success_without_parent(service, mock_repo):
    """Успешное создание отдела без родителя (parent_id = None)."""
    # Подготовка
    data = DepatmentCreate(name="HR", parent_id=None)
    expected_dict = data.model_dump()
    expected_department = MagicMock(id=1, **expected_dict)
    
    # Настройка моков
    mock_repo.get_by_name_and_parent.return_value = None  # нет дубликата
    mock_repo.create.return_value = expected_department
    
    # Вызов
    result = await service.create_department(data)
    
    # Проверки
    mock_repo.get_by_id.assert_not_awaited()  # parent_id=None -> проверка не нужна
    mock_repo.get_by_name_and_parent.assert_awaited_once_with(
        expected_dict['name'], None
    )
    mock_repo.create.assert_awaited_once_with(expected_dict)
    assert result == expected_department


@pytest.mark.asyncio
async def test_get_department_tree_not_found(service, mock_repo):
    """Отдел не найден."""
    mock_repo.get_by_id.return_value = None
    
    result = await service.get_department_tree(
        department_id=999,
        dept=0,
        include_employees=False,
        sort_employees_by='created_at'
    )
    
    assert result is None
    mock_repo.get_by_id.assert_awaited_once_with(999)

@pytest.mark.asyncio
async def test_update_department_success_name_only(service, mock_repo):
    """Успешное обновление только названия отдела."""
    department_id = 1
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    updated_department = MagicMock(id=department_id, name="Technology", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.return_value = mock_department
    mock_repo.get_by_name_and_parent.return_value = None
    mock_repo.update.return_value = updated_department
    
    update_data = DepartmentUpdate(name="Technology")
    result = await service.update_department(department_id, update_data)
    
    assert result == updated_department
    mock_repo.get_by_id.assert_awaited_once_with(department_id)
    mock_repo.update.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_department_not_found(service, mock_repo):
    """Отдел для обновления не найден."""
    mock_repo.get_by_id.return_value = None
    
    update_data = DepartmentUpdate(name="New Name")
    with pytest.raises(HTTPException) as exc_info:
        await service.update_department(999, update_data)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Department not found"

@pytest.mark.asyncio
async def test_update_department_parent_not_found(service, mock_repo):
    """Новый родительский отдел не найден."""
    department_id = 1
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.return_value = mock_department
    mock_repo.get_by_id.side_effect = [mock_department, None]  # First call returns department, second returns None for parent
    
    update_data = DepartmentUpdate(parent_id=999)
    with pytest.raises(HTTPException) as exc_info:
        await service.update_department(department_id, update_data)
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_update_department_own_parent(service, mock_repo):
    """Попытка сделать отдел своим собственным родителем."""
    department_id = 1
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.return_value = mock_department
    
    update_data = DepartmentUpdate(parent_id=department_id)
    with pytest.raises(HTTPException) as exc_info:
        await service.update_department(department_id, update_data)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Department cannot be its own parent"

@pytest.mark.asyncio
async def test_update_department_name_conflict(service, mock_repo):
    """Конфликт имени при обновлении."""
    department_id = 1
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    existing_department = MagicMock(id=2, name="HR", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.return_value = mock_department
    mock_repo.get_by_name_and_parent.return_value = existing_department
    
    update_data = DepartmentUpdate(name="HR")
    with pytest.raises(HTTPException) as exc_info:
        await service.update_department(department_id, update_data)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Department with this name already exists in the same parent"

@pytest.mark.asyncio
async def test_delete_department_cascade(service, mock_repo, mock_employee_repo):
    """Удаление отдела в cascade режиме."""
    department_id = 1
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.return_value = mock_department
    mock_repo.delete.return_value = None
    
    await service.delete_department(department_id, mode="cascade")
    
    mock_repo.get_by_id.assert_awaited_once_with(department_id)
    mock_repo.delete.assert_awaited_once_with(mock_department)

@pytest.mark.asyncio
async def test_delete_department_not_found(service, mock_repo):
    """Отдел для удаления не найден."""
    mock_repo.get_by_id.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_department(999, mode="cascade")
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Department not found"

@pytest.mark.asyncio
async def test_delete_department_reassign_missing_target_id(service, mock_repo):
    """Удаление в режиме reassign без указания целевого отдела."""
    department_id = 1
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.return_value = mock_department
    
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_department(department_id, mode="reassign", reassign_to_department_id=None)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "reassign_to_department_id is required when mode=reassign"

@pytest.mark.asyncio
async def test_delete_department_reassign_target_not_found(service, mock_repo):
    """Целевой отдел для переназначения не найден."""
    department_id = 1
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.side_effect = [mock_department, None]
    
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_department(department_id, mode="reassign", reassign_to_department_id=999)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Target department not found"

@pytest.mark.asyncio
async def test_delete_department_reassign_same_department(service, mock_repo):
    """Попытка переназначить на тот же отдел."""
    department_id = 1
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.return_value = mock_department
    
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_department(department_id, mode="reassign", reassign_to_department_id=department_id)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Cannot reassign to the same department"

@pytest.mark.asyncio
async def test_delete_department_reassign_success(service, mock_repo, mock_employee_repo):
    """Успешное удаление в режиме reassign."""
    department_id = 1
    target_department_id = 2
    mock_department = MagicMock(id=department_id, name="IT", parent_id=None, created_at=datetime.now())
    mock_target_department = MagicMock(id=target_department_id, name="HR", parent_id=None, created_at=datetime.now())
    
    mock_repo.get_by_id.side_effect = [mock_department, mock_target_department]
    mock_repo.get_children.return_value = []
    mock_repo.delete.return_value = None
    
    await service.delete_department(department_id, mode="reassign", reassign_to_department_id=target_department_id)
    
    mock_employee_repo.update_department_from_employee.assert_awaited_once_with(department_id, target_department_id)
    mock_repo.delete.assert_awaited_once_with(mock_department)
