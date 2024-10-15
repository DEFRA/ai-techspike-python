from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from bson import ObjectId
from src.models.todo import Todos, TodoCollection, UpdateTodos

router = APIRouter(
    prefix='/todo',
    tags=['todo']
)

@router.get("/", response_description="List all todos", response_model=TodoCollection, response_model_by_alias=False)
async def get_todos(request: Request):
    todos = request.app.db["todos"]
    results = []
    cursor = todos.find()
    async for todo in cursor:
        results.append(todo)
    return TodoCollection(todos=results)

@router.get("/{id}", response_description="Get a single todo", response_model=Todos, response_model_by_alias=False)
async def get_todo(request: Request, id: str):
    todos = request.app.db["todos"]
    
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Todo {id} not found")
    
    if (todo := await todos.find_one({"_id": ObjectId(id)})) is not None:
        return todo
    raise HTTPException(status_code=404, detail=f"Todo {id} not found")

@router.put("/{id}", response_description="Update a todo", response_model=Todos, response_model_by_alias=False)
async def update_todo(request: Request, id: str, todo: UpdateTodos = Body(...)):
    todos = request.app.db["todos"]
    
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Todo {id} not found")
    
    document = todo.model_dump(
        by_alias=True,
        exclude_unset=True,
        exclude=["id"]
    )
    if (todo := await todos.find_one_and_update({"_id": ObjectId(id)}, {"$set": document}, return_document=True)) is not None:
        return todo
    raise HTTPException(status_code=404, detail=f"Todo {id} not found")

@router.post("/", response_description="Add new todo", response_model=Todos, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def add_todo(request: Request, todo: Todos = Body(...)):
    todos = request.app.db["todos"]
    document = todo.model_dump(
        by_alias=True,
        exclude_unset=True,
        exclude=["id"]
    )
    inserted = await todos.insert_one(document)
    return await todos.find_one({"_id": inserted.inserted_id})

@router.delete("/{id}", response_description="Delete a todo", response_model=Todos, response_model_by_alias=False)
async def delete_todo(request: Request, id: str):
    todos = request.app.db["todos"]
    
    try:
        id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Todo {id} not found")
    
    if (todo := await todos.find_one({"_id": ObjectId(id)})) is not None:
        await todos.delete_one({"_id": ObjectId(id)})
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=404, detail=f"Todo {id} not found")