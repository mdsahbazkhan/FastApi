# FastAPI framework import
from fastapi import FastAPI, Depends,HTTPException

# SQLAlchemy imports
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# Database URL
# sqlite:///./database.db
# Means create database.db file in current folder
DATABASE_URL = "sqlite:///./database.db"


# Create FastAPI app
app = FastAPI()


# Create database engine
# Engine helps Python connect with database
engine = create_engine(
    DATABASE_URL,

    # SQLite normally works in single thread only
    # False allows FastAPI to use DB in multiple requests/threads
    connect_args={"check_same_thread": False}
)


# sessionmaker creates new database sessions
# bind=engine means connect sessions with our database engine
sessionLocal = sessionmaker(bind=engine)


# Base class for creating database tables/models
Base = declarative_base()


# Todo model/table
class Todo(Base):

    # Table name inside database
    __tablename__ = "todos"

    # id column
    # Integer type
    # primary_key=True => unique ID
    # index=True => faster searching
    id = Column(Integer, primary_key=True, index=True)

    # title column
    title = Column(String)

    # completed column
    # Boolean means True/False
    # default=False means initially task is not completed
    completed = Column(Boolean, default=False)


# Create tables in database automatically
# If table already exists, it won't create again
Base.metadata.create_all(bind=engine)


# Dependency function
# Used to create and close DB session automatically
def get_db():

    # Create DB session
    db = sessionLocal()

    try:
        # Give DB session to route temporarily
        yield db

    finally:
        # Close DB session after request finishes
        db.close()



#Create API route to create new todo item
@app.post("/todos")

def create_todo(title:str,db:Session=Depends(get_db)):
    todo=Todo(title=title,completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
            "message": "Todo item created successfully",
            "data":todo
            }


# Read all todo items

@app.get("/todos")

def get_todos(db:Session=Depends(get_db)):
    todos=db.query(Todo).all()
    return {
            "message": "Todo items retrieved successfully",
            "Total":len(todos),
            "data":todos
            }
    

# Read single todo item by ID

@app.get("/todos/{todo_id}")

def get_todo(todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    return {
            "message": "Todo item retrieved successfully",
            "data":todo
            }
    
# Update todo item by ID

@app.put("/todos/{todo_id}")

def update_todo(todo_id:int,title:str,completed:bool, db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")

    todo.title=title
    todo.completed=completed
    db.commit()
    db.refresh(todo)
    return {
            "message": "Todo item updated successfully",
            "data":todo
            }

# Delete todo item by ID
@app.delete("/todos/{todo_id}")

def delete_todo(todo_id:int, db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")

    db.delete(todo)
    db.commit()
    return {
            "message": "Todo item deleted successfully"
            }