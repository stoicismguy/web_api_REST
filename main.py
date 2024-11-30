from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel, select, Field
import asyncio
from starlette.concurrency import run_in_threadpool
from utils import get_products
from contextlib import asynccontextmanager


ITEMS = []

DATABASE_URL = "sqlite+aiosqlite:///parser.db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine)


class Item(SQLModel, table=True):
    __tablename__ = "items"
    id:int = Field(primary_key=True)
    title: str = Field()
    price: int = Field()


def create_db():
    engine = create_engine("sqlite:///parser.db")
    SQLModel.metadata.create_all(engine)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

SessionDep = Depends(get_session)

async def preload_database():
    global ITEMS
    async for session in get_session():
        query = await session.execute(select(Item))
        items = query.scalars().all()
        ITEMS = items
    print(f"Database preloaded. items: {len(ITEMS)}")

async def background_parser_async():
    global ITEMS
    async for session in get_session():
        while True:
            products = await run_in_threadpool(get_products)
            for title, price in products:
                item = Item(title=title, price=price)
                if item not in ITEMS:
                    session.add(item)
                    ITEMS.append(item)

            await session.commit()
            print("Items updated.")
            await asyncio.sleep(20)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    await preload_database()
    await startup_events()
    yield

    
async def startup_events():
    asyncio.create_task(background_parser_async())


app = FastAPI(lifespan=lifespan)
# app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items")
async def get_items():
    global ITEMS
    return ITEMS


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, session: AsyncSession=SessionDep):
    item = await session.execute(select(Item).where(Item.id == item_id))
    item = item.scalars().first()
    await session.delete(item)
    await session.commit()
    ITEMS.remove(item)
    return {"message": "Item deleted"}


@app.post("/items/create")
async def create_item(item: Item, session: AsyncSession=SessionDep):
    session.add(item)
    await session.commit()
    return item