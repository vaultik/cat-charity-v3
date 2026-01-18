from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_before_delete,
    check_project_before_edit,
    check_project_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud
from app.models import User
from app.schemas import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services import (
    process_edit_project, run_investing_process
)

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
UserDep = Annotated[User, Depends(current_user)]
SuperUserDep = Depends(current_superuser)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Получить все благотворительные проекты',
    description='Получает список всех проектов для сбора средств.'
                'Доступно для всех пользователей.',
    response_description='Данные проектов',
)
async def get_all_projects(
        session: SessionDep,
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Создать благотворительный проект',
    description='Создает новый проект для сбора средств.'
                'Только для суперюзеров.',
    response_description='Данные созданного проекта',
    dependencies=[SuperUserDep],
)
async def create_new_project(
        project: CharityProjectCreate,
        session: SessionDep,
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(
        project, session, not_commit=True
    )
    new_project = await run_investing_process(new_project, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Обновить благотворительный проект',
    description='Закрытый проект нельзя редактировать; '
                'нельзя установить требуемую сумму меньше уже вложенной..'
                'Только для суперюзеров.',
    response_description='Данные обновленного проекта',
    dependencies=[SuperUserDep],
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: SessionDep
):
    project = await check_project_exists(
        project_id, session
    )
    await check_project_before_edit(
        project, session, obj_in.name, obj_in.full_amount
    )
    project = await charity_project_crud.update(
        project, obj_in, session, True
    )
    process_edit_project(project, obj_in)
    project = await run_investing_process(project, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Удалить благотворительный проект',
    description='Нельзя удалить проект, '
                'в который уже были инвестированы средства.'
                'Только для суперюзеров.',
    response_description='Данные удаленного проекта',
    dependencies=[SuperUserDep],
)
async def remove_project(
        project_id: int,
        session: SessionDep
):
    project = await check_project_exists(
        project_id, session
    )
    await check_project_before_delete(project)
    project = await charity_project_crud.remove(
        project, session
    )
    return project
