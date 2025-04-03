from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/")
async def webhook(request: Request):
    payload = await request.json()
    print("Received webhook:", payload)
    return {"message": "Webhook received"}

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=10000)
