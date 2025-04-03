import shutil
from fastapi import APIRouter, Depends, UploadFile, File
from routers.schemas import PostBase, PostDisplay
from sqlalchemy.orm.session import Session
from database.database import get_db
from database import db_post
import string
import random

router = APIRouter(
  prefix='/post',
  tags=['post']
)

@router.post('')
def create_post(request: PostBase, db: Session = Depends(get_db)):
  return db_post.create_post(db, request)

@router.get('/all')
def get_all_posts(db: Session = Depends(get_db)):
  return db_post.get_all_posts(db)

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
  return db_post.delete_post(id, db)

@router.post('/image')
def upload_image(image: UploadFile = File(...)):
  letter = string.ascii_letters
  rand_str = ''.join(random.choice(letter) for i in range(6))
  new = f'_{rand_str}.'
  filename = new.join(image.filename.rsplit('.',1))
  path = f'images/{filename}'

  with open(path, "w+b") as buffer:
    shutil.copyfileobj(image.file, buffer)

  return {'filename': path}
