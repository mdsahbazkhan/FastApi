from dotenv import load_dotenv
import os
load_dotenv()

class Settings:
    origins=os.getenv("ORIGINS")
    
settings=Settings()