from fastapi import FastAPI, HTTPException, Request
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
from functions import create_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Fetch neighbours
@app.post("/neighbours/", response_class=HTMLResponse)
async def fetch_item(request: Request, query: str=Form(...), neighbours: int=Form(...)):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    results = db.similarity_search(query, k=neighbours)
    return templates.TemplateResponse("index.html", {"request": request, "results": results})

# Create database
@app.get("/create/", response_class=JSONResponse)
async def create_database():
    create_db()
    return JSONResponse(content={"message": "Database created."})

# # Delete database
# @app.delete("/delete/", response_class=HTMLResponse)
# async def delete_database():
#     try:
#         delete_persisted_db()
#         return JSONResponse(content={"message": "Database deleted."})
#     except FileNotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))
    
