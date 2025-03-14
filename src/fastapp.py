from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, Path, status
from sqlalchemy.future import select

from src.database import Base, engine, session
from src.models import Recipe
from src.schemas import (
    RecipeDetailOut,
    RecipeFullDetailOut,
    RecipeIn,
    RecipeListOut,
)


async def get_last_id():
    async with session.begin():
        res = await session.execute(select(Recipe))
        return res.scalars().all()[-1].id


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/home")
async def get_home():
    return {"message": "home page"}


@app.get("/recipes/", response_model=List[RecipeListOut])
async def recipes_get_all() -> List[RecipeListOut]:
    async with session.begin():
        res = await session.execute(
            select(Recipe).order_by(Recipe.count_of_view.desc())
        )
        return res.scalars().all()


@app.get("/recipes/{id}", response_model=RecipeDetailOut)
async def recipe_get_by_id(id: int = Path(title="Id of the recipe")):
    async with session.begin():
        res = await session.execute(select(Recipe).where(Recipe.id == id))
        recipe = res.scalars().one_or_none()
        if recipe is None:
            raise HTTPException(
                status_code=404,
                detail="Рецепт не найден"
            )
        recipe.count_of_view += 1
        return recipe


@app.post(
    "/recipes/",
    response_model=RecipeFullDetailOut,
    status_code=status.HTTP_201_CREATED
)
async def recipes_post(recipe: RecipeIn):
    new_recipe = Recipe(**recipe.model_dump())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe
