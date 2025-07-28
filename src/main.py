from typing import List,Annotated
from fastapi import FastAPI, HTTPException,Depends
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from nikita.src.models import Base, Recipes
from nikita.src.schemas import ReceiptBase, ReceiptPostAdd
from nikita.src.database import engine, Base, get_session

app = FastAPI()

SessionDep = Annotated[AsyncSession,Depends(get_session)]


@app.post("/")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'ok':200}


@app.post('/recipes')
async def recipes(receipt: ReceiptPostAdd,session:SessionDep):
    new_recipes = Recipes(name=receipt.name,
                          time_to_cook=receipt.time_to_cook,
                          description=receipt.description,
                          views=receipt.views)
    session.add(new_recipes)
    await session.commit()
    return {"ok":True}


@app.get('/recipes', response_model=List[ReceiptBase])
async def get_recipe(session:SessionDep):
    res = await session.execute(select(Recipes).order_by(Recipes.views.desc(),
                                                         Recipes.time_to_cook.desc()))
    return res.scalars().all()

@app.get('/recipes/{id}', response_model=List[ReceiptBase])
async def get_recipe(session:SessionDep,id):
    res = await session.execute(select(Recipes).filter(Recipes.id==id))
    return res.scalars().all()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
