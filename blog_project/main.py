from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from db import engine,sessionLocal
from auth import verify_token,create_token

import models,schemas

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
# Dependency to get DB session
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# Login API to get token
@app.post("/login")
def login():
    return{
        "access_token":create_token({"user":"admin1"}),
        "token_type":"bearer"
    }

@app.get("/")
def home():
    return {"message": "Welcome to the Blog API!"}

# Create a new blog post

@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    new_blog=models.Blog(
        title=blog.title,
        content=blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get all blog posts
@app.get("/blogs",response_model=list[schemas.BlogResponse])
def get_blogs(db:Session=Depends(get_db),user=Depends(verify_token)):
    blogs=db.query(models.Blog).all()
    return blogs

# Get a single blog post by ID

@app.get("/blogs/{blog_id}",response_model=schemas.BlogResponse)
def get_blog(blog_id:int,db:Session=Depends(get_db),user=Depends(verify_token)):
    blog=db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code=404,detail="Blog not found")
    return blog


# Update a blog post by ID
@app.put("/blogs/{blog_id}",response_model=schemas.BlogResponse)

def update_blog(blog_id:int,blog:schemas.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    existing_blog=db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not existing_blog:
        raise HTTPException(status_code=404,detail="Blog not found")
    existing_blog.title=blog.title
    existing_blog.content=blog.content
    db.commit()
    db.refresh(existing_blog)
    return existing_blog

# Delete a blog post by ID
@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id:int, db:Session=Depends(get_db),user=Depends(verify_token)):
    blog=db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return { "message": "Blog deleted successfully", "blog": blog }
