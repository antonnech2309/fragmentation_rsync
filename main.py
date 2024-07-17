from fastapi import FastAPI
from fragmentation_server.routes import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "WebSocket Server is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="188.208.196.87", port=8000)
