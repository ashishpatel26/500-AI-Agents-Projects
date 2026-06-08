"""
Recipe Recommendation Agent using Agno-style single agent.

Suggests recipes based on available ingredients, dietary restrictions,
and time constraints.

Usage:
    python agent.py --ingredients "chicken, garlic, lemon, rosemary"
    python agent.py --ingredients "tofu, broccoli, soy sauce" --diet vegan --time 20
"""

import argparse
import json
import os
import re

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

RECIPE_PROMPT = """You are a professional chef and nutritionist. Given available ingredients and constraints,
suggest 3 recipes. Return JSON:
{
  "recipes": [
    {
      "name": "Recipe Name",
      "cuisine": "Italian/Asian/etc",
      "difficulty": "Easy/Medium/Hard",
      "prep_time": "X minutes",
      "cook_time": "X minutes",
      "servings": N,
      "ingredients_needed": ["ingredient (amount)"],
      "missing_ingredients": ["optional additions"],
      "instructions": ["Step 1: ...", "Step 2: ..."],
      "nutrition_per_serving": {"calories": N, "protein": "Xg", "carbs": "Xg", "fat": "Xg"},
      "tips": "Chef's tip"
    }
  ],
  "recommended": "Recipe Name (best match)"
}
Return only valid JSON."""


def parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    return json.loads(cleaned)


def get_recipes(ingredients: list[str], diet: str, time_limit: int, servings: int) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    constraints = []
    if diet:
        constraints.append(f"Dietary restriction: {diet}")
    if time_limit:
        constraints.append(f"Max total time: {time_limit} minutes")
    if servings:
        constraints.append(f"Servings needed: {servings}")

    messages = [
        SystemMessage(content=RECIPE_PROMPT),
        HumanMessage(content=f"Available ingredients: {', '.join(ingredients)}\n\nConstraints:\n{chr(10).join(constraints) if constraints else 'None'}"),
    ]

    response = llm.invoke(messages)
    return parse_json_response(response.content)


def display_recipe(recipe: dict):
    print(f"\n🍽️  {recipe.get('name', 'Recipe')} ({recipe.get('cuisine', 'N/A')})")
    print(f"⏱️  Prep: {recipe.get('prep_time', 'N/A')} | Cook: {recipe.get('cook_time', 'N/A')} | Difficulty: {recipe.get('difficulty', 'N/A')}")
    print(f"👥 Serves: {recipe.get('servings', 'N/A')}")
    print(f"\n📝 Ingredients:")
    for ing in recipe.get("ingredients_needed", []):
        print(f"  • {ing}")
    if recipe.get("missing_ingredients"):
        print(f"\n➕ Optional additions: {', '.join(recipe['missing_ingredients'])}")
    print(f"\n👨‍🍳 Instructions:")
    for i, step in enumerate(recipe.get("instructions", []), 1):
        print(f"  {i}. {step}")
    n = recipe.get("nutrition_per_serving", {})
    if n:
        print(f"\n🥗 Nutrition: {n.get('calories', '?')} cal | Protein: {n.get('protein', '?')} | Carbs: {n.get('carbs', '?')} | Fat: {n.get('fat', '?')}")
    if recipe.get("tips"):
        print(f"\n💡 Chef's tip: {recipe['tips']}")


def main():
    parser = argparse.ArgumentParser(description="Recipe Recommendation Agent")
    parser.add_argument("--ingredients", default="chicken breast, garlic, lemon, olive oil, rosemary, potatoes", help="Comma-separated ingredients")
    parser.add_argument("--diet", default="", help="Dietary restriction (vegan, vegetarian, gluten-free, keto, etc.)")
    parser.add_argument("--time", type=int, default=0, help="Max cooking time in minutes")
    parser.add_argument("--servings", type=int, default=2, help="Number of servings")
    args = parser.parse_args()

    ingredients = [i.strip() for i in args.ingredients.split(",")]
    print(f"\n🥘 Finding recipes with: {', '.join(ingredients)}")
    if args.diet:
        print(f"🥗 Diet: {args.diet}")
    if args.time:
        print(f"⏱️  Max time: {args.time} minutes")

    result = get_recipes(ingredients, args.diet, args.time, args.servings)

    print("\n" + "=" * 60)
    recipes = result.get("recipes", [])
    recommended = result.get("recommended") or (recipes[0].get("name", "N/A") if recipes else "N/A")
    print("✅ RECOMMENDED:", recommended)
    print("=" * 60)

    for recipe in recipes:
        display_recipe(recipe)
        print("\n" + "-" * 40)


if __name__ == "__main__":
    main()
