from typing import Union

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.database import get_session
from core.auth_utils import extract_token
from model.user import User
from core.security import token_manager
from service.menu_item_service import MenuItemService

security = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_session),
) -> User:
    token = credentials.credentials if credentials else extract_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    payload = token_manager.verify_token(token)
    subject: Union[str, int, None] = payload.get("sub")

    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = None
    if isinstance(subject, int) or (isinstance(subject, str) and subject.isdigit()):
        user = db.get(User, int(subject))

    if user is None:
        user = db.execute(select(User).where(User.email == str(subject))).scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive"
        )

    return user

def require_menu(path: str):
    async def permission(current_user: User = Depends(get_current_user),db: Session = Depends(get_session)):
        menu_id = current_user.get_menu_ids()
        menus = await MenuItemService(db).get_all_menu_by_id(menu_id)
        
        def has_permission(items):
            for item in items:
                if (
                    item.get("path") == path
                ):
                    return True

                if has_permission(item.get("children", [])):
                    return True

            return False

        if not has_permission(menus):
            raise HTTPException(
                status_code=403,
                detail="Permission denied."
            )

    return permission
