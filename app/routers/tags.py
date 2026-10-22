from fastapi import HTTPException, status, APIRouter, Depends
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/tags",
    tags= ['Tags']
)


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.TagOut)

def create_tag(name: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    existing = db.query(models.Tag).filter(models.Tag.name == name).first()

    if existing:
        return existing

    new_tag = models.Tag(name = name)

    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


@router.get("/", response_model=list[schemas.TagOut])

def get_tag(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    return db.query(models.Tag).all()

