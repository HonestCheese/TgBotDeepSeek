from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

router = APIRouter(
    prefix="/pages",
    tags=["frontend"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/name", response_class=HTMLResponse)
async def get_something(request: Request):
    return templates.TemplateResponse(name="name.html", context={"request": request} )