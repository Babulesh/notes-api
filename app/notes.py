from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from .db import get_db
from .models import Note, User
from .schemas import NoteIn, NoteOut, NoteUpdate
from .deps import get_current_user


router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteOut])
async def list_notes(
    db: AsyncSession = Depends(get_db), current: User = Depends(get_current_user),
    limit: int = 50, offset: int = 0
):
    q = (
        select(Note)
        .where(Note.user_id == current.id)
        .order_by(Note.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    res = await db.execute(q)
    return res.scalars().all()


@router.post("/", response_model=NoteOut, status_code=201)
async def create_note(
    payload: NoteIn,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    note = Note(user_id=current.id, title=payload.title, content=payload.content)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


@router.get("/{note_id}", response_model=NoteOut)
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    res = await db.execute(select(Note).where(Note.id == note_id, Note.user_id == current.id))
    note = res.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Not found")
    return note


@router.patch("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int,
    payload: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    res = await db.execute(select(Note).where(Note.id == note_id, Note.user_id == current.id))
    note = res.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Not found")


    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content


    await db.commit()
    await db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    res = await db.execute(select(Note).where(Note.id == note_id, Note.user_id == current.id))
    note = res.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(note)
    await db.commit()
    return None