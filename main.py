import flet as ft
from fastapi import FastAPI
import uvicorn
import threading

# Import your application components
from app.api.routes import router
from app.ui.views import main_view

# Create FastAPI app
app = FastAPI(title="AI Code Assistant")

# Register API routes
app.include_router(router)

# Define Flet UI main function
def main(page: ft.Page):
    page.title = "AI Code Assistant"
    main_view(page)

# Function to run FastAPI server
def run_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# If running directly, start both API and UI
if __name__ == "__main__":
    # Start API server in a separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Start Flet UI
    ft.app(target=main)