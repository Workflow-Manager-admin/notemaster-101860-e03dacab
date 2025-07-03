from fastapi import FastAPI, HTTPException, status, Path
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from .supabase_client import (
    Note,
    create_note,
    get_note,
    list_notes,
    update_note,
    delete_note,
)

app = FastAPI(
    title="Notes API",
    description="API backend for creating, managing, and storing notes using Supabase.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    openapi_tags=[
        {
            "name": "notes",
            "description": "CRUD endpoints for managing notes.",
        }
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["health"])
def health_check():
    """Health check for the Notes API."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[Note],
    summary="List all notes",
    description="Retrieve all notes sorted by last update (descending).",
    tags=["notes"],
    response_model_exclude_none=True
)
def api_list_notes():
    """
    Returns all notes from the database.

    Returns:
        List[Note]: All notes, most recent first.
    """
    return list_notes()


# PUBLIC_INTERFACE
@app.get(
    "/notes/{note_id}",
    response_model=Note,
    summary="Get a note by ID",
    description="Retrieve a note by its unique ID.",
    tags=["notes"],
    responses={
        404: {"description": "Note not found"},
        200: {"description": "Note found", "model": Note}
    },
    response_model_exclude_none=True
)
def api_get_note(
    note_id: int = Path(..., title="Note ID", description="The unique ID of the note to retrieve"),
):
    """
    Returns a single note for the given ID.

    Args:
        note_id: Note's unique identifier.

    Returns:
        Note
    """
    note = get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Create a new note with a title and content.",
    tags=["notes"],
    response_model_exclude_none=True
)
def api_create_note(note: Note):
    """
    Create a new note.

    Args:
        note: Note object without id/created_at/updated_at.

    Returns:
        The newly created Note.
    """
    created = create_note(note)
    return created


# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    summary="Update a note",
    description="Update the title/content of an existing note.",
    tags=["notes"],
    responses={
        404: {"description": "Note not found"},
        200: {"description": "Updated note", "model": Note},
    },
    response_model_exclude_none=True
)
def api_update_note(
    note_id: int = Path(..., title="Note ID", description="The unique ID of the note to update"),
    note: Note = None,
):
    """
    Update the fields of a note.

    Args:
        note_id: ID of the note to update
        note: The fields to update

    Returns:
        The updated Note, or 404 if not found.
    """
    updated = update_note(note_id, note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated


# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its unique ID.",
    tags=["notes"],
    responses={
        204: {"description": "Note deleted"},
        404: {"description": "Note not found"},
    },
)
def api_delete_note(
    note_id: int = Path(..., title="Note ID", description="The unique ID of the note to delete"),
):
    """
    Delete a note.

    Args:
        note_id: The ID of the note to remove.

    Returns:
        HTTP 204 if deleted, HTTP 404 if not found.
    """
    deleted = delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
