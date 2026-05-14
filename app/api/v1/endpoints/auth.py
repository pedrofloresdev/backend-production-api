import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import UserLogin

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, str(db_user.hashed_password)):
        logger.warning("Failed login attempt for email=%s", user.email)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    logger.info("User logged in email=%s", user.email)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
