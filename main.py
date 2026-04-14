from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import true
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from database.database import engine
from handlers.models import User
from images.images import router as image_router
from handlers import routers
from pages.router import router as page_router
from images.resize_icon import router_resize
from sqladmin import Admin, ModelView

@asynccontextmanager
async def lifespan(app: FastAPI):
        redis_client = redis.from_url("redis://:Try1moretime@localhost:6379/0", encoding="utf-8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis_client), prefix="cache")
        yield
        print("end")


app = FastAPI(lifespan=lifespan)


for router in routers:
        app.include_router(router)
app.include_router(page_router)
app.include_router(image_router)
app.include_router(router_resize)

app.mount("/static", StaticFiles(directory="static"), name="static") # Типа include router

origin = [

]

app.add_middleware(
        CORSMiddleware,
        allow_origins = origin,
        allow_credentials = True,
        allow_methods = ['*'],
        allow_headers = ['*'],
)



admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


admin.add_view(UserAdmin)