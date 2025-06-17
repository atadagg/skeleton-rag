from fastapi import FastAPI, BackgroundTasks
from src.indexer.run_indexer import run_indexing_pipeline

# from .dependencies import ...
# from .config import ...
# from websocket.router import WebSocketRouter
# from auth.router import auth_router

app = FastAPI()

@app.post("/update-index")
def update_index(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_indexing_pipeline)
    return {"status": "Index update started"}

# Include routers here
# app.include_router(WebSocketRouter(...))
# app.include_router(auth_router) 