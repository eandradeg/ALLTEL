from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth
from database import engine, get_db
from datetime import timedelta
from typing import List


app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

@app.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(models.Administrator).filter(
        models.Administrator.usuario == form_data.username
    ).first()
    
    if not admin or not auth.verify_password(form_data.password, admin.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": admin.usuario, "permisionario": admin.permisionario},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/clients/", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = db.query(models.Client).offset(skip).limit(limit).all()
    return clients

@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
 
@app.get("/reclamations/", response_model=List[schemas.Reclamation])
def read_reclamations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reclamations = db.query(models.Reclamation).offset(skip).limit(limit).all()
    return reclamations

@app.post("/reclamations/", response_model=schemas.Reclamation)
def create_reclamation(reclamation: schemas.ReclamationCreate, db: Session = Depends(get_db)):
    db_reclamation = models.Reclamation(**reclamation.dict())
    db.add(db_reclamation)
    db.commit()
    db.refresh(db_reclamation)
    return db_reclamation

@app.get("/repair-times/", response_model=List[schemas.RepairTime])
def read_repair_times(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repair_times = db.query(models.RepairTime).offset(skip).limit(limit).all()
    return repair_times

@app.post("/repair-times/", response_model=schemas.RepairTime)
def create_repair_time(repair_time: schemas.RepairTimeCreate, db: Session = Depends(get_db)):
    db_repair_time = models.RepairTime(**repair_time.dict())
    db.add(db_repair_time)
    db.commit()
    db.refresh(db_repair_time)
    return db_repair_time