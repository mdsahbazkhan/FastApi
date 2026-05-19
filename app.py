# FastAPI framework import
from fastapi import FastAPI, Depends

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


# Home route
@app.get("/")
def home(db: Session = Depends(get_db)):

    # Depends(get_db)
    # FastAPI automatically calls get_db()
    # and gives database session inside db variable

    return {
        "message": "DB connected successfully!"
    }