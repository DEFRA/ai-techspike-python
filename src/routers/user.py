from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from bson import ObjectId
from src.models.user import Users, UserCollection, UpdateUsers


router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get("/", response_description="List all users", response_model=UserCollection, response_model_by_alias=False)
async def get_users(request: Request):
    users = request.app.db["users"]
    results = []
    cursor = users.find()
    async for user in cursor:
        results.append(user)
    return UserCollection(users=results)

@router.get("/{id}", response_description="Get a single user", response_model=Users, response_model_by_alias=False)
async def get_user(request: Request, id: str):
    users = request.app.db["users"]
    
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    
    if (user := await users.find_one({"_id": ObjectId(id)})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {id} not found")

@router.put("/{id}", response_description="Update a user", response_model=Users, response_model_by_alias=False)
async def update_user(request: Request, id: str, user: UpdateUsers = Body(...)):
    users = request.app.db["users"]
    
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    
    document = user.model_dump(
        by_alias=True,
        exclude_unset=True,
        exclude=["id"]
    )
    if (user := await users.find_one_and_update({"_id": ObjectId(id)}, {"$set": document}, return_document=True)) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {id} not found")

@router.post("/", response_description="Add new user", response_model=Users, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def add_user(request: Request, user: Users = Body(...)):
    users = request.app.db["users"]
    document = user.model_dump(
        by_alias=True,
        exclude_unset=True,
        exclude=["id"]
    )
    inserted = await users.insert_one(document)
    return await users.find_one({"_id": inserted.inserted_id})

@router.delete("/{id}", response_description="Delete a user", response_model=Users)
async def delete_user(request: Request, id: str):
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    
    users = request.app.db["users"]

    delete_user = await users.find_one({"_id": ObjectId(id)})

    if delete_user.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"User {id} not found")
    