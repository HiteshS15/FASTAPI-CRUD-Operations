from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import user, Gender, Role, UserUpdateRequest
from typing import Optional, List
from uuid import UUID, uuid4


# creating an instance of the FastAPI class called app, 
# which will serve as the main entry point for your application.
app = FastAPI()

db: List[user] = [
    user(
        id=uuid4(),
        first_name="Hitesh",
        last_name="S",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    ),
    user(
        id=uuid4(),
        first_name="SSHHSS",
        last_name="S",
        gender=Gender.female,
        roles=[Role.student]
    )
]

@app.get("/api/users")
def get_users():
    return db

@app.post("/api/users")
def addusers(user:user):
    db.append(user)
    return {"id":user.id}

@app.put("/api/users/{user_id}")
def updateUser(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles   
        return
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exists"
    )   
@app.delete("/api/users/{user_id}")  
def deleteUser(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return{"msg":"record deleted"}         

               
    