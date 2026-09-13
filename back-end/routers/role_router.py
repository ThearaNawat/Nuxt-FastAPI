from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from infrastructure.database import get_session
from utils.auth import AuthorizationService
from core.dependency import get_current_user, require_menu
from schema.role import base_role as RoleCreate, base_role as RoleUpdate, base_role_read as RoleResponse
from model import User, Role

role_router = APIRouter(prefix="/role", tags=["role_management"])


@role_router.get("", response_model=List[RoleResponse], dependencies=[Depends(require_menu('/role'))])
async def get_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> List[RoleResponse]:
    return AuthorizationService(db).get_all_roles(skip, limit)


@role_router.get("/{role_id}", response_model=RoleResponse, dependencies=[Depends(require_menu('/role'))])
async def get_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Role:
    role = AuthorizationService(db).get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target RBAC identity profile not found.")
    return role


@role_router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_menu('/create'))])
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Role:
    return AuthorizationService(db).create_role(**role_data.model_dump())


@role_router.put("/{role_id}", response_model=RoleResponse, dependencies=[Depends(require_menu('/update'))])
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> Role:
    print(f"Updating role with ID: {role_id} and data: {role_data}")
    updated_role = AuthorizationService(db).update_role(role_id, **role_data.model_dump(exclude_unset=True))
    if not updated_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target RBAC identity profile not found.")
    return updated_role


@role_router.delete("/{role_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_menu('/delete'))])
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
) -> str:
    return AuthorizationService(db).delete_role(role_id)
        