from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int

@dataclass 
class RecipeSummary():
	name: str
	cookTime: int
	ingredients: List[RequiredItem]

# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str, None]:
	
	recipeName = re.sub(r"[_-]", ' ', recipeName) 
	recipeName = re.sub(r"[^a-zA-Z\s]", '', recipeName)	
	recipeName = re.sub(r"\s+", ' ', recipeName).strip()
	recipeName = recipeName.title()

	if recipeName: 
		return recipeName
	else: 
		return None

# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	entry_data = request.get_json()
	global cookbook

	entry_type = entry_data.get("type")
	entry_name = entry_data.get("name")

	if entry_type != "recipe" and entry_type != "ingredient":
		return jsonify({"error": "invalid type"}), 400

	if entry_name in cookbook:
		return jsonify({"error": "entry names must be unique"}), 400

	if entry_type == "ingredient":
		cook_time = entry_data.get("cookTime")

		if cook_time is None or not isinstance(cook_time, int) or cook_time < 0:
			return jsonify({"error": "cookTime cannot be negative"}), 400

		cookbook[entry_name] = Ingredient(name=entry_name, cook_time=cook_time)

	if entry_type == "recipe":
		required_items = entry_data.get("requiredItems")

		req_item_names = set()
		req_items = []
		for item in required_items:
			item_name = item.get("name")
			item_quantity = item.get("quantity")

			if item_quantity is None or not isinstance(item_quantity, int) or item_quantity <= 0:
				return jsonify({"error": "requiredItems can only have one element per name"}), 400
			
			if item_name in req_item_names: 
				return jsonify({"error": "requiredItems can only have one element per name"}), 400

			req_item_names.add(item_name)
			req_items.append(RequiredItem(name=item_name, quantity=item_quantity))

		cookbook[entry_name] = Recipe(name=entry_name, required_items=req_items)
	
	return "", 200

# [TASK 3] ====================================================================
# recurses through recipes and adds up total cookTime 
def recurse_recipes(item, summary, quantity):
	global cookbook

	curr_item = cookbook.get(item.name)
	if curr_item is None: return False
	
	if isinstance(curr_item, Ingredient):
		summary.cookTime += curr_item.cook_time * quantity 

		existing_ingredient = None 
		for ing in summary.ingredients:
			if ing.name == item.name:
				existing_ingredient = ing
				break

		if existing_ingredient: 
			existing_ingredient.quantity += quantity
		else:
			addIngredient = RequiredItem(
				name=item.name,
				quantity=quantity,
			)
			summary.ingredients.append(addIngredient)
	
	if isinstance(curr_item, Recipe):
		for sub_item in curr_item.required_items:
			if not recurse_recipes(sub_item, summary, sub_item.quantity * quantity):
				return False

	return True

# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	recipe_name = request.args.get("name")
	global cookbook

	if not recipe_name or recipe_name not in cookbook:
		return "recipe not found", 400

	recipe = cookbook[recipe_name]

	if not isinstance(recipe, Recipe):
		return "recipe not found", 400

	summary = RecipeSummary(
		name=recipe_name,
		cookTime=0,
		ingredients=[]
	)
	for item in recipe.required_items:
		if not recurse_recipes(item, summary, item.quantity):
			return "recipe/ingredient not found", 400

	return jsonify(summary.__dict__), 200
	


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
