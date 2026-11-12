from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from jose import jwt, JWTError

from app.core.database import get_db
from app.models.chat import ChatMessage
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse
from app.api.v1.endpoints.auth import oauth2_scheme
from app.core.security import SECRET_KEY, ALGORITHM

router = APIRouter()

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        # هنا نفترض أنك تستخدم ID 1 للـ admin للتسهيل
        # في مشروع حقيقي، ستقوم بجلب الـ ID من قاعدة البيانات بناءً على username
        return 1 
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=List[ChatMessageResponse])
def get_history(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    messages = db.query(ChatMessage).filter(ChatMessage.user_id == user_id).order_by(ChatMessage.created_at).all()
    return messages

@router.post("/", response_model=ChatMessageResponse)
def save_message(message: ChatMessageCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    new_msg = ChatMessage(user_id=user_id, role=message.role, content=message.content)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg