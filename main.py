import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Query, HTTPException
from typing import Union, Annotated, List
from datetime import datetime, timezone
from sqlmodel import Field, Session, create_engine, select, SQLModel, Column
from sqlalchemy.sql.expression import or_
from sqlalchemy.types import JSON

load_dotenv()

#Define the SQLModel and connection
db_username = os.getenv('USER_DB')
db_password = os.getenv('PASSWORD_DB')
db_host = os.getenv('HOST_DB')
db_name = os.getenv('NAME_DB')

url_connection = f'mysql+pymysql://{db_username}:{db_password}@{db_host}:3306/{db_name}'
engine = create_engine(url_connection)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]

#Define models
class PostBase(SQLModel):
    title: str = Field(index=True)
    content: str
    category: str = "General"
    tags: Union[List[str], None] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

class Post(PostBase, table=True):
    id: int = Field(default=None, primary_key=True)
    __tablename__ = "posts"

class PostRead(PostBase):
    id: int

class PostCreate(SQLModel):
    title: str
    content: str
    category: str = "General"
    tags: Union[List[str], None] = None

class PostUpdate(SQLModel):
    title: Union[str, None] = None
    content: Union[str, None] = None
    category: Union[str, None] = None
    tags: Union[List[str], None] = None

#API - PATHS
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.on_event('startup')
async def on_startup():
    create_db_and_tables()

#Create a post
@app.post("/posts", response_model=PostRead, status_code=201)
async def create_post(post: PostCreate, session: session_dep):
    #db_post = Post.model_validate(post)
    db_post = Post.model_validate(post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

#Get all posts
@app.get("/posts/", response_model=list[PostRead])
async def read_posts(
    session: session_dep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts

#Filter post by a search term
@app.get("/posts", response_model=list[PostRead])
async def search_posts(
    *,
    session: session_dep,
    term: Annotated[str, Query(description="Search term to filter posts by title, category or content")]
):
    search_pattern = f"%{term}%"

    statement = select(Post).where(
        or_(
            Post.title.like(search_pattern),
            Post.content.like(search_pattern),
            Post.category.like(search_pattern) 
        )
    )

    results = session.exec(statement).all()

    if not results:
        return []
        #raise HTTPException(status_code=404, detail="No posts found matching the search term")
    return results

#Get a single post
@app.get("/posts/{post_id}", response_model=PostRead)
async def read_post(post_id: int, session: session_dep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

#Update a post
@app.patch("/posts/{post_id}", response_model=PostRead)
async def update_post(
    *, 
    post_id: int, 
    input_post: PostUpdate, 
    session: session_dep
):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    update_data = input_post.model_dump(exclude_unset=True)

    #if not update_data:
    #    return db_post 

    #db_post.model_validate(update_data, update=True)

    if update_data:
        update_data['updated_at'] = datetime.now(timezone.utc)
        db_post.sqlmodel_update(update_data)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)

    return db_post

#Delete a post
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, session: session_dep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"ok": True}