from typing import Annotated, List

from fastapi import APIRouter, Query, Path, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud.author import (
    get_authors,
    create_author,
    get_author,
    update_author,
    delete_author,
)
from app.schemas.author import AuthorResponse, AuthorCreate, AuthorUpdate

router = APIRouter(tags=["authors"])


@router.get("/api/authors", response_model=List[AuthorResponse], status_code=200)
async def get_authors_view(
    db: Annotated[Session, Depends(get_db)],
    search: Annotated[str, Query()] = "",
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0, le=100)] = 20,
):
    return get_authors(db, search, skip, limit)


@router.post("/api/authors", response_model=AuthorResponse)
async def create_author_view(
    db: Annotated[Session, Depends(get_db)], data: AuthorCreate
):
    author = create_author(db, data)

    return author


@router.get("/api/authors/{id}", response_model=AuthorResponse)
async def get_author_view(
    id: Annotated[int, Path(ge=0)], db: Annotated[Session, Depends(get_db)]
):
    author = get_author(db, id)
    if author:
        return author
    else:
        raise HTTPException(status_code=404, detail="author not found.")


@router.patch("/api/authors/{id}", response_model=AuthorResponse)
async def update_author_view(
    id: Annotated[int, Path(ge=0)],
    db: Annotated[Session, Depends(get_db)],
    data: AuthorUpdate,
):
    existing_author = get_author(db, id)
    if existing_author is None:
        raise HTTPException(status_code=404, detail="author not found.")

    author = update_author(db, existing_author, data)

    return AuthorResponse(
        id=author.id,
        first_name=author.first_name,
        last_name=author.last_name,
        bio=author.bio,
        born_date=author.born_date,
    )


@router.delete("/api/authors/{id}")
async def delete_author_view(
    id: Annotated[int, Path(ge=0)], db: Annotated[Session, Depends(get_db)]
):
    existing_author = get_author(db, id)
    if existing_author is None:
        raise HTTPException(status_code=404, detail="author not found.")

    delete_author(db, existing_author)

    return {"message": "author deleted."}
