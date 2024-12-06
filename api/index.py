from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import get_recipes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecipeRequest(BaseModel):
    recipes: Optional[str] = None

@app.post("/api/recipes")
async def recipe_endpoint(recipe_request: RecipeRequest):
    if recipe_request.recipes:
        structured_recipe = get_recipes(recipe_request.recipes)
        return {"message": structured_recipe}
    return {"message": "No recipes specified"} 