from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from .supabase_client import Note, create_note, get_note, list_notes, update_note, delete_note

app = FastAPI(
    title="Notes API",
    description="API backend for creating, managing, and storing notes using Supabase.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """Health check for the Notes API."""
    return {"message": "Healthy"}
