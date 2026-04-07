import shutil
from pathlib import Path
from shutil import copy

from PIL.Image import Image
from fastapi import APIRouter, UploadFile
from fastapi import Request
from tasks.tasks import process_pic
router_resize = APIRouter(prefix="/images", tags=["images"])


@router_resize.post("/")
async def resize_image(name: str, file: UploadFile):
    im_path = f"static/images/{name}.webp"
    with open(im_path, "wb+") as image_object:
        shutil.copyfileobj(file.file, image_object)
    process_pic.delay(im_path)