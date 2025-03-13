from pydantic import BaseModel


class RecipeIn(BaseModel):
    title: str
    cooking_time: int
    ingredients: str
    description: str | None = None


class RecipeBaseOut(BaseModel):
    id: int
    title: str

    class Config:
        # orm_mode = True
        from_attributes = True


class RecipeDetailOut(RecipeBaseOut):
    count_of_view: int
    cooking_time: int



class RecipeListOut(RecipeBaseOut):
    ingredients: str
    description: str | None = None



class RecipeFullDetailOut(RecipeDetailOut, RecipeListOut):
    ...