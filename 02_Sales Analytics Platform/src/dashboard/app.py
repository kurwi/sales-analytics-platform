"""
Dash application entry point for Sales Analytics Platform.

This module initializes the Dash web application, configures the layout,
registers callbacks, and starts the real-time event processing system.
"""
import logging
from dash import Dash
import dash_bootstrap_components as dbc

from .layout import create_layout
from .callbacks import register_callbacks
from .realtime_client import start_realtime_client, sales_event_queue
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Dash application with professional Bootstrap theme
app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="Sales Analytics Platform"
)

app.title = "Sales Analytics Platform"

# Configure layout and callbacks
app.layout = create_layout()
register_callbacks(app)

def start_realtime_background():
    """
    Initialize real-time event processing system.
    
    Starts two background threads:
    1. Real-time client connection to streaming server
    2. Event polling loop for processing incoming sales events
    """
    start_realtime_client()
    
    def poll_events():
        """Poll and process events from the real-time queue."""
        while True:
            try:
                while not sales_event_queue.empty():
                    event = sales_event_queue.get()
                    logger.info(f"Processing real-time event: {event.get('type', 'unknown')}")
                    # Event processing logic can be extended here
                    # e.g., trigger callbacks, update stores, send notifications
                time.sleep(2)
            except Exception as e:
                logger.error(f"Event polling error: {e}", exc_info=True)
                time.sleep(5)
    
    polling_thread = threading.Thread(target=poll_events, daemon=True)
    polling_thread.start()
    logger.info("Real-time event processing system initialized")

# Start background services
start_realtime_background()

if __name__ == "__main__":
    logger.info("Starting Sales Analytics Platform")
    logger.info("Dashboard URL: http://localhost:8050")
    logger.info("Press CTRL+C to stop the server")
    
    app.run_server(debug=True, host='0.0.0.0', port=8050)
