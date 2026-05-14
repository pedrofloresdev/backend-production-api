import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.models.post import Post
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.post import PostCreate, PostPatch, PostResponse, PostUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostResponse, status_code=201)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_post = Post(title=post.title, content=post.content, owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    logger.info("Created post id=%s by user id=%s", new_post.id, current_user.id)
    return new_post


@router.get("", response_model=list[PostResponse])
def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(Post).offset(skip).limit(limit).all()


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    post.title = post_data.title
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post


@router.patch("/{post_id}", response_model=PostResponse)
def patch_post(
    post_id: int,
    post_data: PostPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(post)
    db.commit()
