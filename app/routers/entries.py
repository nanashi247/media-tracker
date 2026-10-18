
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/entries",
    tags=["Entries"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.EntryOut)
def create_entry(entry: schemas.EntryCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    new_entry = models.Entry(user_id=current_user.user_id, **entry.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


@router.get("/", response_model=list[schemas.EntryOut])
def get_entries(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    entries = db.query(models.Entry).filter(models.Entry.user_id == current_user.user_id).all()
    return entries

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

    entry_query.update(updated_entry.model_dump(exclude_unser= True), synchronize_session= False)
    db.commit()
    return entry


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    entry_query = db.query(models.Entry).filter(models.Entry.id == id, models.Entry.user_id == current_user.user_id)
    entry = entry_query.first()

    if not entry: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Entry with id: {id} was not found')

    return entry_query.delete(synchronize_session= False)









  