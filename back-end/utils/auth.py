from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from datetime import datetime, timezone
from model import User, Role, AuditLog
from fastapi import HTTPException, status


class AuthorizationService:

    def __init__(self, db: Session):
        self.db = db

    def create_role(self, role_name: str, description: Optional[str] = None, status: bool = True, menu: List[int] = []) -> Role:
        existing_role = self.get_role_by_name(role_name)
        
        if existing_role:
            raise HTTPException(
                status_code = 400,
                detail=f"Role '{role_name}' already exists"
            )
        
        role = Role(role_name=role_name, description=description, status=status, menu=list(set(menu)))
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def get_all_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        role_list = self.db.query(Role).offset(skip).limit(limit).all()
        return [role.to_dict() for role in role_list]
    
    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.role_name == role_name).first()
    
    def update_role(
        self,
        role_id: int,
        role_name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[bool] = None,
        menu: list[int] = []
    ) -> Role:
        role = self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id '{role_id}' not found"
            )
        
        if role_name:
            role.role_name = role_name
        
        if description is not None:
            role.description = description

        if status is not None:
            role.status = status

        if menu is not None:
            role.menu = list(set(menu))

        role.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def delete_role(self, role_id: int) -> str:
        role = self.get_role_by_id(role_id)

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id '{role_id}' not found"
            )
        
        self.db.delete(role)
        self.db.commit()
        return f"Role with id '{role_id}' has been deleted"
    
    

    def get_user_roles(self, user_id: int) -> List[str]:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return []
        roles: List[str] = []
        for user_role in user.user_roles:
            if not user_role.status:
                continue
            role = user_role.role
            if role and role.status and role.role_name not in roles:
                roles.append(role.role_name)
        return roles

    def get_user_permissions(self, user_id: int) -> List[str]:
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            return []

        permissions: List[str] = []
        for user_role in user.user_roles:
            if not user_role.status:
                continue
            role = user_role.role
            if not role or not role.status:
                continue

            for role_permission in role.role_permissions:
                if not role_permission.status:
                    continue
                permission = role_permission.permission
                if (
                    permission
                    and permission.status
                    and permission.permission_name not in permissions
                ):
                    permissions.append(permission.permission_name)

        return permissions

    # ========================================================================
    # OPTIMIZED BATCH ACCESS CONTROL CHECKS (Mitigating N+1 database leaks)
    # ========================================================================

    def has_permission(self, user_id: int, permission_name: str) -> bool:
        return self.has_any_permission(user_id, [permission_name])

    def has_role(self, user_id: int, role_name: str) -> bool:
        return self.has_any_role(user_id, [role_name])

    def has_any_permission(self, user_id: int, permissions: List[str]) -> bool:
        if not permissions:
            return False

        user_permissions = set(self.get_user_permissions(user_id))
        return any(permission in user_permissions for permission in permissions)

    def has_all_permissions(self, user_id: int, permissions: List[str]) -> bool:
        if not permissions:
            return True

        user_permissions = set(self.get_user_permissions(user_id))
        return set(permissions).issubset(user_permissions)

    def has_any_role(self, user_id: int, roles: List[str]) -> bool:
        if not roles:
            return False

        user_roles = set(self.get_user_roles(user_id))
        return any(role in user_roles for role in roles)

    def has_all_roles(self, user_id: int, roles: List[str]) -> bool:
        if not roles:
            return True

        user_roles = set(self.get_user_roles(user_id))
        return set(roles).issubset(user_roles)

    # ========================================================================
    # AUDIT LOGGING
    # ========================================================================

    def log_action(self, user_id: int, module: str, action: str, 
                   entity_type: str, entity_id: int, 
                   old_values: Optional[str] = None,
                   new_values: Optional[str] = None,
                   ip_address: Optional[str] = None) -> None:
        audit_log = AuditLog(
            module=module,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=old_values,
            new_value=new_values,
            user_id=user_id,
            ip_address=ip_address,
            status=True,
            created_at=datetime.now(timezone.utc),
        )
        
        self.db.add(audit_log)
        self.db.commit()
