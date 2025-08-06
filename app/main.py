from fastapi.responses import RedirectResponse

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import get_db, Base, engine
from app.cache import get_cached_url, set_cached_url

import os
from dotenv import load_dotenv

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_URL = os.getenv("BASE_URL")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")



@app.post("/shorten", response_model=schemas.URLInfo)
def shorten_url(request: schemas.URLCreate, db: Session = Depends(get_db)):
    code = utils.generate_short_code()
    db_url = models.URL(original_url=request.original_url, short_code=code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    short_url = f"{BASE_URL}/{code}"
    return schemas.URLInfo(short_url=short_url, original_url=db_url.original_url, visit_count=db_url.visit_count)


# @app.get("/{code}")
# def redirect(code: str, db: Session = Depends(get_db)):
#     url = db.query(models.URL).filter(models.URL.short_code == code).first()
#     if not url:
#         raise HTTPException(status_code=404, detail="Short URL not found")

#     url.visit_count += 1
#     db.commit()

#     return RedirectResponse(url.original_url)


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    # First check Redis
    original_url = get_cached_url(code)
    if original_url:
        return RedirectResponse(original_url)

    # Fallback to DB
    url = db.query(models.URL).filter(models.URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Cache for future use
    set_cached_url(code, url.original_url)

    # Update visit count
    url.visit_count += 1
    db.commit()

    return RedirectResponse(url.original_url)



@app.get("/stats/{code}")
def get_url_stats(code: str, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter(models.URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "visit_count": url.visit_count,
        "created_at": url.created_at
    }