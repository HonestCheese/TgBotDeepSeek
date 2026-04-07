from fastapi import APIRouter, Request, HTTPException, UploadFile
import shutil


router = APIRouter(
    prefix="/images",
    tags=["images"],
)

@router.post("/hotels")
async def add_image(name: str, file: UploadFile):
    with open(f"static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)


