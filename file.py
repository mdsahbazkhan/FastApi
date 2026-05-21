# Import required modules from FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException

# Used for file and folder operations
import os

# Used to serve uploaded files as static files
from fastapi.staticfiles import StaticFiles

# Used to copy uploaded file data
import shutil


# Create FastAPI app
app = FastAPI()


# -----------------------------
# STEP 1: Create uploads folder
# -----------------------------

# Folder name where uploaded files will be stored
UPLOAD_DIR = "uploads"

# Check if uploads folder exists
if not os.path.exists(UPLOAD_DIR):

    # Create uploads folder if it does not exist
    os.makedirs(UPLOAD_DIR)


# ---------------------------------
# STEP 2: Configure static files
# ---------------------------------

# This allows users to access uploaded files using URL
# Example:
# http://127.0.0.1:8000/files/image.png

app.mount(
    "/files",                          # URL path
    StaticFiles(directory=UPLOAD_DIR), # Folder location
    name="files"
)


# ---------------------------------
# STEP 3: File upload API
# ---------------------------------

# Create POST API endpoint
@app.post("/upload")

# UploadFile handles uploaded file
# File(...) means file is required
def upload_file(file: UploadFile = File(...)):

    # Check if filename exists
    if not file.filename:

        # Return error if no file uploaded
        raise HTTPException(
            status_code=400,
            detail="No file uploaded"
        )

    # Create full file path
    # Example: uploads/photo.png
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Open file in write binary mode
    with open(file_path, "wb") as buffer:

        # Copy uploaded file content into buffer
        shutil.copyfileobj(file.file, buffer)

    # Return success response
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,

        # File access URL
        "url": f"http://127.0.0.1:8000/files/{file.filename}"
    }


# ---------------------------------
# STEP 4: Get file details API
# ---------------------------------

# Dynamic route for filename
@app.get("/files/{filename}")

def get_file(filename: str):

    # Create full file path
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Check if file exists
    if not os.path.exists(file_path):

        # Return 404 error if file not found
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    # Return file details
    return {
        "filename": filename,
        "url": f"http://127.0.0.1:8000/files/{filename}"
    }



@app.get("/")

def home():

    return {
        "message": "Welcome to the File Upload API"
    }