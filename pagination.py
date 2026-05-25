from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import time

app=FastAPI()

last_fetch = 0 
cache_data = []
@app.get("/news")
# def get_news(page:int=1,limit:int=5):
def get_news():
    global cache_data, last_fetch
    start= time.time()
    if time.time() - last_fetch>60:
       
        url="https://news.ycombinator.com/"
        response=requests.get(url)
        soup=BeautifulSoup(response.text,"html.parser")
        cache_data=[item.text for item in soup.find_all("span",class_="titleline")]
        last_fetch=time.time()
        
    
    end= time.time()
    time_taken= round(end-start,4)
    return{
            "time_taken": time_taken,
            "message": "Data fetched from cache",
            "data":cache_data[:5]
        }
        
        
        #  Pagination logic
        # title=[]
        
        # for item in soup.find_all("span",class_="titleline"):
        #     title.append(item.text )
        
        # # Pagination logic
        # start = (page - 1) * limit
        # end = start + limit
        # return {
        #     "page": page,
        #     "limit": limit,
        #     "total": len(title),
        #     "data": title[start:end]}
        