from fastapi import FastAPI
import sqlite3
import uvicorn
from sqlite3 import Error
from pydantic import BaseModel
from fastapi.responses import RedirectResponse, JSONResponse

app = FastAPI()

class URLObject(BaseModel):
    complete_url : str
    short_url : str

class CreateURLDB:
    def __init__(self, path="urls.db"):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, complete_url TEXT NOT NULL, short_url TEXT NOT NULL)")
        self.connection.commit()

    def insert_url(self, complete_url, short_url) -> bool:
        self.cursor.execute("SELECT complete_url FROM urls WHERE short_url=?", (short_url,))
        if self.cursor.fetchone() is not None:
            return False
        self.cursor.execute("INSERT INTO urls (complete_url, short_url) VALUES (?, ?)", (complete_url, short_url))
        self.connection.commit()
        return True


    def get_url(self, short_url) -> str:
        self.cursor.execute("SELECT complete_url FROM urls WHERE short_url=?", (short_url,))
        return self.cursor.fetchone()

    def __del__(self) -> None:
        self.connection.close()

db = CreateURLDB()

@app.get("/url/{shorturl}")
async def geturl(shorturl: str):
    if shorturl is None:
        return JSONResponse(status_code=404, content={"message": "shorturl is missing!"})
    completeurl = db.get_url(shorturl)
    if completeurl is None:
        return JSONResponse(status_code=404, content={"message": "shorturl not found!"})
    return RedirectResponse(url=completeurl[0])

@app.post("/url/", status_code=200)
async def createurl(input: URLObject):
    if input.complete_url is None or input.short_url is None:
        return JSONResponse(status_code=404, content={"message": "Please provide inputs properly!"})
    if not db.insert_url(input.complete_url, input.short_url):
        return JSONResponse(status_code=404, content={"message": "Record already exist. Try another short URL!"})
    return JSONResponse(status_code=200, content={"message": "Successfully created!"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)