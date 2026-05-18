from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel

app=FastAPI()

todos=[]


class Todo(BaseModel):
    id:int
    title:str
    description:str
    completed:bool=False
    
    
@app.post("/todos",status_code=status.HTTP_201_CREATED)

def create_todo(todo:Todo):
    todos.append(todo)
    return {"message":"Todo created successfully","data":todo}


@app.get("/todos", status_code=status.HTTP_200_OK)

def get_todos():
    
    return {"message":"List of todos","data":todos}


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)

def get_todo(todo_id:int):
    for todo in todos:
        if todo.id==todo_id:
            return {"message":"Todo found","data":todo}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)


def update_todo(todo_id:int,updated_todo:Todo):
    for index,todo in enumerate(todos):
        if todo.id==todo_id:
            todos[index]=updated_todo
            return {"message":"Todo updated successfully","data":updated_todo}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)

def delete_todo(todo_id:int):
    for index,todo in enumerate(todos):
        if todo.id==todo_id:
            deleted_todo=todos.pop(index)
            return {"message":"Todo deleted successfully","data":deleted_todo}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


