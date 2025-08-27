from fastapi import FastAPI

app = FastAPI(title="Notes API")

@app.get("/health")
async def health():
    return {"status": "ok"}
