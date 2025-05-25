from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
#from pyseoa import SmartBatchSEOAnalyzer
from pyseoa import BatchSEOAnalyzer
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, url: str = Form(...), crawl: bool = Form(False)):
    # analyzer = SmartBatchSEOAnalyzer([url], follow_links=crawl)
    # analyzer.run_batch_analysis()
    # return templates.TemplateResponse("result.html", {
    #     "request": request,
    #     "url": url,
    #     "results": analyzer.results
    # })
    analyzer = BatchSEOAnalyzer([url])
    analyzer.run_batch_analysis()
    return templates.TemplateResponse('result.html', {
        "request": request,
        "url": url,
        "results": analyzer.results
    })

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
