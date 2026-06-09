import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal

from auth import hash_password, verify_password, create_token
from dependencies import get_current_user, require_roles
from email_utils import send_login_email, send_promotion_email, send_signup_email

router = APIRouter()

      
# DB SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# SIGNUP (TRAINEE DEFAULT)
@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        existing = db.query(models.User).filter(models.User.email == user.email).first()

        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

        role = "trainee"
        initial_admin_email = os.getenv("INITIAL_ADMIN_EMAIL")
        admin_exists = db.query(models.User).filter(models.User.role == "admin").first()

        if not admin_exists:
            role = "admin"
        elif initial_admin_email and user.email == initial_admin_email:
            role = "admin"

        new_user = models.User(
            email=user.email,
            hashed_password=hash_password(user.password),
            role=role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        email_ok = send_signup_email(new_user.email)

        response = {"message": f"Signup successful as {role}"}
        if not email_ok:
            response["email_warning"] = "Signup created, but email notification failed. Check SMTP settings and app password."

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# LOGIN

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_token({
        "sub": db_user.email,
        "role": db_user.role
    })

    email_ok = send_login_email(db_user.email)

    response = {
        "message": "Login successful",
        "access_token": token,
        "user_id": db_user.id,
        "role": db_user.role
    }
    if not email_ok:
        response["email_warning"] = "Login succeeded, but email notification failed. Check SMTP settings and app password."

    return response


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return current_user


# TEAM LEADER → VIEW TRAINEES

@router.get("/trainees")
def get_trainees(
    current_user=Depends(require_roles(["team_leader", "admin"])),
    db: Session = Depends(get_db)
):

    return db.query(models.User).filter(
        models.User.role == "trainee"
    ).all()

@router.put("/assign-admin/{user_id}")
def assign_admin(
    user_id: int,
    current_user=Depends(require_roles(["admin"])),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = "admin"
    db.commit()

    return {"message": "User promoted to admin successfully"}

# PROMOTE TRAINEE → INTERN

@router.put("/promote/{user_id}")
def promote_to_intern(
    user_id: int,
    current_user=Depends(require_roles(["team_leader", "admin"])),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != "trainee":
        raise HTTPException(status_code=400, detail="Only trainee can be promoted")

    user.role = "intern"
    db.commit()

    send_promotion_email(user.email)

    return {"message": "User promoted to intern successfully"}



# VIEW INTERNS
@router.get("/interns")
def get_interns(
    current_user=Depends(require_roles(["team_leader", "admin"])),
    db: Session = Depends(get_db)
):

    return db.query(models.User).filter(
        models.User.role == "intern"
    ).all()