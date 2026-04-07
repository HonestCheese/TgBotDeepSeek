from fastapi import APIRouter
from fastapi import Request
router_resize = APIRouter(prefix="/images", tags=["images"])


@router_resize.post("/resize")
async def resize_image(request: Request):
    request.