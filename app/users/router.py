from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.users import schemas, auth
from app.users.models import User

router = APIRouter()

@router.post("/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já registrado")

    hashed_pw = auth.get_password_hash(user_in.password)

    new_user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        open_router_api_key=auth.encrypt_api_key(user_in.open_router_api_key)
        if user_in.open_router_api_key else None,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # retorna descriptografando
    return schemas.UserRead(
        id=new_user.id,
        email=new_user.email,
        is_active=new_user.is_active,
        open_router_api_key=auth.decrypt_api_key(new_user.open_router_api_key)
        if new_user.open_router_api_key else None
    )

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais incorretas")

    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/update", response_model=schemas.UserRead)
def update_user(
    user_in: schemas.UserUpdate,
    db: Session = Depends(auth.get_db),
    current_user: User = Depends(auth.get_current_user),
):
    if user_in.password:
        current_user.hashed_password = auth.get_password_hash(user_in.password)

    if user_in.open_router_api_key:
        current_user.open_router_api_key = auth.encrypt_api_key(user_in.open_router_api_key)

    db.commit()
    db.refresh(current_user)

    return schemas.UserRead(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        open_router_api_key=auth.decrypt_api_key(current_user.open_router_api_key)
        if current_user.open_router_api_key else None
    )
