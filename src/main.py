from typing import List
from fastapi import FastAPI, HTTPException

from sqlalchemy.future import select

from nikita.src.models import Base, Recipes
from nikita.src.schemas import ReceiptBase, ReceiptPostAdd
from nikita.src.database import engine, session

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message":"hello world"}


@app.on_event('startup')
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event('shutdown')
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/recipes/', response_model=ReceiptPostAdd)
async def recipes(receipt: ReceiptPostAdd) -> Recipes:
    new_recipes = Recipes(name=receipt.name,
                          time_to_cook=receipt.time_to_cook,
                          description=receipt.description,
                          views=receipt.views
                          )
    async with session.begin():
        session.add(new_recipes)
    return new_recipes


@app.delete('/recipes/<int:id>')
async def recipes(id: int):
    db_item = await session.execute(select(Recipes).where(Recipes.id == id))
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(db_item)
    session.commit()
    return {"message": "Item deleted successfully"}


@app.get('/recipes/<int:id>')
async def get_recipes_by_id(id: int):
    res = await session.execute(select(Recipes).where(Recipes.id == id))
    dish = res.scalar()
    if dish:
        dish.views += 1
        await session.commit()
        return dish
    return res.scalars().all()



@app.get('/recipes/', response_model=List[ReceiptBase])
async def get_recipe():
    res = await session.execute(select(Recipes).order_by(Recipes.views.desc(),
                                                         Recipes.time_to_cook.desc()))
    return res.scalars().all()
