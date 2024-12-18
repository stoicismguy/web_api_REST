from fastapi import FastAPI, Depends, WebSocket
import json
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
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class ConnectionManager:
    
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
                await connection.send_text(data)


manager = ConnectionManager()

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
                ex = await exists(item)
                if not ex:
                    session.add(item)
                    ITEMS.append(item)
                    await manager.broadcast(f"POST {item.model_dump_json()}")

            await session.commit()
            print("Items updated.")
            await asyncio.sleep(20)

async def exists(item):
    global ITEMS
    for i in ITEMS:
        if i.title == item.title and i.price == item.price:
            return True
    return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    функция preload_database подгружает из бд в список ITEMS,
    спаршенные продукты проверяет есть ли в ITEMS, если нет то добавляет и в ITEMS и в бд
    сделал так чтобы на каждый раз когда парсилось не добавлялись повторы в бд и сохранялись записи post-запросов, а если бы и удаляли бд,
    то записи из post-запросов не сохранились
    """
    create_db()
    await preload_database()
    await startup_events()
    yield

    
async def startup_events():
    asyncio.create_task(background_parser_async())


app = FastAPI(lifespan=lifespan)


@app.get("/items")
async def get_items(session: AsyncSession=SessionDep):
    items = await session.execute(select(Item))
    items = items.scalars().all()
    return items


@app.get("/items/{item_id}")
async def get_item(item_id: int, session: AsyncSession=SessionDep):
    item = await session.execute(select(Item).where(Item.id == item_id))
    item = item.scalars().first()
    return item


@app.post("/items/create")
async def create_item(item: Item, session: AsyncSession=SessionDep):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    await manager.broadcast(f"POST {item.model_dump_json()}")
    return item


@app.put("/items/{item_id}")
async def update_item(item: Item, session: AsyncSession=SessionDep):
    founded = await session.execute(select(Item).where(Item.id == item.id))
    founded = founded.scalars().first()
    founded.title = item.title
    founded.price = item.price
    await session.commit()
    await manager.broadcast(f"PUT {item.model_dump_json()}")
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, session: AsyncSession=SessionDep):
    item = await session.execute(select(Item).where(Item.id == item_id))
    item = item.scalars().first()
    await session.delete(item)
    await manager.broadcast(f"DELETE {item.model_dump_json()}")
    await session.commit()
    return {"message": "Item deleted"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except:
        await manager.broadcast(f"Cliend {websocket} disconnected.")

