from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main() -> dict:
    return {
        "message": "게시판"
    }