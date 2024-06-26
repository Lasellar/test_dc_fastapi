import uvicorn
from fastapi import FastAPI
from database import engine, Base
from routers import tasks as tasks_router
from auth.routers import router as auth_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(tasks_router.router, prefix='/tasks', tags=['task'])
app.include_router(auth_router, prefix='/access', tags=['auth'])

if __name__ == '__main__':
    uvicorn.run(
        "main:app", host='127.0.0.1',
        port=8000, reload=True, workers=4
    )
