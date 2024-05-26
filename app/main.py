from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi import Form
from models import Query
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from functions import create_db, delete_persisted_db
import os
from firebase import upload_to_firebase

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Upload file
@app.post("/upload/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    os.makedirs("app/temp", exist_ok=True)
    file_location = f"app/temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    file_url = upload_to_firebase(file_location, file.filename)
    # Remove the temporary file
    os.remove(file_location)
    create_db(file_url)
    return templates.TemplateResponse("index.html", {"request": request, "message": f"File uploaded"})

# Fetch neighbours
@app.post("/neighbours/", response_class=HTMLResponse)
async def fetch_item(request: Request, query: str=Form(...), neighbours: int=Form(...)):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="app/chroma_db", embedding_function=embedding_function)
    results = db.similarity_search(query, k=neighbours)
    return templates.TemplateResponse("index.html", {"request": request, "results": results})


    
