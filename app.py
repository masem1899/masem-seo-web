from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
#from pyseoa import SmartBatchSEOAnalyzer
from pyseoa import BatchSEOAnalyzer
from rate_limiter import get_user_id, can_run_analysis, record_analysis
from middleware.i18n import I18nMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(I18nMiddleware)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    _ = request.state.gettext
    return templates.TemplateResponse("index.html", {
        "request": request,
        '_': _,
    })

@app.post("/analyze", response_class=HTMLResponse)
def analyze(request: Request, url: str = Form(...), crawl: bool = Form(False)):
    user_id = get_user_id(request)
    allowed, message = can_run_analysis(user_id, crawl)

    if not allowed:
        return HTMLResponse(f'<h1>❌ {message}</h1><a href="/">⬅ Back</a>', status_code=429)
    
    record_analysis(user_id, crawl)

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
        "results": analyzer.results,
        "message": message
    })

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
