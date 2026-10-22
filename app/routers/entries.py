from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import tmdb
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/entries",
    tags=["Entries"]
)

#external api call to tmdb

@router.get("/search/external")
def search_external(query:str, current_user: int = Depends(oauth2.get_current_user)):
   return tmdb.search_media(query)


@router.post("/from-external", status_code=status.HTTP_201_CREATED, response_model=schemas.EntryOut)
def create_entry_from_tmdb(entry: schemas.EntryCreateTMDB, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    title = tmdb.get_media_details(entry.tmdb_id, entry.kind)

    new_entry = models.Entry(
        tmdb_id = entry.tmdb_id,
        user_id=current_user.user_id,
        title=title,
        kind=entry.kind, 
        status=entry.status,
        rating=entry.rating,
        notes=entry.notes)

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EntryOut)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    new_entry = models.Entry(user_id=current_user.user_id, **entry.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

@router.get("/", response_model=list[schemas.EntryOut])
def get_entries(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    status_filter: Optional[schemas.EntryStatus] = None,
    kind: Optional[schemas.EntryKind] = None,
    search: Optional[str] = "",
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    sort_by: Optional[str] = "created_at"):
    tag: Optional[str] = None

    query = db.query(models.Entry).filter(models.Entry.user_id == current_user.user_id)

    if tag:
        query = query.join(models.EntryTag).join(models.Tag).filter(models.Tag.name == tag)

    if status_filter:
        query = query.filter(models.Entry.status == status_filter)
    if kind:
        query = query.filter(models.Entry.kind == kind)
    if search:
        query = query.filter(models.Entry.title.contains(search))

    sort_column = getattr(models.Entry, sort_by, models.Entry.created_at)

    entries = query.order_by(sort_column.desc()).offset(skip).limit(limit).all()
    return entries


@router.post("/{id}/tags/{tag_id}", response_model= schemas.EntryOut)

def add_tags_to_entries(id: int, tag_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    entry = db.query(models.Entry).filter(id == models.Entry.id, models.Entry.user_id == current_user.user_id).first()

    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'entry with id = {id} was not found.')

    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()

    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'tag with id = {tag_id} was not found.')

    if tag not in entry.tags:
        entry.tags.append(tag)
        db.commit()
        db.refresh(entry)

    return entry

@router.delete("/{id}/tags/{tag_id}", response_model= schemas.EntryOut)
def remove_tag_from_entries(tag_id: int,id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    entry = db.query(models.Entry).filter(models.Entry.id == id, models.Entry.user_id == current_user.user_id).first()

    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'entry with id = {id} wasnt found.')

    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()

    if tag and tag in entry.tags:
        entry.tags.remove(tag)
        db.commit()
        db.refresh(entry)

    return entry



@router.get("/{id}", response_model=schemas.EntryOut)
def get_entry(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    entry = db.query(models.Entry).filter(models.Entry.id == id, models.Entry.user_id == current_user.user_id).first()

    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Entry with id: {id} was not found")

    return entry


@router.put("/{id}", response_model=schemas.EntryOut)
def update_entry(id: int, updated_entry: schemas.EntryUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    entry_query = db.query(models.Entry).filter(models.Entry.id == id, models.Entry.user_id == current_user.user_id)
    entry = entry_query.first()

    if not entry:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Entry with id: {id} was not found")

    if entry.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this entry")

    entry_query.update(updated_entry.model_dump(exclude_unset= True), synchronize_session= False)
    db.commit()
    return entry


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    entry_query = db.query(models.Entry).filter(models.Entry.id == id, models.Entry.user_id == current_user.user_id)
    entry = entry_query.first()

    if not entry: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Entry with id: {id} was not found')

    entry_query.delete(synchronize_session= False)
    db.commit()
    return (f'Entry with id: {id} was successfully deleted.')









  