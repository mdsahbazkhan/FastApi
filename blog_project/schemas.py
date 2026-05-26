from pydantic import BaseModel

# Input Schema for creating a new blog post

class BlogCreate(BaseModel):
    title: str
    content: str
    
# Output Schema for returning a blog post
class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    
    class Config:
        from_attributes = True