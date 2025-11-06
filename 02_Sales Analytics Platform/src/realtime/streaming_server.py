"""
Real-Time Streaming Server for Sales Dashboard (Exercise 7)
Broadcasts live sales and pipeline updates using SocketIO + FastAPI
"""

import asyncio
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd
from pathlib import Path
import time

# SocketIO server (async mode)
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app_sio = socketio.ASGIApp(sio, app)

# Path to sales data (simulate live updates)
DATA_PATH = Path(__file__).parent.parent.parent / 'data' / 'sales_data.csv'

async def sales_update_broadcast():
    """Background task: broadcast new sales every 5 seconds"""
    last_row = 0
    while True:
        if DATA_PATH.exists():
            df = pd.read_csv(DATA_PATH)
            if len(df) > last_row:
                # Send only new rows
                new_sales = df.iloc[last_row:]
                for _, row in new_sales.iterrows():
                    await sio.emit('new_sale', row.to_dict())
                last_row = len(df)
        await asyncio.sleep(5)

@app.on_event("startup")
async def start_broadcast():
    asyncio.create_task(sales_update_broadcast())

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

if __name__ == "__main__":
    print("Starting real-time streaming server on http://localhost:8001 ...")
    uvicorn.run(app_sio, host="0.0.0.0", port=8001)
