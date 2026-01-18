from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import (
    DonationCreate, DonationDB, DonationFullInfoDB
)
from app.services import run_investing_process

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
UserDep = Annotated[User, Depends(current_user)]
SuperUserDep = Depends(current_superuser)


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    summary='Получить список всех пожертвований',
    description='Получает список всех пожертвований '
                'в проекты для сбора средств.'
                'Только для суперюзеров.',
    response_description='Список пожертвований',
    dependencies=[SuperUserDep],
)
async def get_all_donations(
        session: SessionDep
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    summary='Получить список своих пожертвований',
    description='Получает список только своих пожертвований '
                'с базовой информацией, без подробностей.'
                'Только для авторизованных пользователей.',
    response_description='Список своих пожертвований',
)
async def get_all_donations(
        user: UserDep,
        session: SessionDep,
):
    return await donation_crud.get_by_user(user, session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary='Создать пожертвование',
    description='Создает новое пожертвование в проекты для сбора средств.'
                'Только для авторизованных пользователей.',
    response_description='Данные созданного проекта',
)
async def create_donation(
        donation: DonationCreate,
        user: UserDep,
        session: SessionDep
):
    new_donation = await donation_crud.create(
        donation, session, user, not_commit=True
    )
    new_donation = await run_investing_process(new_donation, session)
    return new_donation
