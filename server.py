from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from main import get_recipes

# Create a model for the request body
class RecipeRequest(BaseModel):
    recipes: Optional[str] = None

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recipes")
async def recipe_endpoint(recipe_request: RecipeRequest):
    if recipe_request.recipes:
        structured_recipe = get_recipes(recipe_request.recipes)
        return {"message": structured_recipe}
    return {"message": "No recipes specified"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
