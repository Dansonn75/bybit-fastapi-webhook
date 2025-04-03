from fastapi import FastAPI, Request
import uvicorn
import os
from pybit.unified_trading import HTTP  # Import Bybit client

app = FastAPI()

# Initialize Bybit testnet session
session = HTTP(
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
    testnet=True
)

@app.post("/")
async def webhook(request: Request):
    payload = await request.json()
    print("Received webhook:", payload)

    try:
        symbol = payload.get("symbol", "BTCUSDT")
        side = payload.get("side", "Buy")
        qty = float(payload.get("qty", 0.1))

        order = session.place_active_order(
            category="linear",
            symbol=symbol,
            side=side,
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel"
        )

        print("✅ Order placed:", order)
        return {"message": "Order placed", "details": order}

    except Exception as e:
        print("❌ Order failed:", e)
        return {"error": str(e)}

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=10000)
