import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fragmentation_server.router import router
load_dotenv()
app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "WebSocket Server is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=os.getenv("MY_IP"), port=3000)
