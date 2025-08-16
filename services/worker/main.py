from fastapi import FastAPI

# Placeholder: In a real system this would be a Celery/Arq worker process.
# For now we expose a health endpoint to let Compose start successfully.

app = FastAPI(title="IIA Worker")

@app.get("/health")
async def health():
    return {"status": "ok"}

