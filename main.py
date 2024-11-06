from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.templating import Jinja2Templates

app = FastAPI(title = "E-commerce Scrapper")

templates = Jinja2Templates(directory = "templates")

@app.get("/", response_class=HTMLResponse)

async def read_item(request: Request):
    title = "E-Commerce Scrapper"
    return templates.TemplateResponse(
        name="index.html",
        context = {
            "request" : request,
            "title": title
        })

@app.get("/run")

async def get_file(file_uploaded :UploadFile = File(...), amazon_checked:bool = False, flipkart_checked:bool = False):
    print(amazon_checked)
    print(flipkart_checked)
    print(file_uploaded.filename)