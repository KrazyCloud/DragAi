from fastapi import FastAPI
from routes.chatRoute import router

app = FastAPI()

app.include_router(router)

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="10.226.53.238", port=5003)