
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers.users import user
from routers.security import security
from routers.buttons import button
from fastapi import FastAPI
import uvicorn

app = FastAPI(title='FalaComigo - v1')
app.include_router(security, prefix='/api', tags=['security'])
app.include_router(user, prefix='/api', tags=['users'])
app.include_router(button,prefix='/api', tags=['buttons'])
app.mount("/images", StaticFiles(directory="images"), name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4200)
