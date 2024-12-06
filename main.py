from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_community.document_loaders import TextLoader
from pydantic import BaseModel, Field
from typing import List

class Recipe(BaseModel):
    """
    Use this model when working with complete cooking recipes.
    """
    title: str = Field(description="Name of the recipe")
    ingredients: List[str] = Field(description="List of ingredients needed for the recipe")
    instructions: List[str] = Field(description="Step-by-step instructions to prepare the recipe")

class Recipes(BaseModel):
    """
    Use this model when working with complete cooking recipes.
    """
    recipes: List[Recipe] = Field(description="A list of recipes")

def get_recipes(recipe_text: str):
    # Initialize model and parser
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_model = model.with_structured_output(Recipes)

    # Create prompt template with chaining syntax
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that converts recipe text into structured data. Please convert the following recipes into a structured format."),
        ("human", "Recipe text: {recipe_text}")
    ])

    # Create chain using the | operator
    chain = prompt | structured_model

    structured_recipe = chain.invoke({"recipe_text": recipe_text})
    return structured_recipe

# Load and process recipe
if __name__ == "__main__":
    # loader = TextLoader("class_4/class_code/recipe/recipe_doc.txt")
    # doc = loader.load()
    # recipe_text = doc[0].page_content
    recipe_text = """Banana Pancakes
1-1/2 cups all purpose flour, spooned into measuring cup and leveled off
2 tablespoons sugar
2-1/2 teaspoons baking powder
1/2 teaspoon salt
1 small, over-ripe banana, peeled (the browner, the better)
1 cup plus 2 tablespoons low fat milk
2 large eggs
1/2 teaspoon vanilla extract
3 tablespoons unsalted butter, melted
Vegetable oil 
Unsalted butter
Maple syrup
Sliced bananas
Confectioners' sugar (optional)
Instructions
In a medium bowl, whisk together the flour, sugar, baking powder and salt.
In a small bowl, mash the banana with a fork until almost smooth. Whisk in the eggs, then add the milk and vanilla and whisk until well blended. Pour the banana mixture and the melted butter into the flour mixture. Fold the batter gently with a rubber spatula until just blended; do not over-mix. The batter will be thick and lumpy.
Set a griddle or non-stick pan over medium heat until hot. Put a pad of butter and one tablespoon vegetable oil onto the griddle, and swirl it around. Drop the batter by 1/4-cupfuls onto the griddle, spacing the pancakes about 2 inches apart. Cook until a few holes form on top of each pancake and the underside is golden brown, about 2 minutes. Flip the pancakes and cook until the bottom is golden brown and the top is puffed, 1 to 2 minutes more. Using the spatula, transfer the pancakes to a serving plate.
Wipe the griddle clean with paper towels, add more butter and oil, and repeat with the remaining batter. Serve the pancakes while still hot with maple syrup, sliced bananas and confectioners' sugar if desired."""
    structured_recipe = get_recipes(recipe_text)
    print(structured_recipe)
