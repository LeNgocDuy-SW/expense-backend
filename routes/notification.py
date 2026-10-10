from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database.database import engine
from model.user import User
from model.notification import Notification
from auth_helpers import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("")
def get_notifications(current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.created_at.desc())
        return session.exec(statement).all()

@router.put("/{notification_id}/read")
def mark_as_read(notification_id: int, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        notif = session.get(Notification, notification_id)
        if not notif or notif.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Not found")
        notif.is_read = True
        session.add(notif)
        session.commit()
        session.refresh(notif)
        return notif
