"""
Dash client for real-time sales updates using SocketIO
"""
import socketio
import threading
import queue

# Thread-safe queue for passing events to Dash
sales_event_queue = queue.Queue()

# SocketIO client
sio = socketio.Client()

@sio.event
def connect():
    print("[Realtime] Connected to streaming server.")

@sio.event
def disconnect():
    print("[Realtime] Disconnected from streaming server.")

@sio.on('new_sale')
def on_new_sale(data):
    print(f"[Realtime] New sale event: {data}")
    sales_event_queue.put(data)

def start_realtime_client():
    def run():
        try:
            sio.connect('http://localhost:8001', transports=['websocket'])
            sio.wait()
        except Exception as e:
            print(f"[Realtime] Connection error: {e}")
    t = threading.Thread(target=run, daemon=True)
    t.start()
